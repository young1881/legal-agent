"""
简单的API测试脚本
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_chat():
    """测试聊天接口"""
    print("测试聊天接口...")
    data = {
        "message": "什么是正当防卫？",
        "agent_type": "consultant"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"回答: {result['answer']}")
        print(f"引用数量: {len(result.get('citations', []))}")
        if result.get('citations'):
            print("引用:")
            for citation in result['citations']:
                print(f"  - {citation['article_name']} {citation.get('section', '')}")
    else:
        print(f"错误: {response.text}")
    print()

def test_search():
    """测试搜索接口"""
    print("测试搜索接口...")
    params = {"query": "故意杀人", "top_k": 3}
    response = requests.get(f"{BASE_URL}/api/search", params=params)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"查询: {result['query']}")
        print(f"结果数量: {len(result['results'])}")
        for i, r in enumerate(result['results'], 1):
            print(f"  {i}. {r['article_name']} {r.get('section', '')} (相似度: {r.get('score', 0):.3f})")
    else:
        print(f"错误: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("法学AI-Agent API 测试")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_search()
        test_chat()
        print("所有测试完成！")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务")
        print("请确保后端服务正在运行: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"错误: {e}")

