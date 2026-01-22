# LangSmith 설정 가이드

LangSmith는 LangChain의 모니터링 및 디버깅 플랫폼입니다. LangGraph와 통합하여 에이전트 실행을 추적하고 시각화할 수 있습니다.

## LangSmith 계정 생성

1. https://smith.langchain.com/ 접속
2. 회원가입 또는 로그인
3. 새 프로젝트 생성 (선택사항, 환경 변수에서 설정 가능)

## API 키 발급

1. LangSmith 대시보드에서 **Settings** > **API Keys** 이동
2. **Create API Key** 클릭
3. 키 이름 입력 (예: "agent-test")
4. 생성된 API 키 복사 (형식: `lsv2_...`)

## 환경 변수 설정

`.env` 파일에 다음 환경 변수를 추가하세요:

```env
# 필수: OpenAI API 키
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# LangSmith 설정 (선택사항이지만 추천)
LANGSMITH_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxx
LANGSMITH_PROJECT=agent-test
LANGCHAIN_TRACING_V2=true
```

### 환경 변수 설명

- **`LANGSMITH_API_KEY`**: LangSmith API 키 (필수, LangSmith 사용 시)
- **`LANGSMITH_PROJECT`**: 프로젝트 이름 (선택사항, 기본값: "default")
- **`LANGCHAIN_TRACING_V2`**: 추적 활성화 여부 (`true` 또는 `false`)

## LangGraph 서버와 통합

LangGraph 서버는 환경 변수를 자동으로 읽어 LangSmith와 통합됩니다. 별도의 코드 수정이 필요 없습니다.

```bash
# .env 파일이 있는 상태에서 서버 실행
uv run langgraph dev
```

## LangSmith Studio 사용

### 1. 대시보드에서 실행 추적 확인

1. https://smith.langchain.com/ 접속
2. 프로젝트 선택 (환경 변수에서 설정한 프로젝트)
3. **Traces** 메뉴에서 실행 기록 확인
4. 각 실행을 클릭하여 상세 정보 확인

### 2. LangGraph Studio에서 그래프 시각화

LangGraph Studio는 LangGraph 그래프를 시각화하고 디버깅할 수 있는 도구입니다.

```bash
# LangGraph Studio 실행
uv run langgraph studio
```

또는 브라우저에서:
1. https://smith.langchain.com/ 접속
2. **LangGraph Studio** 메뉴 선택
3. 로컬 그래프 연결

## Agent Chat UI와 LangSmith 통합

Agent Chat UI에서 LangSmith API 키를 입력하면:
- 실행 추적이 자동으로 LangSmith에 기록됩니다
- 대화 히스토리를 LangSmith에서 확인할 수 있습니다
- 타임트래블 디버깅 기능을 사용할 수 있습니다

### 설정 방법

1. [Agent Chat UI](https://chat.langchain.com/) 접속
2. 연결 설정에서:
   - **Graph ID**: `agent`
   - **Deployment URL**: `http://localhost:2024`
   - **LangSmith API key**: 발급받은 API 키 입력

## 추적 정보 확인

LangSmith에서 확인할 수 있는 정보:
- 각 노드의 실행 시간
- LLM 호출 및 응답
- 도구 호출 및 결과
- 에러 및 예외 정보
- 전체 실행 흐름 그래프

## 문제 해결

### 추적이 작동하지 않는 경우

1. 환경 변수가 올바르게 설정되었는지 확인:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('LANGSMITH_API_KEY:', '설정됨' if os.getenv('LANGSMITH_API_KEY') else '설정 안됨')"
```

2. `LANGCHAIN_TRACING_V2=true`가 설정되어 있는지 확인

3. LangSmith API 키가 유효한지 확인

4. 네트워크 연결 확인 (LangSmith API 접근 가능 여부)

## 참고 자료

- [LangSmith 문서](https://docs.smith.langchain.com/)
- [LangGraph Studio 가이드](https://docs.langchain.com/oss/python/langgraph/studio)
- [LangChain 추적 설정](https://docs.smith.langchain.com/tracing)
