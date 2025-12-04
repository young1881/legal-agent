# 故障排查指南

## 问题：搜索返回"未找到相关信息"

### 可能原因1: Embedding模型下载失败

**症状：**
- 启动时看到连接huggingface.co失败的错误
- 终端显示模型下载重试

**解决方案：**

1. **使用本地已下载的模型**
   - 如果之前下载过模型，系统会自动使用
   - 模型通常存储在 `~/.cache/huggingface/` 目录

2. **手动下载模型（如果有网络）**
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

3. **使用代理或镜像**
   - 设置环境变量：
     ```bash
     export HF_ENDPOINT=https://hf-mirror.com
     ```

4. **检查网络连接**
   - 确保可以访问 huggingface.co
   - 或者使用VPN/代理

### 可能原因2: 数据未成功加载到向量库

**检查方法：**

1. **访问调试接口**
   ```
   http://localhost:8000/api/debug/collection-info
   ```
   应该返回 `points_count > 0`

2. **查看启动日志**
   - 应该看到 "成功添加 X 个文档到向量库"
   - 如果看到错误，检查embedding服务是否正常

3. **测试搜索接口**
   ```
   http://localhost:8000/api/search?query=故意杀人
   ```
   应该返回结果列表

### 可能原因3: Qdrant连接问题

**症状：**
- 看到 "警告: 无法连接到Qdrant"
- 系统使用内存模式

**解决方案：**

1. **内存模式也可以工作**，但需要确保：
   - Embedding模型成功加载
   - 数据成功添加到向量库

2. **如果使用Docker Qdrant：**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

### 诊断步骤

1. **检查服务状态**
   ```bash
   curl http://localhost:8000/health
   ```

2. **检查向量库信息**
   ```bash
   curl http://localhost:8000/api/debug/collection-info
   ```

3. **测试搜索**
   ```bash
   curl "http://localhost:8000/api/search?query=故意杀人"
   ```

4. **查看后端日志**
   - 启动时应该看到：
     - "Embedding模型加载成功"
     - "成功添加 X 个文档到向量库"
     - "向量库中共有 X 个文档"

### 常见错误

1. **"所有embedding模型加载失败"**
   - 解决：检查网络，或手动下载模型

2. **"向量库为空"**
   - 解决：检查数据加载日志，确保embedding服务正常

3. **"搜索返回0个结果"**
   - 可能：查询与知识库内容不匹配
   - 尝试：使用更通用的关键词

### 快速测试

运行测试脚本：
```bash
cd backend
python test_api.py
```

应该看到：
- 健康检查通过
- 搜索返回结果
- 聊天接口正常工作

