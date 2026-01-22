"""날짜/시간 도구 - 날짜와 시간 관련 작업을 수행합니다."""

from datetime import datetime, timedelta
from langchain_core.tools import tool


@tool
def get_current_datetime(format: str = "default") -> str:
    """현재 날짜와 시간을 가져옵니다.
    
    Args:
        format: 날짜 형식 ("default", "iso", "korean", "timestamp")
    
    Returns:
        현재 날짜와 시간을 문자열로 반환합니다.
    """
    try:
        now = datetime.now()
        
        if format == "iso":
            return f"현재 시간 (ISO 형식): {now.isoformat()}"
        elif format == "korean":
            return f"현재 시간: {now.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}"
        elif format == "timestamp":
            return f"현재 타임스탬프: {now.timestamp()}"
        else:
            return f"현재 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"날짜/시간 조회 오류: {str(e)}"


@tool
def calculate_date_difference(date1: str, date2: str) -> str:
    """두 날짜 사이의 차이를 계산합니다.
    
    Args:
        date1: 첫 번째 날짜 (YYYY-MM-DD 형식)
        date2: 두 번째 날짜 (YYYY-MM-DD 형식)
    
    Returns:
        두 날짜 사이의 차이를 일 단위로 반환합니다.
    """
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = abs((d2 - d1).days)
        return f"{date1}와 {date2} 사이의 차이는 {diff}일입니다."
    except Exception as e:
        return f"날짜 계산 오류: {str(e)}"


@tool
def add_days_to_date(date: str, days: int) -> str:
    """날짜에 일수를 더합니다.
    
    Args:
        date: 기준 날짜 (YYYY-MM-DD 형식)
        days: 더할 일수 (음수 가능)
    
    Returns:
        계산된 날짜를 반환합니다.
    """
    try:
        base_date = datetime.strptime(date, "%Y-%m-%d")
        result_date = base_date + timedelta(days=days)
        return f"{date}로부터 {days}일 후: {result_date.strftime('%Y-%m-%d')}"
    except Exception as e:
        return f"날짜 계산 오류: {str(e)}"


DateTool = get_current_datetime
DateDifferenceTool = calculate_date_difference
AddDaysTool = add_days_to_date
