import os
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import warnings

class EmbeddingService:
    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
        # 使用轻量级模型作为快速原型，实际生产环境使用bge-m3
        self.model = None
        model_attempts = [
            'paraphrase-multilingual-MiniLM-L12-v2',
            'all-MiniLM-L6-v2',
            'all-MiniLM-L12-v2'
        ]
        
        for model_name_attempt in model_attempts:
            try:
                print(f"尝试加载模型: {model_name_attempt}")
                # 禁用警告
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    self.model = SentenceTransformer(model_name_attempt)
                print(f"✓ Embedding模型加载成功: {model_name_attempt} ({self.model.get_sentence_embedding_dimension()}维)")
                break
            except Exception as e:
                print(f"✗ 模型 {model_name_attempt} 加载失败: {str(e)}")
                continue
        
        if self.model is None:
            raise Exception("所有embedding模型加载失败，请检查网络连接或使用本地模型")

    def embed_query(self, text: str) -> List[float]:
        """对查询文本进行嵌入"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """对文档列表进行嵌入"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

