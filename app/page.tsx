'use client'

import { useState, useRef, useEffect } from 'react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  toolCalls?: Array<{
    name: string
    args: Record<string, unknown>
    result?: string
  }>
}

const DEPLOYMENT_URL = process.env.NEXT_PUBLIC_DEPLOYMENT_URL || 'http://localhost:2024'
const GRAPH_ID = 'agent'

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // 스레드 생성 또는 기존 스레드 사용
      let threadId = sessionStorage.getItem('thread_id')
      
      if (!threadId) {
        const threadResponse = await fetch(`${DEPLOYMENT_URL}/threads`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            graph_id: GRAPH_ID,
          }),
        })

        if (!threadResponse.ok) {
          throw new Error('스레드 생성 실패')
        }

        const { thread_id } = await threadResponse.json()
        threadId = thread_id
        sessionStorage.setItem('thread_id', threadId)
      }

      // 스트리밍 요청
      const streamResponse = await fetch(
        `${DEPLOYMENT_URL}/threads/${threadId}/runs/stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            assistant_id: GRAPH_ID,
            input: {
              messages: [
                {
                  role: 'user',
                  content: userMessage.content,
                },
              ],
            },
            stream_mode: 'events',
          }),
        }
      )

      if (!streamResponse.ok) {
        const errorText = await streamResponse.text()
        throw new Error(`스트림 요청 실패: ${errorText}`)
      }

      const reader = streamResponse.body?.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      let assistantContent = ''
      let toolCalls: Message['toolCalls'] = []
      let assistantMessageAdded = false

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (line.trim() === '') continue
            
            if (line.startsWith('data: ')) {
              try {
                const jsonStr = line.slice(6).trim()
                if (jsonStr === '[DONE]') continue
                
                const data = JSON.parse(jsonStr)
                
                // 채팅 모델 스트림 이벤트
                if (data.event === 'on_chat_model_stream' || data.event === 'on_chain_stream') {
                  const content = data.data?.chunk?.content || data.data?.chunk?.text
                  if (content) {
                    assistantContent += content
                    
                    if (!assistantMessageAdded) {
                      setMessages((prev) => [
                        ...prev,
                        {
                          role: 'assistant',
                          content: assistantContent,
                          toolCalls: toolCalls.length > 0 ? toolCalls : undefined,
                        },
                      ])
                      assistantMessageAdded = true
                    } else {
                      setMessages((prev) => {
                        const newMessages = [...prev]
                        const lastMessage = newMessages[newMessages.length - 1]
                        if (lastMessage?.role === 'assistant') {
                          lastMessage.content = assistantContent
                          lastMessage.toolCalls = toolCalls.length > 0 ? toolCalls : undefined
                        }
                        return newMessages
                      })
                    }
                  }
                }
                // 도구 시작 이벤트
                else if (data.event === 'on_tool_start') {
                  const toolCall = {
                    name: data.data?.name || data.name || 'unknown',
                    args: data.data?.input || data.input || {},
                    result: undefined,
                  }
                  toolCalls.push(toolCall)
                }
                // 도구 종료 이벤트
                else if (data.event === 'on_tool_end') {
                  const toolName = data.data?.name || data.name
                  const toolResult = data.data?.output || data.output
                  const toolCall = toolCalls.find((tc) => tc.name === toolName)
                  if (toolCall) {
                    toolCall.result = typeof toolResult === 'string' 
                      ? toolResult 
                      : JSON.stringify(toolResult, null, 2)
                  }
                }
              } catch (err) {
                console.error('JSON 파싱 오류:', err, line)
              }
            }
          }
        }
      }

      // 최종 메시지 업데이트
      if (assistantContent || toolCalls.length > 0) {
        setMessages((prev) => {
          const newMessages = [...prev]
          const lastMessage = newMessages[newMessages.length - 1]
          if (lastMessage?.role === 'assistant') {
            lastMessage.content = assistantContent || '응답을 생성했습니다.'
            lastMessage.toolCalls = toolCalls.length > 0 ? toolCalls : undefined
          } else if (assistantContent || toolCalls.length > 0) {
            newMessages.push({
              role: 'assistant',
              content: assistantContent || '응답을 생성했습니다.',
              toolCalls: toolCalls.length > 0 ? toolCalls : undefined,
            })
          }
          return newMessages
        })
      }
    } catch (error) {
      console.error('에러:', error)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `오류가 발생했습니다: ${error instanceof Error ? error.message : '알 수 없는 오류'}`,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Agent Chat UI
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            LangGraph Agent와 대화하세요
          </p>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto max-w-4xl w-full mx-auto px-4 py-6">
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500 dark:text-gray-400 text-lg">
                안녕하세요! 무엇을 도와드릴까요?
              </p>
              <p className="text-gray-400 dark:text-gray-500 text-sm mt-2">
                예: "2 + 2를 계산해줘", "10 * 5는 얼마야?", "파이썬에 대해 검색해줘"
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700'
                }`}
              >
                <div className="whitespace-pre-wrap break-words">
                  {message.content}
                </div>
                {message.toolCalls && message.toolCalls.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs font-semibold mb-2 text-gray-600 dark:text-gray-400">
                      사용된 도구:
                    </p>
                    {message.toolCalls.map((toolCall, toolIndex) => (
                      <div
                        key={toolIndex}
                        className="text-xs bg-gray-100 dark:bg-gray-700 rounded p-2 mb-2"
                      >
                        <p className="font-mono font-semibold">
                          {toolCall.name}
                        </p>
                        {toolCall.args && (
                          <p className="text-gray-600 dark:text-gray-300 mt-1">
                            입력: {JSON.stringify(toolCall.args, null, 2)}
                          </p>
                        )}
                        {toolCall.result && (
                          <p className="text-gray-600 dark:text-gray-300 mt-1">
                            결과: {toolCall.result}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white dark:bg-gray-800 rounded-lg px-4 py-3 border border-gray-200 dark:border-gray-700">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="메시지를 입력하세요... (Enter로 전송, Shift+Enter로 줄바꿈)"
              className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white resize-none"
              rows={1}
              disabled={isLoading}
              aria-label="메시지 입력"
              tabIndex={0}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              aria-label="메시지 전송"
              tabIndex={0}
            >
              전송
            </button>
          </form>
        </div>
      </footer>
    </div>
  )
}
