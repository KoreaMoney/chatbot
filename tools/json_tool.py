"""JSON 처리 도구 - JSON 데이터를 파싱하고 검증합니다."""

import json
from langchain_core.tools import tool


@tool
def parse_json(json_string: str) -> str:
    """JSON 문자열을 파싱하고 포맷팅합니다.
    
    Args:
        json_string: 파싱할 JSON 문자열
    
    Returns:
        파싱된 JSON을 보기 좋게 포맷팅하여 반환합니다.
    """
    try:
        parsed = json.loads(json_string)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
        return f"파싱된 JSON:\n{formatted}"
    except json.JSONDecodeError as e:
        return f"JSON 파싱 오류: {str(e)}"
    except Exception as e:
        return f"오류 발생: {str(e)}"


@tool
def validate_json(json_string: str) -> str:
    """JSON 문자열이 유효한지 검증합니다.
    
    Args:
        json_string: 검증할 JSON 문자열
    
    Returns:
        검증 결과를 반환합니다.
    """
    try:
        json.loads(json_string)
        return "JSON이 유효합니다."
    except json.JSONDecodeError as e:
        return f"JSON이 유효하지 않습니다: {str(e)}"
    except Exception as e:
        return f"검증 오류: {str(e)}"


@tool
def get_json_value(json_string: str, key_path: str) -> str:
    """JSON에서 특정 키의 값을 가져옵니다.
    
    Args:
        json_string: JSON 문자열
        key_path: 키 경로 (예: "user.name" 또는 "items[0]")
    
    Returns:
        해당 키의 값을 반환합니다.
    """
    try:
        data = json.loads(json_string)
        
        # 키 경로 파싱 (간단한 버전)
        keys = key_path.split(".")
        result = data
        
        for key in keys:
            if "[" in key and "]" in key:
                # 배열 인덱스 처리
                base_key = key.split("[")[0]
                index = int(key.split("[")[1].split("]")[0])
                result = result[base_key][index]
            else:
                result = result[key]
        
        return f"키 '{key_path}'의 값: {json.dumps(result, ensure_ascii=False)}"
    except KeyError:
        return f"키 '{key_path}'를 찾을 수 없습니다."
    except json.JSONDecodeError as e:
        return f"JSON 파싱 오류: {str(e)}"
    except Exception as e:
        return f"오류 발생: {str(e)}"


ParseJsonTool = parse_json
ValidateJsonTool = validate_json
GetJsonValueTool = get_json_value
