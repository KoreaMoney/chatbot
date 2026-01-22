# 환경 변수 가이드

## 필수 환경 변수

### `OPENAI_API_KEY` (필수)
- **설명**: OpenAI API 키
- **용도**: LLM 모델(gpt-4o-mini) 호출에 사용
- **발급 방법**: 
  1. https://platform.openai.com/ 접속
  2. API Keys 메뉴에서 새 키 생성
  3. 생성된 키를 복사하여 `.env` 파일에 입력
- **예시**: `OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx`

## 선택적 환경 변수

### `LANGSMITH_API_KEY` (선택사항, 추천)
- **설명**: LangSmith API 키
- **용도**: LangSmith를 통한 로깅, 모니터링, 디버깅
- **언제 사용**: 
  - 에이전트 실행 추적이 필요한 경우
  - LangSmith Studio에서 그래프를 시각화하고 싶은 경우
  - 프로덕션 환경에서 모니터링이 필요한 경우
  - Agent Chat UI에서 타임트래블 디버깅을 사용하고 싶은 경우
- **발급 방법**:
  1. https://smith.langchain.com/ 접속
  2. 회원가입 또는 로그인
  3. Settings > API Keys에서 새 키 생성
  4. 생성된 키 복사 (형식: `lsv2_...`)
- **예시**: `LANGSMITH_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxx`
- **참고**: 자세한 설정 방법은 [LANGSMITH_SETUP.md](./LANGSMITH_SETUP.md) 참고

### `LANGSMITH_PROJECT` (선택사항)
- **설명**: LangSmith 프로젝트 이름
- **용도**: LangSmith에서 실행 로그를 그룹화
- **예시**: `LANGSMITH_PROJECT=agent-test`

### `LANGCHAIN_TRACING_V2` (선택사항)
- **설명**: LangChain 추적 활성화 여부
- **용도**: LangSmith 추적을 활성화
- **값**: `true` 또는 `false`
- **예시**: `LANGCHAIN_TRACING_V2=true`

### `LANGCHAIN_ENDPOINT` (선택사항)
- **설명**: LangSmith 엔드포인트 URL
- **용도**: 커스텀 LangSmith 엔드포인트 사용 시
- **기본값**: `https://api.smith.langchain.com`
- **예시**: `LANGCHAIN_ENDPOINT=https://api.smith.langchain.com`

## 설정 방법

### 1. .env 파일 생성
```bash
cp .env.example .env
```

### 2. .env 파일 편집
```bash
# 텍스트 에디터로 .env 파일 열기
nano .env
# 또는
vim .env
```

### 3. 필수 값 입력
최소한 `OPENAI_API_KEY`는 반드시 설정해야 합니다:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
```

### 4. 선택적 값 입력 (원하는 경우)
LangSmith를 사용하려면:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
LANGSMITH_API_KEY=lsv2_xxxxxxxxxxxxxxxxxxxxx
LANGSMITH_PROJECT=agent-test
LANGCHAIN_TRACING_V2=true
```

## 확인 방법

환경 변수가 제대로 로드되었는지 확인:
```bash
# Python에서 확인
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OPENAI_API_KEY:', '설정됨' if os.getenv('OPENAI_API_KEY') else '설정 안됨')"
```

## 보안 주의사항

⚠️ **중요**: 
- `.env` 파일은 절대 Git에 커밋하지 마세요
- `.gitignore`에 `.env`가 포함되어 있는지 확인하세요
- API 키를 코드에 하드코딩하지 마세요
- 프로덕션 환경에서는 환경 변수 관리 시스템을 사용하세요
