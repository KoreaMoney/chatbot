"""에이전트 노드 - LangGraph 그래프의 노드들을 정의합니다."""

import os
from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START

from prompts.agent_prompts import AGENT_SYSTEM_PROMPT
from tools.calculator_tool import CalculatorTool
from tools.web_search_tool import WebSearchTool
from tools.date_time_tool import DateTool, DateDifferenceTool, AddDaysTool
from tools.text_transform_tool import TextCaseTool, UrlEncodeTool, UrlDecodeTool, Base64EncodeTool, Base64DecodeTool
from tools.unit_converter_tool import TemperatureConverterTool, LengthConverterTool, WeightConverterTool
from tools.random_generator_tool import RandomNumberTool, RandomStringTool, RandomPickTool
from tools.string_utils_tool import StringInfoTool, ReverseStringTool, CountOccurrencesTool, ReplaceTextTool, ExtractNumbersTool
from tools.json_tool import ParseJsonTool, ValidateJsonTool, GetJsonValueTool
from tools.hash_tool import HashTool
from tools.uuid_tool import UuidTool
from tools.file_tool import ReadFileTool, WriteFileTool, ListFilesTool
from tools.booking_tool import CreateBookingTool, SearchBookingsTool, CancelBookingTool, ModifyBookingTool
from tools.hotel_tool import SearchHotelsTool, GetHotelRoomTypesTool, CheckHotelAvailabilityTool
from tools.hospital_tool import SearchHospitalsTool, GetDepartmentInfoTool, CheckHospitalAvailabilityTool
from tools.hair_salon_tool import SearchHairSalonsTool, GetHairServiceInfoTool, CheckHairSalonAvailabilityTool
from tools.customer_service_tool import GetBookingStatusTool, GetCustomerBookingsTool, ProvideServiceInfoTool, HandleCustomerInquiryTool
from tools.test_generator_tool import TestGeneratorTool


def create_agent_node():
    """에이전트 노드를 생성합니다."""
    # LLM 초기화 (시스템 메시지 포함)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # 도구 바인딩
    tools = [
        CalculatorTool,
        WebSearchTool,
        DateTool,
        DateDifferenceTool,
        AddDaysTool,
        TextCaseTool,
        UrlEncodeTool,
        UrlDecodeTool,
        Base64EncodeTool,
        Base64DecodeTool,
        TemperatureConverterTool,
        LengthConverterTool,
        WeightConverterTool,
        RandomNumberTool,
        RandomStringTool,
        RandomPickTool,
        StringInfoTool,
        ReverseStringTool,
        CountOccurrencesTool,
        ReplaceTextTool,
        ExtractNumbersTool,
        ParseJsonTool,
        ValidateJsonTool,
        GetJsonValueTool,
        HashTool,
        UuidTool,
        ReadFileTool,
        WriteFileTool,
        ListFilesTool,
        TestGeneratorTool,
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
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: dict):
        """에이전트 노드 - 사용자 입력을 처리하고 응답을 생성합니다.
        
        LangGraph API의 체크포인터를 통해 이전 대화의 모든 메시지가
        state["messages"]에 자동으로 포함됩니다. 이를 통해 대화의 연속성을 유지합니다.
        """
        messages = state.get("messages", [])

        # 메시지가 비어있지 않은지 확인
        if not messages:
            # 메시지가 없으면 빈 응답 반환
            return {"messages": []}

        # 상태의 메시지 리스트에서 시스템 메시지 제외 (중복 방지)
        # 체크포인터를 통해 이전 대화의 모든 메시지가 포함되어 있음
        non_system_messages = [
            msg for msg in messages if not isinstance(msg, SystemMessage)
        ]

        # 메시지 배열이 비어있지 않은지 확인
        if not non_system_messages:
            return {"messages": []}

        # 유효한 메시지 순서로 재구성
        # ToolMessage는 반드시 선행하는 AIMessage의 tool_calls에 대한 응답이어야 함
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

        # 정상적인 경우: 시스템 메시지를 맨 앞에 추가
        messages_to_send = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + valid_messages

        # LLM 호출
        response = llm_with_tools.invoke(messages_to_send)

        return {"messages": [response]}

    return agent_node


def should_continue(state: dict) -> Literal["end", "continue"]:
    """다음 단계를 결정하는 조건부 엣지 함수."""
    messages = state.get("messages", [])
    last_message = messages[-1] if messages else None

    # 마지막 메시지가 AIMessage이고 tool_calls가 없으면 종료
    if isinstance(last_message, AIMessage):
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return "end"
        return "continue"

    return "end"


# 전역 에이전트 노드 인스턴스
_agent_node_func = None


def agent_node(state: dict):
    """에이전트 노드 래퍼 함수."""
    global _agent_node_func
    if _agent_node_func is None:
        _agent_node_func = create_agent_node()
    return _agent_node_func(state)
