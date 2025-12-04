"""
快速诊断脚本 - 检查系统状态
"""
import sys
import os

def check_imports():
    """检查必要的包是否安装"""
    print("=" * 50)
    print("1. 检查Python包...")
    print("=" * 50)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'qdrant_client',
        'sentence_transformers',
        'httpx',
        'pydantic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - 未安装")
            missing.append(package)
    
    if missing:
        print(f"\n缺少以下包，请运行: pip install {' '.join(missing)}")
        return False
    return True

def check_embedding_model():
    """检查embedding模型"""
    print("\n" + "=" * 50)
    print("2. 检查Embedding模型...")
    print("=" * 50)
    
    try:
        from sentence_transformers import SentenceTransformer
        models = [
            'paraphrase-multilingual-MiniLM-L12-v2',
            'all-MiniLM-L6-v2',
            'all-MiniLM-L12-v2'
        ]
        
        for model_name in models:
            try:
                print(f"尝试加载: {model_name}...")
                model = SentenceTransformer(model_name)
                print(f"✓ {model_name} 加载成功 ({model.get_sentence_embedding_dimension()}维)")
                return True
            except Exception as e:
                print(f"✗ {model_name} 加载失败: {str(e)[:100]}")
        
        print("\n⚠ 所有模型加载失败，请检查网络连接")
        return False
    except Exception as e:
        print(f"✗ 无法导入SentenceTransformer: {e}")
        return False

def check_qdrant():
    """检查Qdrant连接"""
    print("\n" + "=" * 50)
    print("3. 检查Qdrant连接...")
    print("=" * 50)
    
    try:
        from qdrant_client import QdrantClient
        try:
            client = QdrantClient(host="localhost", port=6333)
            collections = client.get_collections()
            print("✓ Qdrant连接成功 (localhost:6333)")
            return True
        except:
            print("⚠ 无法连接到Qdrant (localhost:6333)，将使用内存模式")
            client = QdrantClient(":memory:")
            print("✓ 内存模式可用")
            return True
    except Exception as e:
        print(f"✗ Qdrant检查失败: {e}")
        return False

def check_env():
    """检查环境变量"""
    print("\n" + "=" * 50)
    print("4. 检查环境变量...")
    print("=" * 50)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("SJTU_API_KEY", "")
    if api_key and api_key != "your-api-key":
        print("✓ SJTU_API_KEY 已配置")
    else:
        print("⚠ SJTU_API_KEY 未配置或使用默认值")
        print("  请在 .env 文件中设置: SJTU_API_KEY=your-api-key")
    
    return True

def main():
    print("\n" + "=" * 50)
    print("法学AI-Agent 系统诊断")
    print("=" * 50 + "\n")
    
    results = []
    results.append(("Python包", check_imports()))
    results.append(("Embedding模型", check_embedding_model()))
    results.append(("Qdrant连接", check_qdrant()))
    results.append(("环境变量", check_env()))
    
    print("\n" + "=" * 50)
    print("诊断结果")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    all_ok = all(r[1] for r in results)
    
    if all_ok:
        print("\n✓ 所有检查通过！系统应该可以正常运行。")
    else:
        print("\n⚠ 部分检查失败，请根据上述提示修复问题。")
        print("\n详细故障排查请参考: backend/TROUBLESHOOTING.md")

if __name__ == "__main__":
    main()

