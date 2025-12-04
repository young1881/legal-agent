# 环境变量配置说明

在 `backend` 目录下创建 `.env` 文件，包含以下配置：

```env
# API Configuration
SJTU_API_KEY=your-api-key
SJTU_API_URL=https://models.sjtu.edu.cn/api/v1
MODEL_NAME=deepseek-v3

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=legal_documents

# Embedding Model
EMBEDDING_MODEL=bge-m3
```

## 配置说明

### 必需配置

- **SJTU_API_KEY**: 你的上海交通大学模型API密钥
  - 从API提供方获取
  - 这是唯一必需修改的配置

### 可选配置

- **SJTU_API_URL**: API地址（默认已配置）
- **MODEL_NAME**: 使用的模型名称（默认：deepseek-v3）
- **QDRANT_HOST**: Qdrant主机地址（默认：localhost）
- **QDRANT_PORT**: Qdrant端口（默认：6333）
- **QDRANT_COLLECTION_NAME**: 集合名称（默认：legal_documents）
- **EMBEDDING_MODEL**: 嵌入模型名称（默认：bge-m3）

## 注意事项

1. 如果未安装Qdrant，系统会自动使用内存模式
2. 内存模式的数据在重启后会丢失，仅用于测试
3. 生产环境建议使用Docker运行Qdrant

