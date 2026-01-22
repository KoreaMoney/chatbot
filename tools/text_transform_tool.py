"""텍스트 변환 도구 - 텍스트를 다양한 형식으로 변환합니다."""

import urllib.parse
import base64
from langchain_core.tools import tool


@tool
def transform_text_case(text: str, case: str) -> str:
    """텍스트의 대소문자를 변환합니다.
    
    Args:
        text: 변환할 텍스트
        case: 변환 형식 ("upper", "lower", "title", "capitalize")
    
    Returns:
        변환된 텍스트를 반환합니다.
    """
    try:
        if case == "upper":
            return f"대문자 변환: {text.upper()}"
        elif case == "lower":
            return f"소문자 변환: {text.lower()}"
        elif case == "title":
            return f"제목 형식 변환: {text.title()}"
        elif case == "capitalize":
            return f"첫 글자 대문자 변환: {text.capitalize()}"
        else:
            return f"지원되지 않는 형식입니다. 'upper', 'lower', 'title', 'capitalize' 중 하나를 선택하세요."
    except Exception as e:
        return f"텍스트 변환 오류: {str(e)}"


@tool
def url_encode(text: str) -> str:
    """텍스트를 URL 인코딩합니다.
    
    Args:
        text: 인코딩할 텍스트
    
    Returns:
        URL 인코딩된 텍스트를 반환합니다.
    """
    try:
        encoded = urllib.parse.quote(text)
        return f"URL 인코딩 결과: {encoded}"
    except Exception as e:
        return f"URL 인코딩 오류: {str(e)}"


@tool
def url_decode(encoded_text: str) -> str:
    """URL 인코딩된 텍스트를 디코딩합니다.
    
    Args:
        encoded_text: 디코딩할 URL 인코딩된 텍스트
    
    Returns:
        디코딩된 텍스트를 반환합니다.
    """
    try:
        decoded = urllib.parse.unquote(encoded_text)
        return f"URL 디코딩 결과: {decoded}"
    except Exception as e:
        return f"URL 디코딩 오류: {str(e)}"


@tool
def base64_encode(text: str) -> str:
    """텍스트를 Base64로 인코딩합니다.
    
    Args:
        text: 인코딩할 텍스트
    
    Returns:
        Base64 인코딩된 텍스트를 반환합니다.
    """
    try:
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return f"Base64 인코딩 결과: {encoded}"
    except Exception as e:
        return f"Base64 인코딩 오류: {str(e)}"


@tool
def base64_decode(encoded_text: str) -> str:
    """Base64 인코딩된 텍스트를 디코딩합니다.
    
    Args:
        encoded_text: 디코딩할 Base64 인코딩된 텍스트
    
    Returns:
        디코딩된 텍스트를 반환합니다.
    """
    try:
        decoded = base64.b64decode(encoded_text).decode('utf-8')
        return f"Base64 디코딩 결과: {decoded}"
    except Exception as e:
        return f"Base64 디코딩 오류: {str(e)}"


TextCaseTool = transform_text_case
UrlEncodeTool = url_encode
UrlDecodeTool = url_decode
Base64EncodeTool = base64_encode
Base64DecodeTool = base64_decode
