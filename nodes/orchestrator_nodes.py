"""오케스트레이터 노드 - 중앙 오케스트레이터를 정의합니다."""

import json
import os
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from prompts.orchestrator_prompts import ORCHESTRATOR_SYSTEM_PROMPT


def create_orchestrator_node():
    """오케스트레이터 노드를 생성합니다."""
    # LLM 초기화
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    def orchestrator_node(state: dict):
        """오케스트레이터 노드 - 사용자 요청을 분석하고 적절한 노드로 라우팅합니다.
        
        Args:
            state: 에이전트 상태
            
        Returns:
            next_node 필드가 포함된 상태 업데이트
        """
        messages = state.get("messages", [])
        
        if not messages:
            return {"next_node": "agent"}
        
        # 마지막 사용자 메시지 가져오기
        last_message = messages[-1]
        if not isinstance(last_message, HumanMessage):
            return {"next_node": "agent"}
        
        # content가 문자열인지 확인 (리스트일 수 있음)
        message_content = last_message.content
        if isinstance(message_content, list):
            # 리스트인 경우 첫 번째 요소를 사용하거나 문자열로 변환
            content = str(message_content[0] if message_content else "").lower()
        else:
            content = str(message_content).lower()
        
        # 고객센터 관련 키워드
        customer_service_keywords = [
            "예약", "호텔", "병원", "헤어", "미용", "레스토랑",
            "예약하기", "예약 취소", "예약 변경", "예약 조회",
            "객실", "체크인", "체크아웃", "투숙",
            "진료", "내과", "외과", "정형외과", "산부인과", "소아과",
            "이비인후과", "안과", "치과", "피부과", "정신건강의학과",
            "컷트", "펌", "염색", "클리닉", "스타일링",
            "예약번호", "예약 번호", "예약상태", "예약 상태",
            "고객센터", "상담", "문의", "취소", "변경", "환불"
        ]
        
        # 키워드 기반 라우팅
        if any(keyword in content for keyword in customer_service_keywords):
            return {"next_node": "customer_service"}
        
        # LLM을 사용한 더 정교한 라우팅 (선택사항)
        # non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        # messages_to_send = [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT)] + non_system_messages
        # 
        # # JSON 형식으로 응답하도록 프롬프트
        # response = llm.invoke(messages_to_send)
        # 
        # # 응답에서 JSON 파싱 시도
        # try:
        #     # 응답 내용에서 JSON 추출
        #     content = response.content
        #     if "{" in content and "}" in content:
        #         json_str = content[content.index("{"):content.rindex("}")+1]
        #         routing = json.loads(json_str)
        #         return {"next_node": routing.get("next_node", "agent")}
        # except:
        #     pass
        
        return {"next_node": "agent"}

    return orchestrator_node


def route_from_orchestrator(state: dict) -> Literal["agent", "customer_service"]:
    """오케스트레이터의 결정에 따라 적절한 노드로 라우팅합니다.
    
    Args:
        state: 에이전트 상태
        
    Returns:
        라우팅할 노드 이름
    """
    next_node = state.get("next_node", "agent")
    return next_node


# 전역 오케스트레이터 노드 인스턴스
_orchestrator_node_func = None


def orchestrator_node(state: dict):
    """오케스트레이터 노드 래퍼 함수."""
    global _orchestrator_node_func
    if _orchestrator_node_func is None:
        _orchestrator_node_func = create_orchestrator_node()
    return _orchestrator_node_func(state)
