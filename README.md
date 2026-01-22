# LangGraph Agent Test

LangGraph와 LangChain 최신 버전을 사용한 AI 에이전트 테스트 웹 애플리케이션입니다.
**LangGraph 공식 Agent Chat UI**를 사용합니다.

## 프로젝트 구조

```
agent-test/
├── agents/          # 에이전트 모듈
│   ├── __init__.py
│   ├── agent.py     # LangGraph 에이전트 구현
│   └── server.py    # LangGraph 서버 엔트리포인트
├── nodes/           # 노드 모듈
│   ├── __init__.py
│   └── agent_nodes.py  # LangGraph 노드 정의
├── prompts/         # 프롬프트 모듈
│   ├── __init__.py
│   └── agent_prompts.py  # 에이전트 프롬프트 템플릿
├── tools/           # 도구 모듈
│   ├── __init__.py
│   ├── calculator_tool.py  # 계산기 도구
│   └── web_search_tool.py  # 웹 검색 도구
├── app/             # Next.js 프론트엔드
│   ├── globals.css  # 전역 스타일
│   ├── layout.tsx   # 레이아웃 컴포넌트
│   └── page.tsx     # Chat UI 메인 페이지
├── langgraph.json   # LangGraph 서버 설정
├── package.json     # Node.js 의존성
├── tsconfig.json    # TypeScript 설정
├── tailwind.config.js  # TailwindCSS 설정
├── next.config.js   # Next.js 설정
├── run_server.sh    # 서버 실행 스크립트
├── check_env.py     # 환경 변수 확인 스크립트
├── ENV_GUIDE.md     # 환경 변수 가이드
├── LANGSMITH_SETUP.md  # LangSmith 설정 가이드
└── pyproject.toml   # 프로젝트 설정
```

## 설치 및 실행

### 1. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# .env 파일 생성
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
```

환경 변수 설정 확인:
```bash
uv run python check_env.py
```

#### LangSmith 설정 (선택사항, 추천)

LangSmith를 사용하면 에이전트 실행을 추적하고 모니터링할 수 있습니다:

```bash
# .env 파일에 LangSmith 설정 추가
cat >> .env << EOF
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=agent-test
LANGCHAIN_TRACING_V2=true
EOF
```

자세한 설정 방법은 [LANGSMITH_SETUP.md](./LANGSMITH_SETUP.md)를 참고하세요.

### 2. LangGraph 서버 실행

```bash
# uv를 사용하여 LangGraph 서버 실행
uv run langgraph dev

# 또는 직접 실행
langgraph dev
```

서버는 기본적으로 `http://localhost:2024`에서 실행됩니다.

### 3. Agent Chat UI 설치 및 실행

#### 방법 1: 프로젝트 내장 UI 사용 (권장)

프로젝트에 Next.js 기반 Chat UI가 포함되어 있습니다:

**bun 설치 (아직 설치하지 않은 경우):**
```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# 또는 Homebrew 사용
brew install bun
```

**의존성 설치 및 실행:**
```bash
# bun으로 의존성 설치
bun install

# 개발 서버 실행
bun run dev
```

브라우저에서 `http://localhost:3000`에 접속하면 Chat UI를 사용할 수 있습니다.

#### 방법 2: 호스팅 버전 사용

1. [Agent Chat UI](https://chat.langchain.com/)에 접속
2. 다음 정보를 입력:
   - **Graph ID**: `agent`
   - **Deployment URL**: `http://localhost:2024`
   - **LangSmith API key** (선택사항): 로컬 서버 사용 시 불필요

#### 방법 3: 별도 로컬 설치

```bash
# Agent Chat UI 프로젝트 생성
npx create-agent-chat-app --project-name agent-chat-ui
cd agent-chat-ui

# 의존성 설치 및 실행
pnpm install
pnpm dev
```

로컬 Agent Chat UI를 실행한 후:
1. **Graph ID**: `agent` 입력
2. **Deployment URL**: `http://localhost:2024` 입력
3. **LangSmith API key**: 비워두기 (로컬 서버 사용 시)

### 4. 사용하기

Agent Chat UI에서 에이전트와 대화할 수 있습니다:
- "2 + 2를 계산해줘"
- "10 * 5는 얼마야?"
- "파이썬에 대해 검색해줘"

도구 호출과 결과가 자동으로 시각화됩니다.

## 기능

- **계산기 도구**: 수학 표현식을 계산합니다
- **웹 검색 도구**: 웹에서 정보를 검색합니다 (시뮬레이션)
- **LangGraph 기반 에이전트**: 도구를 사용하여 사용자 질문에 답변합니다
- **Agent Chat UI**: LangGraph 공식 UI로 실시간 채팅, 도구 시각화, 타임트래블 디버깅 지원

## 기술 스택

### 백엔드
- **LangChain**: LLM 애플리케이션 프레임워크
- **LangGraph**: 상태 기반 멀티 에이전트 워크플로우
- **OpenAI**: LLM 모델 (gpt-4o-mini)
- **uv**: Python 패키지 관리자

### 프론트엔드
- **Next.js**: React 프레임워크
- **TypeScript**: 타입 안정성
- **TailwindCSS**: 유틸리티 기반 CSS 프레임워크
- **React**: UI 라이브러리

## LangSmith 모니터링

LangSmith를 설정하면:
- 에이전트 실행 추적 및 시각화
- LLM 호출 및 도구 사용 모니터링
- 에러 및 성능 분석
- LangGraph Studio에서 그래프 디버깅

자세한 내용은 [LANGSMITH_SETUP.md](./LANGSMITH_SETUP.md)를 참고하세요.

## 참고 자료

- [LangGraph Agent Chat UI 문서](https://docs.langchain.com/oss/python/langgraph/ui)
- [LangGraph 문서](https://docs.langchain.com/oss/python/langgraph)
- [LangSmith 문서](https://docs.smith.langchain.com/)
