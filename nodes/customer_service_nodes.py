"""고객센터 노드 - LangGraph 그래프의 고객센터 노드를 정의합니다."""

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


def create_customer_service_node():
    """고객센터 노드를 생성합니다."""
    # LLM 초기화
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # 고객센터 전용 도구 바인딩
    customer_service_tools = [
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        SearchHotelsTool,
        GetHotelRoomTypesTool,
        CheckHotelAvailabilityTool,
        SearchHospitalsTool,
        GetDepartmentInfoTool,
        CheckHospitalAvailabilityTool,
        SearchHairSalonsTool,
        GetHairServiceInfoTool,
        CheckHairSalonAvailabilityTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
        ProvideServiceInfoTool,
        HandleCustomerInquiryTool,
    ]
    llm_with_tools = llm.bind_tools(customer_service_tools)

    def customer_service_node(state: dict):
        """고객센터 노드 - 고객센터 관련 요청을 처리하고 응답을 생성합니다.
        
        LangGraph API의 체크포인터를 통해 이전 대화의 모든 메시지가
        state["messages"]에 자동으로 포함됩니다. 이를 통해 대화의 연속성을 유지합니다.
        """
        messages = state.get("messages", [])

        # 메시지가 비어있지 않은지 확인
        if not messages:
            return {"messages": []}

        # 상태의 메시지 리스트에서 시스템 메시지 제외 (중복 방지)
        non_system_messages = [
            msg for msg in messages if not isinstance(msg, SystemMessage)
        ]

        # 메시지 배열이 비어있지 않은지 확인
        if not non_system_messages:
            return {"messages": []}

        # 유효한 메시지 순서로 재구성
        valid_messages = []
        for i, msg in enumerate(non_system_messages):
            if isinstance(msg, ToolMessage):
                # ToolMessage의 경우, 바로 이전 메시지가 AIMessage이고 tool_calls가 있어야 함
                if i > 0 and isinstance(non_system_messages[i - 1], AIMessage):
                    prev_msg = non_system_messages[i - 1]
                    if hasattr(prev_msg, "tool_calls") and prev_msg.tool_calls:
                        valid_messages.append(msg)
            else:
                valid_messages.append(msg)

        if not valid_messages:
            return {"messages": []}

        # 고객센터 시스템 메시지를 맨 앞에 추가
        messages_to_send = [SystemMessage(content=CUSTOMER_SERVICE_SYSTEM_PROMPT)] + valid_messages

        # LLM 호출
        response = llm_with_tools.invoke(messages_to_send)

        return {"messages": [response]}

    return customer_service_node


def should_continue_customer_service(state: dict) -> Literal["end", "continue"]:
    """고객센터 노드의 다음 단계를 결정하는 조건부 엣지 함수."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None

    # 마지막 메시지가 AIMessage이고 tool_calls가 없으면 종료
    if isinstance(last_message, AIMessage):
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        return "continue"

    return "end"


# 전역 고객센터 노드 인스턴스
_customer_service_node_func = None


def customer_service_node(state: dict):
    """고객센터 노드 래퍼 함수."""
    global _customer_service_node_func
    if _customer_service_node_func is None:
        _customer_service_node_func = create_customer_service_node()
    return _customer_service_node_func(state)
