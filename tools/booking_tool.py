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
    
    **매우 중요**: 이 도구를 사용하기 전에 반드시 다음 조건을 모두 만족해야 합니다:
    
    1. 사용자가 명시적으로 예약을 요청했을 때만 사용 (예: "예약해줘", "예약하고 싶어", "예약해주세요")
    2. 단순히 정보를 조회하거나 가용성을 확인하는 경우에는 절대 사용하지 마세요
    3. **필수 정보가 모두 수집되었는지 확인**:
       - customer_name: 반드시 사용자로부터 받은 실제 이름이어야 함. "고객", "미정" 같은 기본값 사용 금지
       - date: 반드시 사용자로부터 받은 날짜여야 함. YYYY-MM-DD 형식
       - time: 반드시 사용자로부터 받은 시간이어야 함. HH:MM 형식
       - service_type: 서비스 유형이 명확해야 함
       - details: 병원명, 호텔명 등 상세 정보
    4. **필수 정보가 하나라도 없으면 이 도구를 절대 사용하지 마세요. 먼저 사용자에게 물어보세요**
    5. **반드시 예약 정보를 사용자에게 보여주고 확인을 받은 후에만 사용하세요**
    6. 사용자가 "네", "예", "확인", "진행", "예약해줘" 등으로 명시적으로 확인했을 때만 사용
    7. 사용자가 확인하지 않았거나 거부한 경우에는 절대 사용하지 마세요
    
    **절대 하지 말아야 할 것**:
    - 필수 정보(고객명, 날짜, 시간) 없이 이 도구 호출 금지
    - "고객", "미정", "TBD" 같은 기본값이나 임의의 값으로 예약 생성 금지
    - 사용자에게 물어보지 않고 추측해서 예약 생성 금지
    - 예약 정보를 먼저 표시하고 사용자 확인을 받지 않고 바로 이 도구를 호출 금지
    
    Args:
        service_type: 서비스 유형 ("hotel", "hospital", "hair", "restaurant", "etc")
        customer_name: 고객 이름 (사용자로부터 받은 실제 이름, 기본값 사용 금지)
        date: 예약 날짜 (YYYY-MM-DD 형식, 사용자로부터 받은 날짜)
        time: 예약 시간 (HH:MM 형식, 사용자로부터 받은 시간)
        details: 추가 상세 정보 (병원명, 호텔명 등)
        phone: 연락처 (선택사항)
    
    Returns:
        예약 생성 결과를 반환합니다.
    """
    try:
        # 필수 정보 검증
        if not customer_name or customer_name.strip() == "":
            return "오류: 고객명이 필요합니다. 사용자에게 고객명을 먼저 물어보세요."
        
        # 기본값이나 임의의 값 사용 금지
        invalid_names = ["고객", "미정", "TBD", "미지정", "없음", "알 수 없음", "unknown", "customer"]
        if customer_name.strip() in invalid_names:
            return f"오류: '{customer_name}'는 유효한 고객명이 아닙니다. 사용자에게 실제 고객명을 먼저 물어보세요."
        
        if not date or date.strip() == "":
            return "오류: 예약 날짜가 필요합니다. 사용자에게 날짜를 먼저 물어보세요."
        
        # 날짜 형식 검증 (YYYY-MM-DD)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return f"오류: 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식이어야 합니다. (입력된 값: {date})"
        
        if not time or time.strip() == "":
            return "오류: 예약 시간이 필요합니다. 사용자에게 시간을 먼저 물어보세요."
        
        # 시간 형식 검증 (HH:MM)
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            return f"오류: 시간 형식이 올바르지 않습니다. HH:MM 형식이어야 합니다. (입력된 값: {time})"
        
        if not service_type or service_type.strip() == "":
            return "오류: 서비스 유형이 필요합니다."
        
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
