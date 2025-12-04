import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
from app.services.embedding_service import EmbeddingService
import uuid

class VectorStore:
    def __init__(self):
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "legal_documents")
        self.use_memory = False
        
        # 尝试连接Qdrant，设置较短的超时时间
        try:
            print(f"尝试连接到Qdrant: {self.host}:{self.port}")
            self.client = QdrantClient(
                host=self.host, 
                port=self.port,
                timeout=3.0  # 3秒超时
            )
            # 快速测试连接
            try:
                self.client.get_collections()
                print(f"✓ 成功连接到Qdrant: {self.host}:{self.port}")
            except Exception as e:
                print(f"⚠ Qdrant连接测试失败: {e}")
                print("切换到内存模式...")
                self.client = QdrantClient(":memory:")
                self.use_memory = True
        except Exception as e:
            print(f"⚠ 无法连接到Qdrant ({self.host}:{self.port}): {e}")
            print("切换到内存模式...")
            self.client = QdrantClient(":memory:")
            self.use_memory = True
        
        self.embedding_service = EmbeddingService()
        self._ensure_collection()

    def _ensure_collection(self):
        """确保集合存在"""
        try:
            # 对于内存模式，直接尝试创建集合
            if self.use_memory:
                try:
                    dim = self.embedding_service.model.get_sentence_embedding_dimension()
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(
                            size=dim,
                            distance=Distance.COSINE
                        )
                    )
                    print(f"✓ 在内存模式中创建集合: {self.collection_name}")
                except Exception as e:
                    # 集合可能已存在
                    if "already exists" in str(e).lower() or "exists" in str(e).lower():
                        print(f"集合 {self.collection_name} 已存在")
                    else:
                        raise
            else:
                # 远程模式，检查集合是否存在
                try:
                    collections = self.client.get_collections().collections
                    collection_names = [c.name for c in collections]
                    
                    if self.collection_name not in collection_names:
                        dim = self.embedding_service.model.get_sentence_embedding_dimension()
                        self.client.create_collection(
                            collection_name=self.collection_name,
                            vectors_config=VectorParams(
                                size=dim,
                                distance=Distance.COSINE
                            )
                        )
                        print(f"✓ 创建集合: {self.collection_name}")
                    else:
                        print(f"集合 {self.collection_name} 已存在")
                except Exception as e:
                    print(f"⚠ 检查集合时出错: {e}")
                    # 如果远程连接有问题，切换到内存模式
                    if "timeout" in str(e).lower() or "connection" in str(e).lower():
                        print("切换到内存模式...")
                        self.client = QdrantClient(":memory:")
                        self.use_memory = True
                        self._ensure_collection()  # 递归调用
        except Exception as e:
            print(f"✗ 集合初始化错误: {e}")
            import traceback
            traceback.print_exc()

    def add_documents(self, documents: List[Dict[str, Any]]):
        """添加文档到向量库"""
        if not documents:
            print("警告: 没有文档需要添加")
            return
        
        try:
            texts = [doc["content"] for doc in documents]
            print(f"正在生成 {len(texts)} 个文档的嵌入向量...")
            embeddings = self.embedding_service.embed_documents(texts)
            print(f"✓ 嵌入向量生成完成")
            
            points = []
            for i, doc in enumerate(documents):
                original_id = doc.get("id", str(uuid.uuid4()))
                source_id = doc.get("source_id", original_id)
                
                # Qdrant内存模式要求ID必须是字符串或整数
                # 使用UUID5基于命名空间和原始ID生成确定性UUID，然后转换为字符串
                namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # 固定命名空间
                try:
                    # 如果已经是UUID格式，转换为字符串
                    uuid_obj = uuid.UUID(original_id)
                    point_id = str(uuid_obj)
                except (ValueError, AttributeError, TypeError):
                    # 如果不是UUID格式，转换为UUID再转字符串（确定性转换）
                    uuid_obj = uuid.uuid5(namespace, str(original_id))
                    point_id = str(uuid_obj)
                
                points.append(
                    PointStruct(
                        id=point_id,  # 使用字符串格式的UUID
                        vector=embeddings[i],
                        payload={
                            "content": doc["content"],
                            "article_name": doc.get("article_name", ""),
                            "section": doc.get("section", ""),
                            "source_id": source_id,  # 保留原始ID在payload中
                            "original_id": original_id,  # 也保存原始ID
                            "doc_type": doc.get("doc_type", "statute"),
                            "url": doc.get("url", ""),
                            **doc.get("metadata", {})
                        }
                    )
                )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )
            print(f"✓ 成功添加 {len(points)} 个文档到向量库")
        except Exception as e:
            error_str = str(e).lower()
            if "timeout" in error_str or "connection" in error_str or "timed out" in error_str:
                print(f"⚠ 远程Qdrant操作超时，切换到内存模式...")
                # 切换到内存模式并重试
                self.client = QdrantClient(":memory:")
                self.use_memory = True
                # 重新创建集合
                try:
                    dim = self.embedding_service.model.get_sentence_embedding_dimension()
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(
                            size=dim,
                            distance=Distance.COSINE
                        )
                    )
                    print(f"✓ 在内存模式中创建集合")
                except Exception as e2:
                    if "already exists" not in str(e2).lower():
                        print(f"⚠ 创建集合时出错（可能已存在）: {e2}")
                # 重试插入
                try:
                    self.client.upsert(
                        collection_name=self.collection_name,
                        points=points,
                        wait=True
                    )
                    print(f"✓ 成功添加 {len(points)} 个文档到向量库（内存模式）")
                except Exception as e2:
                    print(f"✗ 内存模式添加文档也失败: {e2}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"✗ 添加文档错误: {e}")
                import traceback
                traceback.print_exc()

    def _simple_keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """简单的关键词搜索（fallback方法）"""
        try:
            # 获取所有文档
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                limit=1000  # 获取所有文档
            )
            
            # 简单的关键词匹配
            query_words = set(query.lower().split())
            scored_docs = []
            
            for point in scroll_result[0]:
                payload = point.payload
                content = payload.get("content", "").lower()
                article_name = payload.get("article_name", "").lower()
                section = payload.get("section", "").lower()
                
                # 计算匹配分数
                score = 0
                for word in query_words:
                    if word in content:
                        score += 2
                    if word in article_name:
                        score += 1
                    if word in section:
                        score += 1
                
                if score > 0:
                    scored_docs.append({
                        "source_id": payload.get("source_id", ""),
                        "article_name": payload.get("article_name", ""),
                        "section": payload.get("section", ""),
                        "content": payload.get("content", ""),
                        "doc_type": payload.get("doc_type", "statute"),
                        "url": payload.get("url", ""),
                        "score": score / 10.0,  # 归一化到0-1范围
                        "metadata": {k: v for k, v in payload.items() 
                                   if k not in ["content", "article_name", "section", "source_id", "doc_type", "url"]}
                    })
            
            # 按分数排序
            scored_docs.sort(key=lambda x: x["score"], reverse=True)
            return scored_docs[:top_k]
        except Exception as e:
            print(f"关键词搜索失败: {e}")
            return []

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        try:
            print(f"搜索查询: {query}")
            
            # 检查集合是否存在
            try:
                collection_info = self.client.get_collection(self.collection_name)
                count = collection_info.points_count
                print(f"向量库中共有 {count} 个文档")
                if count == 0:
                    print("⚠ 警告: 向量库为空，请检查数据是否成功加载")
                    return []
            except Exception as e:
                print(f"⚠ 无法获取集合信息: {e}")
                return []
            
            # 尝试向量搜索
            try:
                query_embedding = self.embedding_service.embed_query(query)
                print(f"✓ 查询向量生成完成 (维度: {len(query_embedding)})")
                
                search_result = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=top_k,
                    query_filter=None  # 可以添加过滤条件
                )
                
                print(f"向量搜索返回 {len(search_result)} 个结果")
                results = []
                for hit in search_result:
                    payload = hit.payload
                    results.append({
                        "source_id": payload.get("source_id", ""),
                        "article_name": payload.get("article_name", ""),
                        "section": payload.get("section", ""),
                        "content": payload.get("content", ""),
                        "doc_type": payload.get("doc_type", "statute"),
                        "url": payload.get("url", ""),
                        "score": hit.score,
                        "metadata": {k: v for k, v in payload.items() 
                                   if k not in ["content", "article_name", "section", "source_id", "doc_type", "url"]}
                    })
                    print(f"  - {payload.get('article_name', '')} {payload.get('section', '')} (相似度: {hit.score:.3f})")
                
                return results
            except Exception as e:
                print(f"⚠ 向量搜索失败: {e}")
                print("尝试使用关键词搜索...")
                # 使用关键词搜索作为fallback
                results = self._simple_keyword_search(query, top_k)
                print(f"关键词搜索返回 {len(results)} 个结果")
                return results
                
        except Exception as e:
            print(f"✗ 搜索错误: {e}")
            import traceback
            traceback.print_exc()
            return []

