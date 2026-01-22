"""에이전트 - LangGraph를 사용한 에이전트 구현."""

import os
from typing import Annotated, Optional, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from nodes.agent_nodes import agent_node, should_continue
from nodes.code_quality_nodes import code_quality_check_node
from nodes.customer_service_orchestrator_nodes import (
    customer_service_orchestrator_node,
    route_from_customer_service_orchestrator,
)
from nodes.customer_service_workers import (
    hotel_worker,
    hospital_worker,
    hair_salon_worker,
    booking_worker,
    general_customer_service_worker,
    should_continue_worker,
)
from nodes.orchestrator_nodes import orchestrator_node, route_from_orchestrator
from prompts.agent_prompts import AGENT_SYSTEM_PROMPT
from tools.calculator_tool import CalculatorTool
from tools.code_quality_tool import CodeQualityTool
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

load_dotenv()

# 상태 정의
class AgentState(TypedDict, total=False):
    """에이전트 상태."""
    messages: Annotated[list[BaseMessage], add_messages]
    next_node: Optional[str]  # 메인 오케스트레이터가 결정한 다음 노드
    customer_service_next_node: Optional[str]  # 고객센터 오케스트레이터가 결정한 다음 워커 노드
    code_quality_checked: Optional[bool]  # 코드 품질 검사 실행 여부 (스레드별)




def create_agent_graph():
    """LangGraph 에이전트 그래프를 생성합니다."""
    # LLM 초기화
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # 일반 에이전트 도구 바인딩
    general_tools = [
        CalculatorTool,
        CodeQualityTool,
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
    ]
    
    # 고객센터 도구 바인딩 (각 워커별로 분리)
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
    
    booking_tools = [
        CreateBookingTool,
        SearchBookingsTool,
        CancelBookingTool,
        ModifyBookingTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
    ]
    
    general_customer_service_tools = [
        ProvideServiceInfoTool,
        HandleCustomerInquiryTool,
        GetBookingStatusTool,
        GetCustomerBookingsTool,
        SearchBookingsTool,
    ]
    
    # 모든 고객센터 도구
    all_customer_service_tools = (
        hotel_tools + hospital_tools + hair_salon_tools + 
        booking_tools + general_customer_service_tools
    )
    
    # 모든 도구
    all_tools = general_tools + all_customer_service_tools
    
    # 그래프 생성 (오케스트레이터 패턴)
    workflow = StateGraph(AgentState)
    
    # 노드 추가
    # 타입 체커: LangGraph의 add_node는 런타임에 정상 작동하지만 타입 체커가 인식하지 못함
    workflow.add_node("code_quality_check", code_quality_check_node)  # type: ignore[arg-type]  # 코드 품질 자동 검사
    workflow.add_node("orchestrator", orchestrator_node)  # type: ignore[arg-type]  # 중앙 오케스트레이터
    workflow.add_node("agent", agent_node)  # type: ignore[arg-type]  # 일반 에이전트 워커
    workflow.add_node("customer_service_orchestrator", customer_service_orchestrator_node)  # type: ignore[arg-type]  # 고객센터 오케스트레이터
    workflow.add_node("hotel_worker", hotel_worker)  # type: ignore[arg-type]  # 호텔 워커
    workflow.add_node("hospital_worker", hospital_worker)  # type: ignore[arg-type]  # 병원 워커
    workflow.add_node("hair_salon_worker", hair_salon_worker)  # type: ignore[arg-type]  # 헤어샵 워커
    workflow.add_node("booking_worker", booking_worker)  # type: ignore[arg-type]  # 예약 관리 워커
    workflow.add_node("general_customer_service_worker", general_customer_service_worker)  # type: ignore[arg-type]  # 일반 고객센터 워커
    workflow.add_node("tools", ToolNode(all_tools))  # 일반 도구 실행
    workflow.add_node("hotel_tools", ToolNode(hotel_tools))  # 호텔 도구 실행
    workflow.add_node("hospital_tools", ToolNode(hospital_tools))  # 병원 도구 실행
    workflow.add_node("hair_salon_tools", ToolNode(hair_salon_tools))  # 헤어샵 도구 실행
    workflow.add_node("booking_tools", ToolNode(booking_tools))  # 예약 관리 도구 실행
    workflow.add_node("general_customer_service_tools", ToolNode(general_customer_service_tools))  # 일반 고객센터 도구 실행
    
    # 엣지 추가 (오케스트레이터 패턴)
    # 1. 시작점에서 코드 품질 검사로, 그 다음 오케스트레이터로
    workflow.add_edge(START, "code_quality_check")
    workflow.add_edge("code_quality_check", "orchestrator")
    
    # 2. 오케스트레이터가 결정한 노드로 라우팅
    workflow.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "agent": "agent",
            "customer_service": "customer_service_orchestrator",
        },
    )
    
    # 3. 일반 에이전트 노드의 조건부 엣지
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "agent")
    
    # 4. 고객센터 오케스트레이터가 결정한 워커로 라우팅
    workflow.add_conditional_edges(
        "customer_service_orchestrator",
        route_from_customer_service_orchestrator,
        {
            "hotel_worker": "hotel_worker",
            "hospital_worker": "hospital_worker",
            "hair_salon_worker": "hair_salon_worker",
            "booking_worker": "booking_worker",
            "general_customer_service": "general_customer_service_worker",
        },
    )
    
    # 5. 각 워커 노드의 조건부 엣지
    # 호텔 워커
    workflow.add_conditional_edges(
        "hotel_worker",
        should_continue_worker,
        {
            "continue": "hotel_tools",
            "end": END,
        },
    )
    workflow.add_edge("hotel_tools", "hotel_worker")
    
    # 병원 워커
    workflow.add_conditional_edges(
        "hospital_worker",
        should_continue_worker,
        {
            "continue": "hospital_tools",
            "end": END,
        },
    )
    workflow.add_edge("hospital_tools", "hospital_worker")
    
    # 헤어샵 워커
    workflow.add_conditional_edges(
        "hair_salon_worker",
        should_continue_worker,
        {
            "continue": "hair_salon_tools",
            "end": END,
        },
    )
    workflow.add_edge("hair_salon_tools", "hair_salon_worker")
    
    # 예약 관리 워커
    workflow.add_conditional_edges(
        "booking_worker",
        should_continue_worker,
        {
            "continue": "booking_tools",
            "end": END,
        },
    )
    workflow.add_edge("booking_tools", "booking_worker")
    
    # 일반 고객센터 워커
    workflow.add_conditional_edges(
        "general_customer_service_worker",
        should_continue_worker,
        {
            "continue": "general_customer_service_tools",
            "end": END,
        },
    )
    workflow.add_edge("general_customer_service_tools", "general_customer_service_worker")
    
    # 컴파일
    # 참고: LangGraph API는 자동으로 체크포인터를 제공합니다.
    # - thread_id를 통해 각 대화 세션의 상태가 자동으로 저장되고 복원됩니다.
    # - 각 super-step마다 체크포인트가 생성되어 대화 히스토리가 보존됩니다.
    # - state["messages"]에는 이전 대화의 모든 메시지가 자동으로 포함됩니다.
    # 자세한 내용: https://docs.langchain.com/oss/python/langgraph/persistence
    app = workflow.compile()
    return app


