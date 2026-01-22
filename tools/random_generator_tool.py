"""랜덤 생성 도구 - 랜덤 값 생성을 수행합니다."""

import random
import string
from langchain_core.tools import tool


@tool
def generate_random_number(min_value: int, max_value: int, count: int = 1) -> str:
    """랜덤 숫자를 생성합니다.
    
    Args:
        min_value: 최소값
        max_value: 최대값
        count: 생성할 개수 (기본값: 1)
    
    Returns:
        생성된 랜덤 숫자를 반환합니다.
    """
    try:
        if count == 1:
            result = random.randint(min_value, max_value)
            return f"생성된 랜덤 숫자: {result}"
        else:
            results = [random.randint(min_value, max_value) for _ in range(count)]
            return f"생성된 랜덤 숫자 {count}개: {results}"
    except Exception as e:
        return f"랜덤 숫자 생성 오류: {str(e)}"


@tool
def generate_random_string(length: int, include_uppercase: bool = True, 
                          include_lowercase: bool = True, include_digits: bool = True,
                          include_special: bool = False) -> str:
    """랜덤 문자열을 생성합니다.
    
    Args:
        length: 문자열 길이
        include_uppercase: 대문자 포함 여부 (기본값: True)
        include_lowercase: 소문자 포함 여부 (기본값: True)
        include_digits: 숫자 포함 여부 (기본값: True)
        include_special: 특수문자 포함 여부 (기본값: False)
    
    Returns:
        생성된 랜덤 문자열을 반환합니다.
    """
    try:
        chars = ""
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += string.punctuation
        
        if not chars:
            return "오류: 최소 하나의 문자 집합을 선택해야 합니다."
        
        result = ''.join(random.choice(chars) for _ in range(length))
        return f"생성된 랜덤 문자열: {result}"
    except Exception as e:
        return f"랜덤 문자열 생성 오류: {str(e)}"


@tool
def pick_random_item(items: str) -> str:
    """리스트에서 랜덤 항목을 선택합니다.
    
    Args:
        items: 쉼표로 구분된 항목들 (예: "사과, 바나나, 오렌지")
    
    Returns:
        선택된 랜덤 항목을 반환합니다.
    """
    try:
        item_list = [item.strip() for item in items.split(",")]
        if not item_list:
            return "오류: 항목이 없습니다."
        selected = random.choice(item_list)
        return f"선택된 항목: {selected}"
    except Exception as e:
        return f"랜덤 선택 오류: {str(e)}"


RandomNumberTool = generate_random_number
RandomStringTool = generate_random_string
RandomPickTool = pick_random_item
