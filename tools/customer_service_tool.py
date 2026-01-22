"""고객센터 도구 - 고객센터 공통 기능을 제공합니다."""

from datetime import datetime
from langchain_core.tools import tool


@tool
def get_booking_status(booking_id: str) -> str:
    """예약 상태를 조회합니다.
    
    Args:
        booking_id: 예약 번호
    
    Returns:
        예약 상태 정보를 반환합니다.
    """
    try:
        from .booking_tool import load_bookings
        
        bookings = load_bookings()
        booking = next((b for b in bookings if b.get("id") == booking_id), None)
        
        if not booking:
            return f"예약 번호 '{booking_id}'를 찾을 수 없습니다."
        
        service_names = {
            "hotel": "호텔",
            "hospital": "병원",
            "hair": "헤어샵",
            "restaurant": "레스토랑",
            "etc": "기타"
        }
        
        service_name = service_names.get(booking.get("service_type", ""), booking.get("service_type", ""))
        status_names = {
            "confirmed": "확인됨",
            "cancelled": "취소됨",
            "completed": "완료됨",
            "pending": "대기 중"
        }
        
        status_name = status_names.get(booking.get("status", ""), booking.get("status", ""))
        
        result = f"""예약 상태 조회 결과:

예약 번호: {booking_id}
서비스: {service_name}
고객명: {booking.get('customer_name')}
날짜: {booking.get('date')}
시간: {booking.get('time')}
상태: {status_name}
"""
        
        if booking.get("phone"):
            result += f"연락처: {booking.get('phone')}\n"
        
        if booking.get("details"):
            result += f"상세: {booking.get('details')}\n"
        
        if booking.get("status") == "cancelled" and booking.get("cancel_reason"):
            result += f"취소 사유: {booking.get('cancel_reason')}\n"
        
        return result
    
    except Exception as e:
        return f"예약 상태 조회 오류: {str(e)}"


@tool
def get_customer_bookings(customer_name: str, phone: str = "") -> str:
    """고객의 모든 예약을 조회합니다.
    
    Args:
        customer_name: 고객 이름
        phone: 연락처 (선택사항, 정확한 매칭을 위해)
    
    Returns:
        고객의 예약 목록을 반환합니다.
    """
    try:
        from .booking_tool import load_bookings
        
        bookings = load_bookings()
        
        # 이름으로 필터링
        filtered = [b for b in bookings if customer_name.lower() in b.get("customer_name", "").lower()]
        
        # 전화번호로 추가 필터링 (제공된 경우)
        if phone:
            filtered = [b for b in filtered if b.get("phone") == phone]
        
        if not filtered:
            return f"{customer_name}님의 예약 내역을 찾을 수 없습니다."
        
        service_names = {
            "hotel": "호텔",
            "hospital": "병원",
            "hair": "헤어샵",
            "restaurant": "레스토랑",
            "etc": "기타"
        }
        
        status_names = {
            "confirmed": "확인됨",
            "cancelled": "취소됨",
            "completed": "완료됨",
            "pending": "대기 중"
        }
        
        result = f"""{customer_name}님의 예약 내역 ({len(filtered)}건):

"""
        for i, booking in enumerate(filtered, 1):
            service_name = service_names.get(booking.get("service_type", ""), booking.get("service_type", ""))
            status_name = status_names.get(booking.get("status", ""), booking.get("status", ""))
            
            result += f"""{i}. 예약 번호: {booking.get('id')}
   서비스: {service_name}
   날짜: {booking.get('date')}
   시간: {booking.get('time')}
   상태: {status_name}
   
"""
        
        return result
    
    except Exception as e:
        return f"예약 조회 오류: {str(e)}"


@tool
def provide_service_info(service_type: str) -> str:
    """서비스 유형에 대한 일반 정보를 제공합니다.
    
    Args:
        service_type: 서비스 유형 ("hotel", "hospital", "hair", "restaurant", "etc")
    
    Returns:
        서비스 정보를 반환합니다.
    """
    try:
        service_info = {
            "hotel": {
                "name": "호텔 예약",
                "description": "호텔 객실 예약 서비스를 제공합니다.",
                "features": [
                    "호텔 검색 및 비교",
                    "객실 유형 조회",
                    "체크인/체크아웃 날짜 확인",
                    "예약 및 취소"
                ],
                "contact": "예약 문의: 1588-0000"
            },
            "hospital": {
                "name": "병원 예약",
                "description": "병원 진료 예약 서비스를 제공합니다.",
                "features": [
                    "병원 검색",
                    "진료과별 예약",
                    "예약 가능 시간 확인",
                    "예약 및 취소"
                ],
                "contact": "예약 문의: 1588-1111"
            },
            "hair": {
                "name": "헤어샵 예약",
                "description": "헤어샵 서비스 예약을 제공합니다.",
                "features": [
                    "헤어샵 검색",
                    "서비스 유형별 예약",
                    "예약 가능 시간 확인",
                    "예약 및 취소"
                ],
                "contact": "예약 문의: 1588-2222"
            },
            "restaurant": {
                "name": "레스토랑 예약",
                "description": "레스토랑 예약 서비스를 제공합니다.",
                "features": [
                    "레스토랑 검색",
                    "예약 가능 시간 확인",
                    "인원수별 예약",
                    "예약 및 취소"
                ],
                "contact": "예약 문의: 1588-3333"
            },
            "etc": {
                "name": "기타 서비스",
                "description": "다양한 서비스 예약을 제공합니다.",
                "features": [
                    "서비스 검색",
                    "예약 가능 시간 확인",
                    "예약 및 취소"
                ],
                "contact": "예약 문의: 1588-9999"
            }
        }
        
        info = service_info.get(service_type)
        if not info:
            return f"'{service_type}' 서비스 정보를 찾을 수 없습니다."
        
        result = f"""{info['name']} 서비스 안내:

{info['description']}

주요 기능:
{chr(10).join(f'- {feature}' for feature in info['features'])}

{info['contact']}

도움이 필요하시면 언제든지 말씀해주세요!"""
        
        return result
    
    except Exception as e:
        return f"서비스 정보 제공 오류: {str(e)}"


@tool
def handle_customer_inquiry(inquiry_type: str, details: str = "") -> str:
    """고객 문의를 처리합니다.
    
    Args:
        inquiry_type: 문의 유형 ("예약", "취소", "변경", "환불", "기타")
        details: 문의 상세 내용 (선택사항)
    
    Returns:
        문의 처리 안내를 반환합니다.
    """
    try:
        responses = {
            "예약": """예약 도와드리겠습니다!

다음 정보를 알려주시면 예약을 진행해드리겠습니다:
- 서비스 유형 (호텔, 병원, 헤어샵 등)
- 예약 날짜
- 예약 시간
- 고객 이름
- 연락처 (선택사항)

원하시는 서비스를 알려주세요!""",
            
            "취소": """예약 취소 도와드리겠습니다!

예약 취소를 위해 다음 정보가 필요합니다:
- 예약 번호 (또는 고객 이름과 예약 날짜)

예약 번호를 알려주시면 바로 취소 처리를 도와드리겠습니다.""",
            
            "변경": """예약 변경 도와드리겠습니다!

예약 변경을 위해 다음 정보가 필요합니다:
- 예약 번호
- 변경하고 싶은 내용 (날짜, 시간 등)

예약 번호와 변경 사항을 알려주세요!""",
            
            "환불": """환불 문의 도와드리겠습니다!

환불 정책:
- 예약 취소 시 환불 규정은 서비스 유형에 따라 다릅니다
- 호텔: 체크인 3일 전 취소 시 전액 환불
- 병원: 당일 취소 시 환불 불가
- 헤어샵: 예약 시간 24시간 전 취소 시 전액 환불

자세한 환불 문의는 고객센터(1588-0000)로 연락주시기 바랍니다.""",
            
            "기타": """기타 문의 사항을 도와드리겠습니다!

다음과 같은 도움을 드릴 수 있습니다:
- 예약 조회
- 서비스 안내
- 예약 가능 시간 확인
- 기타 문의사항

어떤 도움이 필요하신가요?"""
        }
        
        response = responses.get(inquiry_type, responses["기타"])
        
        if details:
            response += f"\n\n문의 내용: {details}\n\n위 내용을 바탕으로 도와드리겠습니다!"
        
        return response
    
    except Exception as e:
        return f"문의 처리 오류: {str(e)}"


GetBookingStatusTool = get_booking_status
GetCustomerBookingsTool = get_customer_bookings
ProvideServiceInfoTool = provide_service_info
HandleCustomerInquiryTool = handle_customer_inquiry
