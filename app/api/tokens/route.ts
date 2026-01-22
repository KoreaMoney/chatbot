import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // 환경 변수 확인 (서버 사이드에서만 접근 가능)
    const openaiKey = process.env.OPENAI_API_KEY
    const langsmithKey = process.env.LANGSMITH_API_KEY
    const langsmithProject = process.env.LANGSMITH_PROJECT || 'default'
    const tracingEnabled = process.env.LANGCHAIN_TRACING_V2 === 'true'

    return NextResponse.json({
      tokens: {
        openai: {
          configured: !!openaiKey,
          prefix: openaiKey ? `${openaiKey.substring(0, 10)}...` : null,
          type: '필수',
        },
        langsmith: {
          configured: !!langsmithKey,
          prefix: langsmithKey ? `${langsmithKey.substring(0, 10)}...` : null,
          project: langsmithProject,
          tracingEnabled,
          type: '선택',
        },
      },
    })
  } catch (error) {
    console.error('토큰 정보 조회 오류:', error)
    return NextResponse.json(
      { error: '토큰 정보를 가져올 수 없습니다.' },
      { status: 500 }
    )
  }
}
