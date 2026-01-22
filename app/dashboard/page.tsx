'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface DashboardStats {
  totalConversations: number
  activeSessions: number
  toolsUsed: number
  totalMessages: number
}

interface ToolUsage {
  name: string
  count: number
  percentage: number
}

interface RecentActivity {
  id: string
  timestamp: string
  action: string
  tool?: string
  status: 'success' | 'error' | 'pending'
}

interface TokenInfo {
  openai: {
    configured: boolean
    prefix: string | null
    type: string
  }
  langsmith: {
    configured: boolean
    prefix: string | null
    project: string
    tracingEnabled: boolean
    type: string
  }
}

interface TokenUsage {
  totalPromptTokens: number
  totalCompletionTokens: number
  totalTokens: number
  requestCount: number
  lastUpdated: string
}

interface CodeQualityCheck {
  timestamp: string
  result: string
  type_check_passed: boolean
  tests_passed: boolean
  has_errors: boolean
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalConversations: 0,
    activeSessions: 0,
    toolsUsed: 0,
    totalMessages: 0,
  })

  const [toolUsage, setToolUsage] = useState<ToolUsage[]>([])
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([])
  const [tokenInfo, setTokenInfo] = useState<TokenInfo | null>(null)
  const [tokenUsage, setTokenUsage] = useState<TokenUsage | null>(null)
  const [codeQualityHistory, setCodeQualityHistory] = useState<CodeQualityCheck[]>([])
  const [codeQualityEnabled, setCodeQualityEnabled] = useState<boolean>(true)
  const [codeQualityToggling, setCodeQualityToggling] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // 토큰 정보 로드
    const loadTokenInfo = async () => {
      try {
        const response = await fetch('/api/tokens')
        if (response.ok) {
          const data = await response.json()
          setTokenInfo(data.tokens)
        }
      } catch (error) {
        console.error('토큰 정보 로드 오류:', error)
      }
    }

    // 코드 품질 히스토리 및 설정 로드
    const loadCodeQualityHistory = async () => {
      try {
        const response = await fetch('/api/code-quality')
        if (response.ok) {
          const data = await response.json()
          setCodeQualityHistory(data.history || [])
          if (typeof data.enabled === 'boolean') {
            setCodeQualityEnabled(data.enabled)
          }
        }
      } catch (error) {
        console.error('코드 품질 히스토리 로드 오류:', error)
      }
    }

    // 대시보드 데이터 로드
    const loadDashboardData = () => {
      try {
        // sessionStorage에서 thread_id 확인하여 활성 세션 계산
        const threadId = sessionStorage.getItem('thread_id')
        const activeSessions = threadId ? 1 : 0

        // localStorage에서 통계 데이터 가져오기 (있는 경우)
        const storedStats = localStorage.getItem('dashboard_stats')
        const storedToolUsage = localStorage.getItem('tool_usage')
        const storedActivities = localStorage.getItem('recent_activities')

        if (storedStats) {
          const parsedStats = JSON.parse(storedStats)
          setStats({
            ...parsedStats,
            activeSessions,
          })
        } else {
          // 기본 샘플 데이터
          setStats({
            totalConversations: 12,
            activeSessions,
            toolsUsed: 45,
            totalMessages: 128,
          })
        }

        if (storedToolUsage) {
          setToolUsage(JSON.parse(storedToolUsage))
        } else {
          // 기본 샘플 데이터
          setToolUsage([
            { name: 'calculator_tool', count: 15, percentage: 33.3 },
            { name: 'web_search_tool', count: 12, percentage: 26.7 },
            { name: 'date_time_tool', count: 8, percentage: 17.8 },
            { name: 'json_tool', count: 6, percentage: 13.3 },
            { name: 'string_utils_tool', count: 4, percentage: 8.9 },
          ])
        }

        if (storedActivities) {
          setRecentActivities(JSON.parse(storedActivities))
        } else {
          // 기본 샘플 데이터
          setRecentActivities([
            {
              id: '1',
              timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
              action: '계산기 도구 사용',
              tool: 'calculator_tool',
              status: 'success',
            },
            {
              id: '2',
              timestamp: new Date(Date.now() - 12 * 60000).toISOString(),
              action: '웹 검색 실행',
              tool: 'web_search_tool',
              status: 'success',
            },
            {
              id: '3',
              timestamp: new Date(Date.now() - 25 * 60000).toISOString(),
              action: '날짜 변환',
              tool: 'date_time_tool',
              status: 'success',
            },
            {
              id: '4',
              timestamp: new Date(Date.now() - 45 * 60000).toISOString(),
              action: 'JSON 파싱',
              tool: 'json_tool',
              status: 'success',
            },
            {
              id: '5',
              timestamp: new Date(Date.now() - 60 * 60000).toISOString(),
              action: '문자열 변환',
              tool: 'string_utils_tool',
              status: 'success',
            },
          ])
        }

        // 토큰 사용량 로드
        const storedTokenUsage = localStorage.getItem('token_usage')
        if (storedTokenUsage) {
          setTokenUsage(JSON.parse(storedTokenUsage))
        }
      } catch (error) {
        console.error('대시보드 데이터 로드 오류:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadTokenInfo()
    loadCodeQualityHistory()
    loadDashboardData()

    // 주기적으로 활성 세션, 토큰 사용량, 코드 품질 히스토리 업데이트
    const interval = setInterval(() => {
      const threadId = sessionStorage.getItem('thread_id')
      setStats((prev) => ({
        ...prev,
        activeSessions: threadId ? 1 : 0,
      }))
      
      // 토큰 사용량 업데이트
      const storedTokenUsage = localStorage.getItem('token_usage')
      if (storedTokenUsage) {
        setTokenUsage(JSON.parse(storedTokenUsage))
      }

      // 코드 품질 히스토리 업데이트
      loadCodeQualityHistory()
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const formatTimeAgo = (timestamp: string): string => {
    const now = new Date()
    const time = new Date(timestamp)
    const diffInSeconds = Math.floor((now.getTime() - time.getTime()) / 1000)

    if (diffInSeconds < 60) {
      return `${diffInSeconds}초 전`
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60)
      return `${minutes}분 전`
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600)
      return `${hours}시간 전`
    } else {
      const days = Math.floor(diffInSeconds / 86400)
      return `${days}일 전`
    }
  }

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'success':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'error':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }

  const getStatusText = (status: string): string => {
    switch (status) {
      case 'success':
        return '성공'
      case 'error':
        return '오류'
      case 'pending':
        return '대기중'
      default:
        return '알 수 없음'
    }
  }

  const handleCodeQualityToggle = async () => {
    if (codeQualityToggling) return
    const next = !codeQualityEnabled
    setCodeQualityToggling(true)
    try {
      const response = await fetch('/api/code-quality', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: next }),
      })
      if (response.ok) {
        const data = (await response.json()) as { enabled: boolean }
        setCodeQualityEnabled(data.enabled)
      }
    } catch (error) {
      console.error('코드 품질 설정 변경 오류:', error)
    } finally {
      setCodeQualityToggling(false)
    }
  }

  const handleCodeQualityToggleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleCodeQualityToggle()
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">로딩 중...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                대시보드
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Agent 시스템 통계 및 모니터링
              </p>
            </div>
            <Link
              href="/"
              className="px-4 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              aria-label="채팅으로 이동"
              tabIndex={0}
            >
              채팅으로 이동
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 통계 카드 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  총 대화 수
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.totalConversations}
                </p>
              </div>
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
                <svg
                  className="w-6 h-6 text-blue-600 dark:text-blue-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  활성 세션
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.activeSessions}
                </p>
              </div>
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-full">
                <svg
                  className="w-6 h-6 text-green-600 dark:text-green-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  사용된 도구 수
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.toolsUsed}
                </p>
              </div>
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-full">
                <svg
                  className="w-6 h-6 text-purple-600 dark:text-purple-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  총 메시지 수
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.totalMessages}
                </p>
              </div>
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-full">
                <svg
                  className="w-6 h-6 text-orange-600 dark:text-orange-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* 도구 사용 통계 */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                도구 사용 통계
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                가장 많이 사용된 도구들
              </p>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {toolUsage.map((tool, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {tool.name}
                      </span>
                      <span className="text-sm text-gray-500 dark:text-gray-400">
                        {tool.count}회 ({tool.percentage.toFixed(1)}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${tool.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 최근 활동 */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                최근 활동
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                최근 5개 활동 내역
              </p>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-start justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                  >
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {activity.action}
                      </p>
                      {activity.tool && (
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          도구: {activity.tool}
                        </p>
                      )}
                      <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                        {formatTimeAgo(activity.timestamp)}
                      </p>
                    </div>
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                        activity.status
                      )}`}
                    >
                      {getStatusText(activity.status)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 토큰 정보 */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              토큰 정보
            </h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              API 키 설정 상태
            </p>
          </div>
          <div className="p-6">
            {tokenInfo ? (
              <div className="space-y-6">
                {/* OpenAI 토큰 */}
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-full ${
                        tokenInfo.openai.configured
                          ? 'bg-green-100 dark:bg-green-900'
                          : 'bg-red-100 dark:bg-red-900'
                      }`}>
                        <svg
                          className={`w-5 h-5 ${
                            tokenInfo.openai.configured
                              ? 'text-green-600 dark:text-green-400'
                              : 'text-red-600 dark:text-red-400'
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          {tokenInfo.openai.configured ? (
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          ) : (
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          )}
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          OpenAI API Key
                        </h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {tokenInfo.openai.type}
                        </p>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 text-sm font-medium rounded-full ${
                        tokenInfo.openai.configured
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                      }`}
                    >
                      {tokenInfo.openai.configured ? '설정됨' : '설정 안됨'}
                    </span>
                  </div>
                  {tokenInfo.openai.configured && tokenInfo.openai.prefix && (
                    <div className="mt-2">
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        키 앞부분:
                      </p>
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        <span className="font-mono text-xs bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded">
                          {tokenInfo.openai.prefix}
                        </span>
                      </p>
                    </div>
                  )}
                  {/* 토큰 사용량 표시 */}
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-600">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
                      사용량 통계
                    </h4>
                    {tokenUsage && tokenUsage.totalTokens > 0 ? (
                      <>
                        <div className="grid grid-cols-3 gap-3">
                          <div className="bg-white dark:bg-gray-600 rounded p-2">
                            <p className="text-xs text-gray-500 dark:text-gray-400">프롬프트</p>
                            <p className="text-lg font-bold text-gray-900 dark:text-white">
                              {tokenUsage.totalPromptTokens.toLocaleString()}
                            </p>
                          </div>
                          <div className="bg-white dark:bg-gray-600 rounded p-2">
                            <p className="text-xs text-gray-500 dark:text-gray-400">완료</p>
                            <p className="text-lg font-bold text-gray-900 dark:text-white">
                              {tokenUsage.totalCompletionTokens.toLocaleString()}
                            </p>
                          </div>
                          <div className="bg-white dark:bg-gray-600 rounded p-2">
                            <p className="text-xs text-gray-500 dark:text-gray-400">총합</p>
                            <p className="text-lg font-bold text-blue-600 dark:text-blue-400">
                              {tokenUsage.totalTokens.toLocaleString()}
                            </p>
                          </div>
                        </div>
                        <div className="mt-3 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                          <span>요청 수: {tokenUsage.requestCount.toLocaleString()}회</span>
                          <span>
                            마지막 업데이트: {tokenUsage.lastUpdated 
                              ? formatTimeAgo(tokenUsage.lastUpdated) 
                              : '알 수 없음'}
                          </span>
                        </div>
                      </>
                    ) : (
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        아직 토큰 사용량 데이터가 없습니다. 채팅을 시작하면 사용량이 표시됩니다.
                      </p>
                    )}
                  </div>
                </div>

                {/* LangSmith 토큰 */}
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-full ${
                        tokenInfo.langsmith.configured
                          ? 'bg-green-100 dark:bg-green-900'
                          : 'bg-yellow-100 dark:bg-yellow-900'
                      }`}>
                        <svg
                          className={`w-5 h-5 ${
                            tokenInfo.langsmith.configured
                              ? 'text-green-600 dark:text-green-400'
                              : 'text-yellow-600 dark:text-yellow-400'
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          {tokenInfo.langsmith.configured ? (
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          ) : (
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                            />
                          )}
                        </svg>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          LangSmith API Key
                        </h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {tokenInfo.langsmith.type}
                        </p>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 text-sm font-medium rounded-full ${
                        tokenInfo.langsmith.configured
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                      }`}
                    >
                      {tokenInfo.langsmith.configured ? '설정됨' : '미설정'}
                    </span>
                  </div>
                  {tokenInfo.langsmith.configured ? (
                    <div className="mt-3 space-y-2">
                      {tokenInfo.langsmith.prefix && (
                        <div>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                            키 앞부분:
                          </p>
                          <p className="text-sm text-gray-700 dark:text-gray-300">
                            <span className="font-mono text-xs bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded">
                              {tokenInfo.langsmith.prefix}
                            </span>
                          </p>
                        </div>
                      )}
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                          프로젝트:
                        </p>
                        <p className="text-sm text-gray-700 dark:text-gray-300">
                          <span className="font-mono text-xs bg-gray-200 dark:bg-gray-600 px-2 py-1 rounded">
                            {tokenInfo.langsmith.project}
                          </span>
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                          추적 활성화:
                        </p>
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded ${
                            tokenInfo.langsmith.tracingEnabled
                              ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                              : 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-300'
                          }`}
                        >
                          {tokenInfo.langsmith.tracingEnabled ? '활성화' : '비활성화'}
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="mt-2">
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        LangSmith를 사용하려면 LANGSMITH_API_KEY를 설정하세요.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                <p className="mt-4 text-gray-600 dark:text-gray-400">토큰 정보를 불러오는 중...</p>
              </div>
            )}
          </div>
        </div>

        {/* 코드 품질 체크 결과 */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-200 dark:border-gray-700">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                코드 품질 체크 결과
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                타입 체크 및 테스트 실행 히스토리 · {codeQualityEnabled ? '검사 켜짐' : '검사 꺼짐'}
              </p>
            </div>
            <button
              type="button"
              role="switch"
              aria-checked={codeQualityEnabled}
              aria-label={codeQualityEnabled ? '코드 품질 검사 켜짐, 끄려면 클릭' : '코드 품질 검사 꺼짐, 켜려면 클릭'}
              tabIndex={0}
              disabled={codeQualityToggling}
              onClick={handleCodeQualityToggle}
              onKeyDown={handleCodeQualityToggleKeyDown}
              className={`relative inline-flex h-10 w-[5.5rem] shrink-0 cursor-pointer items-center rounded-full border-2 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 ${
                codeQualityEnabled
                  ? 'border-green-500 bg-green-500'
                  : 'border-gray-300 dark:border-gray-600 bg-gray-200 dark:bg-gray-700'
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-9 w-9 shrink-0 transform rounded-full bg-white shadow ring-0 transition-transform ${
                  codeQualityEnabled ? 'translate-x-12' : 'translate-x-1'
                }`}
                aria-hidden
              />
            </button>
          </div>
          <div className="p-6">
            {codeQualityHistory.length > 0 ? (
              <div className="space-y-4">
                {codeQualityHistory.slice(0, 10).map((check, index) => (
                  <div
                    key={index}
                    className={`p-4 rounded-lg border ${
                      check.has_errors
                        ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
                        : 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div
                          className={`p-2 rounded-full ${
                            check.has_errors
                              ? 'bg-red-100 dark:bg-red-900'
                              : 'bg-green-100 dark:bg-green-900'
                          }`}
                        >
                          {check.has_errors ? (
                            <svg
                              className="w-5 h-5 text-red-600 dark:text-red-400"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                              />
                            </svg>
                          ) : (
                            <svg
                              className="w-5 h-5 text-green-600 dark:text-green-400"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                              />
                            </svg>
                          )}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900 dark:text-white">
                            {new Date(check.timestamp).toLocaleString('ko-KR')}
                          </p>
                          <div className="flex items-center gap-3 mt-1">
                            <span
                              className={`px-2 py-1 text-xs font-medium rounded ${
                                check.type_check_passed
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                              }`}
                            >
                              타입 체크: {check.type_check_passed ? '통과' : '실패'}
                            </span>
                            <span
                              className={`px-2 py-1 text-xs font-medium rounded ${
                                check.tests_passed
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                              }`}
                            >
                              테스트: {check.tests_passed ? '통과' : '실패'}
                            </span>
                          </div>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {formatTimeAgo(check.timestamp)}
                      </span>
                    </div>
                    <details className="mt-3">
                      <summary className="cursor-pointer text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                        상세 결과 보기
                      </summary>
                      <div className="mt-3 p-3 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700">
                        <pre className="text-xs text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono overflow-x-auto">
                          {check.result}
                        </pre>
                      </div>
                    </details>
                  </div>
                ))}
                {codeQualityHistory.length > 10 && (
                  <p className="text-sm text-gray-500 dark:text-gray-400 text-center pt-2">
                    최근 10개만 표시됩니다. (총 {codeQualityHistory.length}개)
                  </p>
                )}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <svg
                    className="w-8 h-8 text-gray-400 dark:text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                </div>
                <p className="text-gray-600 dark:text-gray-400">
                  아직 코드 품질 체크 결과가 없습니다.
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                  Agent가 시작되면 자동으로 코드 품질을 검사합니다.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
