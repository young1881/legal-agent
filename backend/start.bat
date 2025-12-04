@echo off
echo 正在启动法学AI-Agent后端服务...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

