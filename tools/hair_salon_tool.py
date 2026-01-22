"""헤어샵 예약 도구 - 헤어샵 예약 관련 기능을 제공합니다."""

from langchain_core.tools import tool


@tool
def search_hair_salons(location: str, service_type: str = "") -> str:
    """헤어샵을 검색합니다.
    
    Args:
        location: 헤어샵 위치 (도시명 또는 지역명)
        service_type: 서비스 유형 (선택사항, 예: "컷트", "펌", "염색", "클리닉", "스타일링")
    
    Returns:
        헤어샵 검색 결과를 반환합니다.
    """
    try:
        salons = [
            {
                "name": f"{location} 프리미엄 헤어샵",
                "address": f"{location}시 미용로 123",
                "services": ["컷트", "펌", "염색", "클리닉", "스타일링"],
                "rating": 4.7,
                "price_range": "30,000원~150,000원",
                "phone": "02-1111-2222",
                "hours": "평일 10:00-20:00, 토요일 09:00-19:00"
            },
            {
                "name": f"{location} 스타일 헤어",
                "address": f"{location}시 패션로 456",
                "services": ["컷트", "펌", "염색", "스타일링"],
                "rating": 4.5,
                "price_range": "25,000원~120,000원",
                "phone": "02-2222-3333",
                "hours": "평일 09:00-21:00, 토요일 09:00-20:00"
            },
            {
                "name": f"{location} 뷰티 살롱",
                "address": f"{location}시 아름다운길 789",
                "services": ["컷트", "펌", "염색", "클리닉"],
                "rating": 4.6,
                "price_range": "20,000원~100,000원",
                "phone": "02-3333-4444",
                "hours": "평일 10:00-19:00, 토요일 10:00-18:00"
            }
        ]
        
        # 서비스 유형 필터링
        if service_type:
            service_type_str = str(service_type)
            salons = [
                s
                for s in salons
                if isinstance(svcs := s.get("services", []), list)
                and service_type_str in svcs
            ]
        
        if not salons:
            return f"{location} 지역에서 {service_type} 서비스를 제공하는 헤어샵을 찾을 수 없습니다."
        
        result = f"""{location} 지역 헤어샵 검색 결과:
{f'{service_type} 서비스 제공 헤어샵' if service_type else ''}

"""
        for i, salon in enumerate(salons, 1):
            result += f"""{i}. {salon['name']}
   주소: {salon['address']}
   평점: {'⭐' * int(salon['rating'])} ({salon['rating']})
   전화: {salon['phone']}
   영업 시간: {salon['hours']}
   가격대: {salon['price_range']}
   제공 서비스: {', '.join(salon['services'])}
   
"""
        
        return result
    
    except Exception as e:
        return f"헤어샵 검색 오류: {str(e)}"


@tool
def get_hair_service_info(service_type: str) -> str:
    """헤어 서비스 정보를 조회합니다.
    
    Args:
        service_type: 서비스 유형 ("컷트", "펌", "염색", "클리닉", "스타일링")
    
    Returns:
        서비스 정보를 반환합니다.
    """
    try:
        service_info = {
            "컷트": {
                "description": "머리카락을 원하는 길이와 스타일로 자릅니다.",
                "duration": "30분~1시간",
                "price_range": "20,000원~50,000원",
                "includes": ["컨설팅", "세안", "컷트", "드라이", "스타일링"]
            },
            "펌": {
                "description": "머리카락에 파마를 넣어 곱슬이나 웨이브를 만듭니다.",
                "duration": "2시간~3시간",
                "price_range": "80,000원~150,000원",
                "includes": ["컨설팅", "세안", "펌 시술", "드라이", "스타일링"]
            },
            "염색": {
                "description": "머리카락을 원하는 색으로 염색합니다.",
                "duration": "2시간~3시간",
                "price_range": "60,000원~120,000원",
                "includes": ["컨설팅", "세안", "염색 시술", "드라이", "스타일링"]
            },
            "클리닉": {
                "description": "두피와 모발 건강 관리를 위한 전문 케어 서비스입니다.",
                "duration": "1시간~1시간 30분",
                "price_range": "50,000원~100,000원",
                "includes": ["두피 진단", "두피 클렌징", "트리트먼트", "마사지"]
            },
            "스타일링": {
                "description": "드라이, 고데기, 볼륨 등을 이용한 헤어 스타일링 서비스입니다.",
                "duration": "30분~1시간",
                "price_range": "30,000원~80,000원",
                "includes": ["세안", "드라이", "스타일링", "완성"]
            }
        }
        
        info = service_info.get(service_type)
        if not info:
            return f"'{service_type}' 서비스 정보를 찾을 수 없습니다. 지원되는 서비스: {', '.join(service_info.keys())}"
        
        result = f"""{service_type} 서비스 정보:

설명: {info['description']}

소요 시간: {info['duration']}

가격대: {info['price_range']}

포함 사항:
{chr(10).join(f'- {item}' for item in info['includes'])}

예약을 도와드릴까요?"""
        
        return result
    
    except Exception as e:
        return f"서비스 정보 조회 오류: {str(e)}"


@tool
def check_hair_salon_availability(salon_name: str, service_type: str, date: str, 
                                 time: str = "") -> str:
    """헤어샵 예약 가능 시간을 확인합니다.
    
    Args:
        salon_name: 헤어샵 이름
        service_type: 서비스 유형
        date: 예약 날짜 (YYYY-MM-DD 형식)
        time: 희망 시간 (HH:MM 형식, 선택사항)
    
    Returns:
        예약 가능 시간 정보를 반환합니다.
    """
    try:
        # 실제 구현에서는 헤어샵 예약 시스템과 연동
        available_times = [
            "10:00", "10:30", "11:00", "11:30", "12:00", "12:30",
            "13:00", "13:30", "14:00", "14:30", "15:00", "15:30",
            "16:00", "16:30", "17:00", "17:30", "18:00", "18:30"
        ]
        
        result = f"""{salon_name} {service_type} 예약 가능 시간:

예약 날짜: {date}

예약 가능한 시간:
{chr(10).join(f'- {t}' for t in available_times)}
"""
        
        if time:
            if time in available_times:
                result += f"\n✅ {time} 시간대 예약이 가능합니다."
            else:
                result += f"\n⚠️ {time} 시간대는 예약이 불가능합니다. 위의 시간 중에서 선택해주세요."
        
        result += "\n원하시는 시간을 알려주시면 예약을 진행해드리겠습니다."
        
        return result
    
    except Exception as e:
        return f"예약 가능 시간 확인 오류: {str(e)}"


SearchHairSalonsTool = search_hair_salons
GetHairServiceInfoTool = get_hair_service_info
CheckHairSalonAvailabilityTool = check_hair_salon_availability
