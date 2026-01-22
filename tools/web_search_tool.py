"""웹 검색 도구 - 웹 검색을 시뮬레이션합니다."""

from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """웹 검색을 수행합니다 (시뮬레이션).
    
    Args:
        query: 검색할 쿼리 문자열
    
    Returns:
        검색 결과를 문자열로 반환합니다.
    """
    # 실제 구현에서는 DuckDuckGo나 다른 검색 API를 사용할 수 있습니다
    return f"'{query}'에 대한 검색 결과:\n- 관련 정보 1\n- 관련 정보 2\n- 관련 정보 3"


WebSearchTool = web_search
