"""계산기 도구 - 간단한 수학 계산을 수행합니다."""

from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """수학 표현식을 계산합니다.
    
    Args:
        expression: 계산할 수학 표현식 (예: "2 + 2", "10 * 5")
    
    Returns:
        계산 결과를 문자열로 반환합니다.
    """
    try:
        # 보안을 위해 제한된 연산만 허용
        allowed_chars = set("0123456789+-*/.() ")
        if not all(c in allowed_chars for c in expression):
            return "오류: 허용되지 않은 문자가 포함되어 있습니다."
        
        result = eval(expression)
        return f"계산 결과: {result}"
    except Exception as e:
        return f"계산 오류: {str(e)}"


CalculatorTool = calculate
