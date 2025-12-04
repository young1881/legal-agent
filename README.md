# 法学AI-Agent 系统

基于RAG（检索增强生成）的法学智能助手系统，支持法律咨询、案例检索和引用追踪。

## 功能特点

- ✅ **RAG优先**: 所有回答基于知识库检索，避免幻觉
- ✅ **引用追踪**: 每个回答都可以追溯到原始法律条文
- ✅ **模块化设计**: 易于扩展和替换组件
- ✅ **多Agent支持**: 支持咨询、出题等不同场景

## 技术栈

### 后端
- FastAPI - 异步Web框架
- LangChain - AI编排框架
- Qdrant - 向量数据库
- Sentence Transformers - 文本嵌入

### 前端
- Next.js - React框架
- ShadcnUI - UI组件库
- TailwindCSS - 样式框架

## 快速开始

### 1. 安装依赖

#### 后端
```bash
cd backend
pip install -r requirements.txt
```

#### 前端
```bash
cd frontend
npm install
```

### 2. 配置环境变量

在 `backend` 目录下创建 `.env` 文件，参考 `backend/ENV_SETUP.md` 进行配置。

**必需配置：**
- `SJTU_API_KEY`: 你的API密钥（从API提供方获取）

**可选配置：**
- `QDRANT_HOST`: Qdrant服务地址（默认localhost）
- `QDRANT_PORT`: Qdrant端口（默认6333）

### 3. 启动Qdrant（可选）

如果使用本地Qdrant：
```bash
docker run -p 6333:6333 qdrant/qdrant
```

或者系统会自动使用内存模式。

### 4. 启动后端

```bash
cd backend
python -m uvicorn app.main:app --reload
```

后端将在 http://localhost:8000 启动

### 5. 启动前端

```bash
cd frontend
npm run dev
```

前端将在 http://localhost:3000 启动

## API文档

启动后端后，访问 http://localhost:8000/docs 查看Swagger API文档。

### 主要接口

- `POST /api/chat` - 法律咨询
- `GET /api/search` - 直接搜索向量库

## 项目结构

```
legal-agent/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── agents/            # Agent实现
│   │   │   ├── legal_consultant.py    # 法律咨询Agent
│   │   │   ├── exam_generator.py      # 出题Agent (待实现)
│   │   │   └── chat_agent.py          # 通用对话Agent (待实现)
│   │   ├── models/            # 数据模型
│   │   │   └── schemas.py     # Pydantic模型定义
│   │   ├── services/          # 核心服务
│   │   │   ├── llm_service.py         # LLM API服务
│   │   │   ├── embedding_service.py  # 文本嵌入服务
│   │   │   ├── vector_store.py       # 向量数据库服务
│   │   │   ├── rerank_service.py     # 重排序服务 (待实现)
│   │   │   ├── cache_service.py      # 缓存服务 (待实现)
│   │   │   └── data_loader.py        # 数据加载
│   │   ├── api/               # API路由 (待重构)
│   │   ├── middleware/         # 中间件 (待实现)
│   │   └── main.py            # FastAPI入口
│   ├── tests/                 # 测试文件
│   ├── requirements.txt       # Python依赖
│   └── .env.example          # 环境变量示例
├── frontend/                  # 前端应用
│   ├── app/                   # Next.js页面
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/               # API路由 (待实现)
│   ├── components/            # React组件
│   │   ├── ChatInterface.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── CitationPanel.tsx
│   │   └── ui/                # UI组件库
│   ├── lib/                   # 工具函数
│   └── package.json
├── docs/                      # 文档 (待创建)
│   ├── architecture.md        # 架构设计文档
│   ├── api.md                 # API文档
│   └── deployment.md          # 部署文档
├── docker/                    # Docker配置 (待创建)
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── README.md                  # 项目说明
```

## 许可证

MIT License

