# 快速启动指南

## 前置要求

- Python 3.8+
- Node.js 18+
- (可选) Qdrant Docker 容器

## 步骤 1: 配置后端

```bash
cd backend
pip install -r requirements.txt
```

复制环境变量文件：
```bash
copy .env.example .env  # Windows
# 或
cp .env.example .env    # Linux/Mac
```

编辑 `.env` 文件，填入你的 API Key：
```
SJTU_API_KEY=your-api-key
```

## 步骤 2: 启动后端

### Windows
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Linux/Mac
```bash
cd backend
python -m uvicorn app.main:app --reload
```

或者使用启动脚本：
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

后端将在 http://localhost:8000 启动

## 步骤 3: 配置并启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:3000 启动

## 步骤 4: 测试

1. 打开浏览器访问 http://localhost:3000
2. 尝试提问：
   - "什么是正当防卫？"
   - "故意杀人罪如何量刑？"
   - "不当得利是什么意思？"

## 注意事项

1. **Qdrant 数据库**：
   - 如果未安装 Qdrant，系统会自动使用内存模式
   - 数据在重启后会丢失，仅用于测试
   - 生产环境建议使用 Docker 运行 Qdrant：
     ```bash
     docker run -p 6333:6333 qdrant/qdrant
     ```

2. **Embedding 模型**：
   - 首次运行会自动下载模型（约 400MB）
   - 下载可能需要一些时间

3. **API 调用**：
   - 确保网络可以访问 `https://models.sjtu.edu.cn`
   - 检查 API Key 是否正确

## 故障排查

### 快速诊断
运行诊断脚本：
```bash
cd backend
python diagnose.py
```

### 常见问题

#### 1. 搜索返回"未找到相关信息"
**可能原因：**
- Embedding模型下载失败（网络问题）
- 数据未成功加载到向量库

**解决方法：**
1. 检查启动日志，确认看到"成功添加 X 个文档到向量库"
2. 访问调试接口：`http://localhost:8000/api/debug/collection-info`
3. 查看详细故障排查：`backend/TROUBLESHOOTING.md`

#### 2. Embedding模型下载失败
**症状：** 启动时看到连接huggingface.co失败

**解决方法：**
- 系统会自动尝试多个模型，如果都失败会使用关键词搜索作为fallback
- 如果有网络，可以手动下载模型
- 详细说明见 `backend/TROUBLESHOOTING.md`

#### 3. 后端无法启动
- 检查 Python 版本：`python --version`
- 检查依赖是否安装：`pip list`
- 查看错误日志

#### 4. 前端无法连接后端
- 确认后端在 8000 端口运行
- 检查 CORS 配置
- 查看浏览器控制台错误

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看 Swagger API 文档。

