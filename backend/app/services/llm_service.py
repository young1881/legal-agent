import os
import httpx
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.api_key = os.getenv("SJTU_API_KEY", "your-api-key")
        self.api_url = os.getenv("SJTU_API_URL", "https://models.sjtu.edu.cn/api/v1")
        self.model_name = os.getenv("MODEL_NAME", "deepseek-v3")
        self.base_url = f"{self.api_url}/chat/completions"

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        stream: bool = False
    ) -> str:
        """调用LLM API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        print(f"调用LLM API: {self.base_url}")
        print(f"模型: {self.model_name}, 消息数量: {len(messages)}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.base_url, headers=headers, json=data)
                print(f"API响应状态码: {response.status_code}")
                
                if response.status_code != 200:
                    error_detail = ""
                    try:
                        error_detail = response.json()
                    except:
                        error_detail = response.text[:500]  # 限制长度
                    print(f"API错误详情: {error_detail}")
                    raise Exception(f"LLM API调用失败 (状态码: {response.status_code}): {error_detail}")
                
                result = response.json()
                
                # 检查响应格式
                if "choices" not in result or len(result["choices"]) == 0:
                    raise Exception(f"API响应格式异常: {result}")
                
                return result["choices"][0]["message"]["content"].strip()
            except httpx.HTTPStatusError as e:
                error_detail = ""
                try:
                    error_detail = e.response.json()
                except:
                    error_detail = e.response.text[:500]
                print(f"HTTP错误: {error_detail}")
                raise Exception(f"LLM API调用失败 (状态码: {e.response.status_code}): {error_detail}")
            except httpx.RequestError as e:
                print(f"请求错误: {e}")
                raise Exception(f"LLM API请求失败: {str(e)}")
            except Exception as e:
                print(f"其他错误: {e}")
                raise Exception(f"LLM API调用失败: {str(e)}")

    def format_legal_prompt(
        self,
        question: str,
        context_chunks: List[Dict],
        agent_type: str = "consultant"
    ) -> List[Dict[str, str]]:
        """格式化法律咨询Prompt"""
        context_text = "\n\n".join([
            f"【参考资料 {i+1}】\n"
            f"来源: {chunk.get('article_name', '未知')} {chunk.get('section', '')}\n"
            f"内容: {chunk.get('content', '')}\n"
            f"[来源ID: {chunk.get('source_id', '')}]"
            for i, chunk in enumerate(context_chunks)
        ])
        
        if agent_type == "consultant":
            system_prompt = """你是一名资深的中国法律顾问。请严格基于以下【参考资料】回答用户问题。

【回答要求】：
1. 引用规范：每一处法律结论必须在句尾标注来源，格式为 [[来源ID]]。
2. 严谨性：如果【参考资料】中没有包含回答问题所需的信息，请直接说明"现有资料不足以回答该问题"，严禁编造法律条文。
3. 结构：先给出简短结论，再展开法律依据，最后给出实务建议。
"""
        else:
            system_prompt = "你是一个专业的法律助手，请基于提供的参考资料回答问题。"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"【参考资料】：\n\n{context_text}\n\n【用户问题】：\n{question}"}
        ]
        
        return messages

