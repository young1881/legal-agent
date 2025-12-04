# 后端服务

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 主应用
│   ├── agents/              # Agent 实现
│   │   ├── __init__.py
│   │   └── legal_consultant.py
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── services/            # 核心服务
│       ├── __init__.py
│       ├── llm_service.py    # LLM API 服务
│       ├── embedding_service.py  # 文本嵌入服务
│       ├── vector_store.py   # 向量数据库服务
│       └── data_loader.py   # 测试数据加载
├── requirements.txt
├── .env.example
└── test_api.py              # API 测试脚本
```

## 核心功能

### 1. LLM 服务 (llm_service.py)
- 封装上海交通大学模型 API 调用
- 支持法律咨询 Prompt 格式化
- 异步请求处理

### 2. 向量存储 (vector_store.py)
- Qdrant 向量数据库集成
- 支持内存模式（无需安装 Qdrant）
- 文档检索和相似度搜索

### 3. 嵌入服务 (embedding_service.py)
- 使用 Sentence Transformers
- 支持多语言文本嵌入
- 自动下载模型

### 4. 法律咨询 Agent (legal_consultant.py)
- RAG 检索流程
- 引用提取和追踪
- 基于知识库的严谨回答

## API 接口

### POST /api/chat
法律咨询接口

**请求体:**
```json
{
  "message": "什么是正当防卫？",
  "agent_type": "consultant"
}
```

**响应:**
```json
{
  "answer": "正当防卫是指...[[xingfa-20]]",
  "citations": [
    {
      "source_id": "xingfa-20",
      "article_name": "中华人民共和国刑法",
      "section": "第二十条",
      "content": "为了使国家...",
      "url": "https://example.com/xingfa#20"
    }
  ],
  "sources": [...]
}
```

### GET /api/search
直接搜索向量库

**参数:**
- `query`: 搜索查询
- `top_k`: 返回结果数量（默认5）

## 环境变量

参考 `.env.example` 文件配置：

- `SJTU_API_KEY`: API 密钥
- `SJTU_API_URL`: API 地址
- `MODEL_NAME`: 模型名称
- `QDRANT_HOST`: Qdrant 主机
- `QDRANT_PORT`: Qdrant 端口

## 测试

运行测试脚本：
```bash
python test_api.py
```

确保后端服务已启动。

