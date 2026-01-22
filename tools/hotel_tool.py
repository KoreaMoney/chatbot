"""호텔 예약 도구 - 호텔 예약 관련 기능을 제공합니다."""

from langchain_core.tools import tool
from duckduckgo_search import DDGS


@tool
def search_hotels(location: str, check_in: str = "", check_out: str = "", 
                 guests: int = 1) -> str:
    """호텔을 검색합니다. 실제 웹 검색을 통해 호텔 정보를 가져옵니다.
    
    Args:
        location: 호텔 위치 (도시명 또는 지역명)
        check_in: 체크인 날짜 (YYYY-MM-DD 형식, 선택사항)
        check_out: 체크아웃 날짜 (YYYY-MM-DD 형식, 선택사항)
        guests: 투숙 인원 (기본값: 1)
    
    Returns:
        호텔 검색 결과를 반환합니다.
    """
    try:
        # 실제 웹 검색을 수행합니다
        search_query = f"{location} 호텔"
        if check_in and check_out:
            search_query += f" {check_in} {check_out}"
        
        with DDGS() as ddgs:
            # 최대 10개의 검색 결과를 가져옵니다
            results = list(ddgs.text(search_query, max_results=10))
            
            if not results:
                return f"'{location}' 지역의 호텔 검색 결과를 찾을 수 없습니다."
            
            # 검색 결과를 포맷팅합니다
            result = f"""{location} 지역 호텔 검색 결과:

"""
            
            date_info = ""
            if check_in and check_out:
                date_info = f"체크인: {check_in}, 체크아웃: {check_out}\n   "
            
            for i, search_result in enumerate(results[:5], 1):  # 상위 5개만 표시
                title = search_result.get("title", "제목 없음")
                body = search_result.get("body", "내용 없음")
                href = search_result.get("href", "")
                
                result += f"""{i}. {title}
   {body[:150]}...
   출처: {href}
   {date_info}투숙 인원: {guests}명
   
"""
            
            if check_in and check_out:
                result += f"\n체크인: {check_in}, 체크아웃: {check_out} 기준으로 검색되었습니다."
            else:
                result += "\n더 자세한 정보나 예약을 원하시면 체크인/체크아웃 날짜를 알려주세요."
            
            return result
    
    except Exception as e:
        return f"호텔 검색 오류: {str(e)}"


@tool
def get_hotel_room_types(hotel_name: str) -> str:
    """호텔의 객실 유형을 조회합니다.
    
    Args:
        hotel_name: 호텔 이름
    
    Returns:
        객실 유형 목록을 반환합니다.
    """
    try:
        room_types = [
            {
                "type": "스탠다드 트윈",
                "description": "2개의 싱글 침대, 20㎡",
                "price": 100000,
                "capacity": 2,
                "amenities": ["TV", "에어컨", "무료 와이파이", "욕실"]
            },
            {
                "type": "스탠다드 더블",
                "description": "킹 사이즈 침대, 25㎡",
                "price": 120000,
                "capacity": 2,
                "amenities": ["TV", "에어컨", "무료 와이파이", "욕실", "미니바"]
            },
            {
                "type": "디럭스 트윈",
                "description": "2개의 더블 침대, 35㎡",
                "price": 150000,
                "capacity": 4,
                "amenities": ["TV", "에어컨", "무료 와이파이", "욕실", "미니바", "발코니"]
            },
            {
                "type": "스위트",
                "description": "거실과 침실 분리, 50㎡",
                "price": 250000,
                "capacity": 4,
                "amenities": ["TV", "에어컨", "무료 와이파이", "욕실", "미니바", "발코니", "거실"]
            }
        ]
        
        result = f"""{hotel_name} 객실 유형:

"""
        for i, room in enumerate(room_types, 1):
            result += f"""{i}. {room['type']}
   설명: {room['description']}
   가격: {room['price']:,}원/박
   수용 인원: {room['capacity']}명
   시설: {', '.join(room['amenities'])}
   
"""
        
        return result
    
    except Exception as e:
        return f"객실 유형 조회 오류: {str(e)}"


@tool
def check_hotel_availability(hotel_name: str, check_in: str, check_out: str, 
                            room_type: str = "") -> str:
    """호텔 객실 가용성을 확인합니다.
    
    Args:
        hotel_name: 호텔 이름
        check_in: 체크인 날짜 (YYYY-MM-DD 형식)
        check_out: 체크아웃 날짜 (YYYY-MM-DD 형식)
        room_type: 객실 유형 (선택사항)
    
    Returns:
        객실 가용성 정보를 반환합니다.
    """
    try:
        # 실제 구현에서는 예약 시스템과 연동
        result = f"""{hotel_name} 객실 가용성 확인:

체크인: {check_in}
체크아웃: {check_out}
"""
        
        if room_type:
            result += f"객실 유형: {room_type}\n\n"
            result += f"✅ {room_type} 객실이 예약 가능합니다.\n"
            result += "예약을 진행하시겠습니까?"
        else:
            result += "\n예약 가능한 객실 유형:\n"
            result += "- 스탠다드 트윈: 예약 가능\n"
            result += "- 스탠다드 더블: 예약 가능\n"
            result += "- 디럭스 트윈: 예약 가능\n"
            result += "- 스위트: 예약 가능\n"
            result += "\n원하시는 객실 유형을 알려주시면 상세 정보를 제공해드리겠습니다."
        
        return result
    
    except Exception as e:
        return f"가용성 확인 오류: {str(e)}"


SearchHotelsTool = search_hotels
GetHotelRoomTypesTool = get_hotel_room_types
CheckHotelAvailabilityTool = check_hotel_availability
