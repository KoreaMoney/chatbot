"""문자열 처리 도구 - 문자열 관련 유틸리티 작업을 수행합니다."""

from langchain_core.tools import tool


@tool
def get_string_info(text: str) -> str:
    """문자열의 정보를 반환합니다.
    
    Args:
        text: 분석할 문자열
    
    Returns:
        문자열의 길이, 단어 수, 줄 수 등의 정보를 반환합니다.
    """
    try:
        length = len(text)
        word_count = len(text.split())
        line_count = len(text.splitlines())
        char_count_no_spaces = len(text.replace(" ", ""))
        
        info = f"""문자열 정보:
- 전체 길이: {length}자
- 공백 제외 길이: {char_count_no_spaces}자
- 단어 수: {word_count}개
- 줄 수: {line_count}줄"""
        
        return info
    except Exception as e:
        return f"문자열 분석 오류: {str(e)}"


@tool
def reverse_string(text: str) -> str:
    """문자열을 뒤집습니다.
    
    Args:
        text: 뒤집을 문자열
    
    Returns:
        뒤집힌 문자열을 반환합니다.
    """
    try:
        return f"뒤집힌 문자열: {text[::-1]}"
    except Exception as e:
        return f"문자열 뒤집기 오류: {str(e)}"


@tool
def count_occurrences(text: str, substring: str) -> str:
    """문자열에서 특정 부분 문자열의 출현 횟수를 세습니다.
    
    Args:
        text: 검색할 문자열
        substring: 찾을 부분 문자열
    
    Returns:
        출현 횟수를 반환합니다.
    """
    try:
        count = text.count(substring)
        return f"'{substring}'의 출현 횟수: {count}회"
    except Exception as e:
        return f"문자열 검색 오류: {str(e)}"


@tool
def replace_text(text: str, old: str, new: str) -> str:
    """문자열에서 특정 부분을 다른 문자열로 교체합니다.
    
    Args:
        text: 원본 문자열
        old: 교체할 부분 문자열
        new: 새로운 문자열
    
    Returns:
        교체된 문자열을 반환합니다.
    """
    try:
        result = text.replace(old, new)
        return f"교체 결과: {result}"
    except Exception as e:
        return f"문자열 교체 오류: {str(e)}"


@tool
def extract_numbers(text: str) -> str:
    """문자열에서 숫자를 추출합니다.
    
    Args:
        text: 숫자를 추출할 문자열
    
    Returns:
        추출된 숫자들을 반환합니다.
    """
    try:
        import re
        numbers = re.findall(r'-?\d+\.?\d*', text)
        if numbers:
            return f"추출된 숫자들: {', '.join(numbers)}"
        else:
            return "숫자를 찾을 수 없습니다."
    except Exception as e:
        return f"숫자 추출 오류: {str(e)}"


StringInfoTool = get_string_info
ReverseStringTool = reverse_string
CountOccurrencesTool = count_occurrences
ReplaceTextTool = replace_text
ExtractNumbersTool = extract_numbers
