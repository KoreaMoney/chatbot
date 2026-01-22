"""고객센터 워커 노드들 - 각 서비스별 전문 워커 노드를 정의합니다."""

import os
from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

from prompts.customer_service_prompts import CUSTOMER_SERVICE_SYSTEM_PROMPT
from tools.booking_tool import CreateBookingTool, SearchBookingsTool, CancelBookingTool, ModifyBookingTool
from tools.hotel_tool import SearchHotelsTool, GetHotelRoomTypesTool, CheckHotelAvailabilityTool
from tools.hospital_tool import SearchHospitalsTool, GetDepartmentInfoTool, CheckHospitalAvailabilityTool
from tools.hair_salon_tool import SearchHairSalonsTool, GetHairServiceInfoTool, CheckHairSalonAvailabilityTool
from tools.customer_service_tool import GetBookingStatusTool, GetCustomerBookingsTool, ProvideServiceInfoTool, HandleCustomerInquiryTool


def create_hotel_worker():
    """호텔 워커 노드를 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    hotel_tools = [
        SearchHotelsTool,
        GetHotelRoomTypesTool,
        CheckHotelAvailabilityTool,
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
    ]
    llm_with_tools = llm.bind_tools(hotel_tools)

    def hotel_worker(state: dict):
        """호텔 워커 노드 - 호텔 예약 관련 요청을 처리합니다."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        if not non_system_messages:
            return {"messages": []}

        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        system_prompt = CUSTOMER_SERVICE_SYSTEM_PROMPT + "\n\n당신은 호텔 예약 전문 상담원입니다. 호텔 예약, 객실 조회, 체크인/체크아웃 관련 요청을 처리합니다."
        messages_to_send = [SystemMessage(content=system_prompt)] + valid_messages
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}

    return hotel_worker


def create_hospital_worker():
    """병원 워커 노드를 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    hospital_tools = [
        SearchHospitalsTool,
        GetDepartmentInfoTool,
        CheckHospitalAvailabilityTool,
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
    ]
    llm_with_tools = llm.bind_tools(hospital_tools)

    def hospital_worker(state: dict):
        """병원 워커 노드 - 병원 예약 관련 요청을 처리합니다."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        if not non_system_messages:
            return {"messages": []}

        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        system_prompt = CUSTOMER_SERVICE_SYSTEM_PROMPT + "\n\n당신은 병원 예약 전문 상담원입니다. 병원 예약, 진료과 조회, 예약 시간 확인 관련 요청을 처리합니다."
        messages_to_send = [SystemMessage(content=system_prompt)] + valid_messages
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}

    return hospital_worker


def create_hair_salon_worker():
    """헤어샵 워커 노드를 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    hair_salon_tools = [
        SearchHairSalonsTool,
        GetHairServiceInfoTool,
        CheckHairSalonAvailabilityTool,
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
    ]
    llm_with_tools = llm.bind_tools(hair_salon_tools)

    def hair_salon_worker(state: dict):
        """헤어샵 워커 노드 - 헤어샵 예약 관련 요청을 처리합니다."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        if not non_system_messages:
            return {"messages": []}

        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        system_prompt = CUSTOMER_SERVICE_SYSTEM_PROMPT + "\n\n당신은 헤어샵 예약 전문 상담원입니다. 헤어샵 예약, 서비스 조회, 예약 시간 확인 관련 요청을 처리합니다."
        messages_to_send = [SystemMessage(content=system_prompt)] + valid_messages
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}

    return hair_salon_worker


def create_booking_worker():
    """예약 관리 워커 노드를 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    booking_tools = [
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
    ]
    llm_with_tools = llm.bind_tools(booking_tools)

    def booking_worker(state: dict):
        """예약 관리 워커 노드 - 예약 관리 관련 요청을 처리합니다."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        if not non_system_messages:
            return {"messages": []}

        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        system_prompt = CUSTOMER_SERVICE_SYSTEM_PROMPT + "\n\n당신은 예약 관리 전문 상담원입니다. 예약 생성, 조회, 취소, 변경, 예약 상태 확인 관련 요청을 처리합니다."
        messages_to_send = [SystemMessage(content=system_prompt)] + valid_messages
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}

    return booking_worker


def create_general_customer_service_worker():
    """일반 고객센터 워커 노드를 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    general_tools = [
        ProvideServiceInfoTool,
        HandleCustomerInquiryTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
        SearchBookingsTool,
    ]
    llm_with_tools = llm.bind_tools(general_tools)

    def general_customer_service_worker(state: dict):
        """일반 고객센터 워커 노드 - 일반 고객센터 문의를 처리합니다."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        non_system_messages = [msg for msg in messages if not isinstance(msg, SystemMessage)]
        if not non_system_messages:
            return {"messages": []}

        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        system_prompt = CUSTOMER_SERVICE_SYSTEM_PROMPT + "\n\n당신은 고객센터 상담원입니다. 일반적인 고객 문의, 서비스 안내, 예약 관련 일반 정보 제공을 처리합니다."
        messages_to_send = [SystemMessage(content=system_prompt)] + valid_messages
        response = llm_with_tools.invoke(messages_to_send)
        return {"messages": [response]}

    return general_customer_service_worker


def should_continue_worker(state: dict) -> Literal["end", "continue"]:
    """워커 노드의 다음 단계를 결정하는 조건부 엣지 함수."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None

    if isinstance(last_message, AIMessage):
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        return "continue"

    return "end"


# 전역 워커 노드 인스턴스
_hotel_worker_func = None
_hospital_worker_func = None
_hair_salon_worker_func = None
_booking_worker_func = None
_general_customer_service_worker_func = None


def hotel_worker(state: dict):
    """호텔 워커 노드 래퍼 함수."""
    global _hotel_worker_func
    if _hotel_worker_func is None:
        _hotel_worker_func = create_hotel_worker()
    return _hotel_worker_func(state)


def hospital_worker(state: dict):
    """병원 워커 노드 래퍼 함수."""
    global _hospital_worker_func
    if _hospital_worker_func is None:
        _hospital_worker_func = create_hospital_worker()
    return _hospital_worker_func(state)


def hair_salon_worker(state: dict):
    """헤어샵 워커 노드 래퍼 함수."""
    global _hair_salon_worker_func
    if _hair_salon_worker_func is None:
        _hair_salon_worker_func = create_hair_salon_worker()
    return _hair_salon_worker_func(state)


def booking_worker(state: dict):
    """예약 관리 워커 노드 래퍼 함수."""
    global _booking_worker_func
    if _booking_worker_func is None:
        _booking_worker_func = create_booking_worker()
    return _booking_worker_func(state)


def general_customer_service_worker(state: dict):
    """일반 고객센터 워커 노드 래퍼 함수."""
    global _general_customer_service_worker_func
    if _general_customer_service_worker_func is None:
        _general_customer_service_worker_func = create_general_customer_service_worker()
    return _general_customer_service_worker_func(state)
