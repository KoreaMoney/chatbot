#!/usr/bin/env python3
"""환경 변수 설정 확인 스크립트."""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("환경 변수 설정 확인")
print("=" * 50)

# 필수 환경 변수
openai_key = os.getenv("OPENAI_API_KEY")
print(f"\n[필수] OPENAI_API_KEY: {'✓ 설정됨' if openai_key else '✗ 설정 안됨'}")
if openai_key:
    print(f"  키 앞부분: {openai_key[:10]}...")

# LangSmith 환경 변수
langsmith_key = os.getenv("LANGSMITH_API_KEY")
langsmith_project = os.getenv("LANGSMITH_PROJECT", "default")
tracing = os.getenv("LANGCHAIN_TRACING_V2", "false")

print(f"\n[선택] LANGSMITH_API_KEY: {'✓ 설정됨' if langsmith_key else '✗ 설정 안됨'}")
if langsmith_key:
    print(f"  키 앞부분: {langsmith_key[:10]}...")
    print(f"  프로젝트: {langsmith_project}")
    print(f"  추적 활성화: {tracing}")
else:
    print("  LangSmith를 사용하려면 LANGSMITH_API_KEY를 설정하세요.")
    print("  자세한 내용은 LANGSMITH_SETUP.md를 참고하세요.")

print("\n" + "=" * 50)
if openai_key:
    print("✓ 최소 설정 완료 - 서버 실행 가능")
    if langsmith_key:
        print("✓ LangSmith 설정 완료 - 모니터링 활성화")
    else:
        print("ℹ LangSmith 미설정 - 모니터링 비활성화")
else:
    print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
    print("  .env 파일에 OPENAI_API_KEY를 설정하세요.")
print("=" * 50)
