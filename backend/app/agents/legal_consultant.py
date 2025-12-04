import re
from typing import List, Dict, Any
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStore
from app.models.schemas import Citation, ChatResponse

class LegalConsultantAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.vector_store = VectorStore()

    async def process_query(self, question: str) -> ChatResponse:
        """处理法律咨询查询"""
        print(f"\n=== 处理查询: {question} ===")
        # 1. 向量检索
        search_results = self.vector_store.search(question, top_k=5)
        print(f"检索到 {len(search_results)} 个相关文档")
        
        if not search_results:
            print("⚠ 警告: 未检索到任何相关文档")
            return ChatResponse(
                answer="抱歉，知识库中未找到相关信息，无法回答您的问题。请检查：1) 向量库是否成功加载数据 2) 查询是否与知识库内容相关",
                citations=[],
                sources=[]
            )
        
        # 2. 格式化上下文
        context_chunks = [
            {
                "source_id": r["source_id"],
                "article_name": r["article_name"],
                "section": r["section"],
                "content": r["content"]
            }
            for r in search_results
        ]
        
        # 3. 调用LLM生成回答
        messages = self.llm_service.format_legal_prompt(
            question=question,
            context_chunks=context_chunks,
            agent_type="consultant"
        )
        
        answer = await self.llm_service.chat(messages, temperature=0.3)
        
        # 4. 提取引用
        citations = self._extract_citations(answer, search_results)
        
        return ChatResponse(
            answer=answer,
            citations=citations,
            sources=search_results
        )

    def _extract_citations(self, answer: str, search_results: List[Dict]) -> List[Citation]:
        """从回答中提取引用"""
        citations = []
        # 匹配 [[source_id]] 格式
        pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, answer)
        
        # 根据source_id查找对应的文档
        source_map = {r["source_id"]: r for r in search_results}
        
        seen_ids = set()
        for source_id in matches:
            if source_id in source_map and source_id not in seen_ids:
                result = source_map[source_id]
                citations.append(Citation(
                    source_id=source_id,
                    article_name=result["article_name"],
                    section=result.get("section", ""),
                    content=result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"],
                    url=result.get("url", "")
                ))
                seen_ids.add(source_id)
        
        return citations

