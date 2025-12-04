from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.models.schemas import ChatRequest, ChatResponse
from app.agents.legal_consultant import LegalConsultantAgent
from app.services.vector_store import VectorStore
from app.services.data_loader import load_sample_data
import uvicorn

# 全局变量
consultant_agent = None
vector_store = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    global consultant_agent, vector_store
    print("正在初始化服务...")
    vector_store = VectorStore()
    print("正在加载测试数据...")
    load_sample_data(vector_store)
    print("测试数据加载完成")
    # 使用已加载数据的vector_store创建agent
    consultant_agent = LegalConsultantAgent(vector_store=vector_store)
    yield
    # 关闭时（如果需要清理资源）

app = FastAPI(
    title="法学AI-Agent API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "法学AI-Agent API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """法律咨询接口"""
    try:
        if consultant_agent is None:
            raise HTTPException(status_code=503, detail="服务未初始化完成")
        if request.agent_type == "consultant":
            response = await consultant_agent.process_query(request.message)
            return response
        else:
            # 其他Agent类型可以在这里扩展
            raise HTTPException(status_code=400, detail=f"不支持的Agent类型: {request.agent_type}")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"API错误详情:\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/search")
async def search(query: str, top_k: int = 5):
    """直接搜索向量库"""
    if vector_store is None:
        raise HTTPException(status_code=503, detail="服务未初始化完成")
    results = vector_store.search(query, top_k=top_k)
    return {"query": query, "results": results, "count": len(results)}

@app.get("/api/debug/collection-info")
async def collection_info():
    """调试接口：查看向量库信息"""
    if vector_store is None:
        raise HTTPException(status_code=503, detail="服务未初始化完成")
    try:
        collection_info = vector_store.client.get_collection(vector_store.collection_name)
        return {
            "collection_name": vector_store.collection_name,
            "points_count": collection_info.points_count,
            "vectors_count": collection_info.vectors_count,
            "status": "ok"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

