"""UUID 생성 도구 - UUID를 생성합니다."""

import uuid
from langchain_core.tools import tool


@tool
def generate_uuid(version: int = 4) -> str:
    """UUID를 생성합니다.
    
    Args:
        version: UUID 버전 (1, 3, 4, 5, 기본값: 4)
    
    Returns:
        생성된 UUID를 반환합니다.
    """
    try:
        if version == 1:
            result = uuid.uuid1()
        elif version == 3:
            # 버전 3은 네임스페이스와 이름이 필요하므로 기본값 사용
            namespace = uuid.NAMESPACE_DNS
            name = "example.com"
            result = uuid.uuid3(namespace, name)
        elif version == 4:
            result = uuid.uuid4()
        elif version == 5:
            # 버전 5는 네임스페이스와 이름이 필요하므로 기본값 사용
            namespace = uuid.NAMESPACE_DNS
            name = "example.com"
            result = uuid.uuid5(namespace, name)
        else:
            return "지원되지 않는 UUID 버전입니다. 1, 3, 4, 5 중 하나를 선택하세요."
        
        return f"생성된 UUID (v{version}): {str(result)}"
    except Exception as e:
        return f"UUID 생성 오류: {str(e)}"


UuidTool = generate_uuid
