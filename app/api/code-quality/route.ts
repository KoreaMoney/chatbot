import { NextResponse } from 'next/server'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'

const CONFIG_FILE = 'code_quality_config.json'

const getConfigPath = () => join(process.cwd(), CONFIG_FILE)

const readConfig = async (): Promise<{ enabled: boolean }> => {
  try {
    const content = await readFile(getConfigPath(), 'utf-8')
    const data = JSON.parse(content) as { enabled?: boolean }
    return { enabled: data.enabled !== false }
  } catch (e: unknown) {
    if (e && typeof e === 'object' && 'code' in e && (e as { code: string }).code === 'ENOENT') {
      return { enabled: true }
    }
    return { enabled: true }
  }
}

export async function GET() {
  try {
    const projectRoot = process.cwd()
    const historyFile = join(projectRoot, 'code_quality_history.json')
    const config = await readConfig()

    let history: unknown[] = []
    try {
      const fileContent = await readFile(historyFile, 'utf-8')
      const parsed = JSON.parse(fileContent)
      history = Array.isArray(parsed) ? parsed : []
    } catch (fileError: unknown) {
      if (fileError && typeof fileError === 'object' && 'code' in fileError && (fileError as { code: string }).code === 'ENOENT') {
        // history 없음 → 빈 배열
      } else {
        throw fileError
      }
    }

    return NextResponse.json({
      history,
      enabled: config.enabled,
      success: true,
    })
  } catch (error) {
    console.error('코드 품질 히스토리 조회 오류:', error)
    return NextResponse.json(
      { error: '코드 품질 히스토리를 가져올 수 없습니다.', history: [], enabled: true },
      { status: 500 }
    )
  }
}

export async function PATCH(request: Request) {
  try {
    const body = (await request.json()) as { enabled?: boolean }
    const enabled = body.enabled === true

    await writeFile(
      getConfigPath(),
      JSON.stringify({ enabled }, null, 2),
      'utf-8'
    )

    return NextResponse.json({ enabled, success: true })
  } catch (error) {
    console.error('코드 품질 설정 업데이트 오류:', error)
    return NextResponse.json(
      { error: '코드 품질 설정을 업데이트할 수 없습니다.' },
      { status: 500 }
    )
  }
}
