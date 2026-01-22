#!/bin/bash
# LangGraph 서버 실행 스크립트

echo "LangGraph 서버를 시작합니다..."
echo "서버 주소: http://localhost:2024"
echo ""
echo "Agent Chat UI에서 다음 정보를 사용하세요:"
echo "  - Graph ID: agent"
echo "  - Deployment URL: http://localhost:2024"
echo ""

uv run langgraph dev
