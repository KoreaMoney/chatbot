"""에이전트 - LangGraph를 사용한 에이전트 구현."""

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from nodes.agent_nodes import agent_node, should_continue
from prompts.agent_prompts import AGENT_SYSTEM_PROMPT
from tools.calculator_tool import CalculatorTool
from tools.web_search_tool import WebSearchTool

load_dotenv()

# 상태 정의
class AgentState(TypedDict):
    """에이전트 상태."""
    messages: Annotated[list[BaseMessage], add_messages]


def create_agent_graph():
    """LangGraph 에이전트 그래프를 생성합니다."""
    # LLM 초기화
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # 도구 바인딩
    tools = [CalculatorTool, WebSearchTool]
    llm_with_tools = llm.bind_tools(tools)
    
    # 그래프 생성
    workflow = StateGraph(AgentState)
    
    # 노드 추가
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))
    
    # 엣지 추가
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "agent")
    
    # 컴파일
    app = workflow.compile()
    return app


