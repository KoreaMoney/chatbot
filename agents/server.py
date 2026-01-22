"""LangGraph 서버용 엔트리포인트."""

from agents.agent import create_agent_graph

# LangGraph 서버가 인식할 수 있도록 graph 변수로 export
graph = create_agent_graph()
