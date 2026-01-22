"""고객센터 오케스트레이터 노드 - 고객센터 내부 오케스트레이터를 정의합니다."""

import os
from typing import Literal

from langchain_core.messages import HumanMessage


def create_customer_service_orchestrator_node():
    """고객센터 오케스트레이터 노드를 생성합니다."""

    def customer_service_orchestrator_node(state: dict):
        """고객센터 오케스트레이터 노드 - 고객센터 요청을 분석하고 적절한 워커로 라우팅합니다.
        
        Args:
            state: 에이전트 상태
            
        Returns:
            customer_service_next_node 필드가 포함된 상태 업데이트
        """
        messages = state.get("messages", [])
        
        if not messages:
            return {"customer_service_next_node": "general_customer_service"}
        
        # 마지막 사용자 메시지 가져오기
        last_message = messages[-1]
        if not isinstance(last_message, HumanMessage):
            return {"customer_service_next_node": "general_customer_service"}
        
        # content가 문자열인지 확인 (리스트일 수 있음)
        message_content = last_message.content
        if isinstance(message_content, list):
            # 리스트인 경우 첫 번째 요소를 사용하거나 문자열로 변환
            content = str(message_content[0] if message_content else "").lower()
        else:
            content = str(message_content).lower()
        
        # 호텔 관련 키워드
        hotel_keywords = [
            "호텔", "객실", "체크인", "체크아웃", "투숙", "숙박",
            "룸", "스위트", "디럭스", "트윈", "더블"
        ]
        
        # 병원 관련 키워드
        hospital_keywords = [
            "병원", "진료", "내과", "외과", "정형외과", "산부인과", "소아과",
            "이비인후과", "안과", "치과", "피부과", "정신건강의학과",
            "의사", "진단", "처방"
        ]
        
        # 헤어샵 관련 키워드
        hair_salon_keywords = [
            "헤어", "미용", "컷트", "펌", "염색", "클리닉", "스타일링",
            "파마", "컬러", "드라이"
        ]
        
        # 예약 관리 관련 키워드
        booking_keywords = [
            "예약번호", "예약 번호", "예약상태", "예약 상태",
            "예약 조회", "예약 취소", "예약 변경", "예약 확인",
            "예약", "예약하기", "예약 진행", "예약 생성", "예약 등록",
            "예약해줘", "예약해주세요", "예약하고 싶어", "예약하려고"
        ]
        
        # 라우팅 결정
        if any(keyword in content for keyword in hotel_keywords):
            return {"customer_service_next_node": "hotel_worker"}
        elif any(keyword in content for keyword in hospital_keywords):
            return {"customer_service_next_node": "hospital_worker"}
        elif any(keyword in content for keyword in hair_salon_keywords):
            return {"customer_service_next_node": "hair_salon_worker"}
        elif any(keyword in content for keyword in booking_keywords):
            return {"customer_service_next_node": "booking_worker"}
        
        return {"customer_service_next_node": "general_customer_service"}

    return customer_service_orchestrator_node


def route_from_customer_service_orchestrator(state: dict) -> Literal[
    "hotel_worker", "hospital_worker", "hair_salon_worker", 
    "booking_worker", "general_customer_service"
]:
    """고객센터 오케스트레이터의 결정에 따라 적절한 워커로 라우팅합니다.
    
    Args:
        state: 에이전트 상태
        
    Returns:
        라우팅할 워커 노드 이름
    """
    next_node = state.get("customer_service_next_node", "general_customer_service")
    return next_node


# 전역 고객센터 오케스트레이터 노드 인스턴스
_customer_service_orchestrator_node_func = None


def customer_service_orchestrator_node(state: dict):
    """고객센터 오케스트레이터 노드 래퍼 함수."""
    global _customer_service_orchestrator_node_func
    if _customer_service_orchestrator_node_func is None:
        _customer_service_orchestrator_node_func = create_customer_service_orchestrator_node()
    return _customer_service_orchestrator_node_func(state)
