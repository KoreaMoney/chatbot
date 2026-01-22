"""예약 관리 도구 - 다양한 서비스의 예약을 관리합니다."""

import json
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool

# 예약 데이터 저장 경로
BOOKINGS_FILE = Path("bookings.json")


def load_bookings():
    """예약 데이터를 로드합니다."""
    if BOOKINGS_FILE.exists():
        try:
            with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_bookings(bookings):
    """예약 데이터를 저장합니다."""
    with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)


@tool
def create_booking(service_type: str, customer_name: str, date: str, time: str, 
                   details: str = "", phone: str = "") -> str:
    """새로운 예약을 생성합니다.
    
    **중요**: 이 도구는 사용자가 명시적으로 예약을 요청했을 때만 사용해야 합니다.
    단순히 정보를 조회하거나 가용성을 확인하는 경우에는 사용하지 마세요.
    사용자가 "예약해줘", "예약하고 싶어", "예약해주세요" 등 명확한 예약 의사를 표현했을 때만 사용하세요.
    
    Args:
        service_type: 서비스 유형 ("hotel", "hospital", "hair", "restaurant", "etc")
        customer_name: 고객 이름
        date: 예약 날짜 (YYYY-MM-DD 형식)
        time: 예약 시간 (HH:MM 형식)
        details: 추가 상세 정보
        phone: 연락처 (선택사항)
    
    Returns:
        예약 생성 결과를 반환합니다.
    """
    try:
        bookings = load_bookings()
        
        # 예약 ID 생성
        booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        booking = {
            "id": booking_id,
            "service_type": service_type,
            "customer_name": customer_name,
            "date": date,
            "time": time,
            "details": details,
            "phone": phone,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        bookings.append(booking)
        save_bookings(bookings)
        
        service_names = {
            "hotel": "호텔",
            "hospital": "병원",
            "hair": "헤어샵",
            "restaurant": "레스토랑",
            "etc": "기타"
        }
        
        service_name = service_names.get(service_type, service_type)
        
        return f"""예약이 완료되었습니다!

예약 번호: {booking_id}
서비스: {service_name}
고객명: {customer_name}
날짜: {date}
시간: {time}
상태: 확인됨
{f'연락처: {phone}' if phone else ''}
{f'상세: {details}' if details else ''}

예약 번호를 꼭 기억해주세요."""
    
    except Exception as e:
        return f"예약 생성 오류: {str(e)}"


@tool
def search_bookings(customer_name: str = "", date: str = "", 
                   service_type: str = "", booking_id: str = "") -> str:
    """예약을 검색합니다.
    
    Args:
        customer_name: 고객 이름 (선택사항)
        date: 예약 날짜 (선택사항)
        service_type: 서비스 유형 (선택사항)
        booking_id: 예약 번호 (선택사항)
    
    Returns:
        검색된 예약 목록을 반환합니다.
    """
    try:
        bookings = load_bookings()
        
        # 필터링
        filtered = bookings
        if customer_name:
            filtered = [b for b in filtered if customer_name.lower() in b.get("customer_name", "").lower()]
        if date:
            filtered = [b for b in filtered if b.get("date") == date]
        if service_type:
            filtered = [b for b in filtered if b.get("service_type") == service_type]
        if booking_id:
            filtered = [b for b in filtered if b.get("id") == booking_id]
        
        if not filtered:
            return "검색된 예약이 없습니다."
        
        service_names = {
            "hotel": "호텔",
            "hospital": "병원",
            "hair": "헤어샵",
            "restaurant": "레스토랑",
            "etc": "기타"
        }
        
        result = f"검색된 예약 {len(filtered)}건:\n\n"
        for i, booking in enumerate(filtered, 1):
            service_name = service_names.get(booking.get("service_type", ""), booking.get("service_type", ""))
            result += f"""{i}. 예약 번호: {booking.get('id')}
   서비스: {service_name}
   고객명: {booking.get('customer_name')}
   날짜: {booking.get('date')}
   시간: {booking.get('time')}
   상태: {booking.get('status')}
   {f"연락처: {booking.get('phone')}" if booking.get('phone') else ''}
   {f"상세: {booking.get('details')}" if booking.get('details') else ''}
   
"""
        
        return result
    
    except Exception as e:
        return f"예약 검색 오류: {str(e)}"


@tool
def cancel_booking(booking_id: str, reason: str = "") -> str:
    """예약을 취소합니다.
    
    Args:
        booking_id: 예약 번호
        reason: 취소 사유 (선택사항)
    
    Returns:
        취소 결과를 반환합니다.
    """
    try:
        bookings = load_bookings()
        
        booking = next((b for b in bookings if b.get("id") == booking_id), None)
        
        if not booking:
            return f"예약 번호 '{booking_id}'를 찾을 수 없습니다."
        
        if booking.get("status") == "cancelled":
            return "이미 취소된 예약입니다."
        
        booking["status"] = "cancelled"
        booking["cancelled_at"] = datetime.now().isoformat()
        if reason:
            booking["cancel_reason"] = reason
        
        save_bookings(bookings)
        
        return f"""예약이 취소되었습니다.

예약 번호: {booking_id}
고객명: {booking.get('customer_name')}
{f'취소 사유: {reason}' if reason else ''}

취소 처리가 완료되었습니다."""
    
    except Exception as e:
        return f"예약 취소 오류: {str(e)}"


@tool
def modify_booking(booking_id: str, date: str = "", time: str = "", 
                  details: str = "") -> str:
    """예약을 수정합니다.
    
    Args:
        booking_id: 예약 번호
        date: 새로운 날짜 (선택사항)
        time: 새로운 시간 (선택사항)
        details: 새로운 상세 정보 (선택사항)
    
    Returns:
        수정 결과를 반환합니다.
    """
    try:
        bookings = load_bookings()
        
        booking = next((b for b in bookings if b.get("id") == booking_id), None)
        
        if not booking:
            return f"예약 번호 '{booking_id}'를 찾을 수 없습니다."
        
        if booking.get("status") == "cancelled":
            return "취소된 예약은 수정할 수 없습니다."
        
        changes = []
        if date:
            old_date = booking.get("date")
            booking["date"] = date
            changes.append(f"날짜: {old_date} → {date}")
        if time:
            old_time = booking.get("time")
            booking["time"] = time
            changes.append(f"시간: {old_time} → {time}")
        if details:
            booking["details"] = details
            changes.append(f"상세 정보가 업데이트되었습니다")
        
        booking["modified_at"] = datetime.now().isoformat()
        save_bookings(bookings)
        
        if not changes:
            return "변경사항이 없습니다."
        
        return f"""예약이 수정되었습니다.

예약 번호: {booking_id}
변경 사항:
{chr(10).join(f'- {change}' for change in changes)}

수정 처리가 완료되었습니다."""
    
    except Exception as e:
        return f"예약 수정 오류: {str(e)}"


CreateBookingTool = create_booking
SearchBookingsTool = search_bookings
CancelBookingTool = cancel_booking
ModifyBookingTool = modify_booking
