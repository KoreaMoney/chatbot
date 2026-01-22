"""해시 생성 도구 - 다양한 해시 알고리즘으로 해시를 생성합니다."""

import hashlib
from langchain_core.tools import tool


@tool
def generate_hash(text: str, algorithm: str = "md5") -> str:
    """텍스트의 해시 값을 생성합니다.
    
    Args:
        text: 해시를 생성할 텍스트
        algorithm: 해시 알고리즘 ("md5", "sha1", "sha256", "sha512")
    
    Returns:
        생성된 해시 값을 반환합니다.
    """
    try:
        text_bytes = text.encode('utf-8')
        
        if algorithm.lower() == "md5":
            hash_obj = hashlib.md5(text_bytes)
        elif algorithm.lower() == "sha1":
            hash_obj = hashlib.sha1(text_bytes)
        elif algorithm.lower() == "sha256":
            hash_obj = hashlib.sha256(text_bytes)
        elif algorithm.lower() == "sha512":
            hash_obj = hashlib.sha512(text_bytes)
        else:
            return "지원되지 않는 알고리즘입니다. 'md5', 'sha1', 'sha256', 'sha512' 중 하나를 선택하세요."
        
        hash_value = hash_obj.hexdigest()
        return f"{algorithm.upper()} 해시 값: {hash_value}"
    except Exception as e:
        return f"해시 생성 오류: {str(e)}"


HashTool = generate_hash
