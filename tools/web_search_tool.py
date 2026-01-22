"""웹 검색 도구 - DuckDuckGo를 사용한 실제 웹 검색을 수행합니다."""

from langchain_core.tools import tool
from duckduckgo_search import DDGS


@tool
def web_search(query: str) -> str:
    """웹 검색을 수행합니다.
    
    Args:
        query: 검색할 쿼리 문자열
    
    Returns:
        검색 결과를 문자열로 반환합니다.
    """
    try:
        with DDGS() as ddgs:
            # 최대 5개의 검색 결과를 가져옵니다
            results = list(ddgs.text(query, max_results=5))
            
            if not results:
                return f"'{query}'에 대한 검색 결과를 찾을 수 없습니다."
            
            # 검색 결과를 포맷팅합니다
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get("title", "제목 없음")
                body = result.get("body", "내용 없음")
                href = result.get("href", "")
                
                formatted_results.append(
                    f"{i}. {title}\n   {body[:200]}...\n   출처: {href}"
                )
            
            return f"'{query}'에 대한 검색 결과:\n\n" + "\n\n".join(formatted_results)
    
    except Exception as e:
        return f"웹 검색 중 오류가 발생했습니다: {str(e)}"


WebSearchTool = web_search
