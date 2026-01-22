"""코드 품질 검사 노드 - Agent 시작 시 자동으로 코드 품질을 검사합니다."""

import json
import logging
from datetime import datetime
from pathlib import Path

from tools.code_quality_tool import check_code_quality

logger = logging.getLogger(__name__)

CONFIG_FILE = "code_quality_config.json"


def _is_code_quality_enabled(project_root: Path) -> bool:
    """code_quality_config.json에서 enabled 여부를 읽습니다. 없거나 오류면 True(기본 켜짐)."""
    config_path = project_root / CONFIG_FILE
    if not config_path.exists():
        return True
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("enabled", True) is not False
    except Exception:
        return True


def code_quality_check_node(state: dict) -> dict:
    """코드 품질 검사 노드 - Agent 시작 시 한 번만 자동으로 코드 품질을 검사합니다.
    
    이 노드는 Agent 그래프의 시작 부분에서 실행되어 프로젝트의 코드 품질을
    자동으로 검사합니다. 각 스레드(대화 세션)마다 한 번씩만 실행됩니다.
    타입 체크와 테스트를 실행하고 결과를 로그로 출력합니다.
    대시보드에서 코드 품질 검사를 끄면(enable=false) 검사를 수행하지 않습니다.
    
    Args:
        state: 에이전트 상태
    
    Returns:
        상태 업데이트 (code_quality_checked 플래그 설정)
    """
    # 이미 이 스레드에서 실행된 적이 있는지 확인
    if state.get("code_quality_checked", False):
        logger.info("이 스레드에서 코드 품질 검사는 이미 실행되었습니다. 스킵합니다.")
        print("ℹ️  이 스레드에서 코드 품질 검사는 이미 실행되었습니다. 스킵합니다.")
        return state

    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent  # nodes/ -> project_root/

    # 대시보드에서 끄면 검사하지 않음
    if not _is_code_quality_enabled(project_root):
        logger.info("코드 품질 검사가 비활성화되어 있습니다. 스킵합니다.")
        print("ℹ️  코드 품질 검사가 꺼져 있어 검사를 건너뜁니다.")
        state["code_quality_checked"] = True
        return state
    
    try:
        history_file = project_root / "code_quality_history.json"
        logger.info("코드 품질 검사 시작...")
        
        # 코드 품질 검사 실행
        result = check_code_quality.invoke({
            "target_path": str(project_root),
            "type_checker": "pyrefly",
            "run_tests": True,
        })
        
        # 결과를 로그로 출력
        logger.info("코드 품질 검사 결과:\n" + result)
        
        # 콘솔에도 출력 (개발 중 확인용)
        print("\n" + "=" * 60)
        print("코드 품질 검사 결과")
        print("=" * 60)
        print(result)
        print("=" * 60 + "\n")
        
        # 결과를 히스토리 파일에 저장
        try:
            timestamp = datetime.now().isoformat()
            
            # 결과에서 성공/실패 여부 파싱
            type_check_passed = "✅ 타입 체크 통과!" in result
            tests_passed = "✅ 모든 테스트 통과!" in result
            has_errors = "❌" in result
            
            # 기존 히스토리 읽기
            history = []
            if history_file.exists():
                try:
                    with open(history_file, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []
            
            # 새 항목 추가
            new_entry = {
                "timestamp": timestamp,
                "result": result,
                "type_check_passed": type_check_passed,
                "tests_passed": tests_passed,
                "has_errors": has_errors,
            }
            
            # 최대 50개까지만 저장 (오래된 항목 제거)
            history.insert(0, new_entry)
            if len(history) > 50:
                history = history[:50]
            
            # 히스토리 저장
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            logger.info(f"코드 품질 검사 결과가 {history_file}에 저장되었습니다.")
        except Exception as save_error:
            logger.warning(f"코드 품질 검사 결과 저장 실패: {str(save_error)}")
        
    except Exception as e:
        # 검사 실패 시에도 Agent는 정상 작동하도록 에러만 로그
        logger.error(f"코드 품질 검사 중 오류 발생: {str(e)}", exc_info=True)
        print(f"⚠️  코드 품질 검사 중 오류 발생: {str(e)}")
        
        # 오류도 히스토리에 저장
        try:
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent
            history_file = project_root / "code_quality_history.json"
            timestamp = datetime.now().isoformat()
            
            history = []
            if history_file.exists():
                try:
                    with open(history_file, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []
            
            error_entry = {
                "timestamp": timestamp,
                "result": f"오류 발생: {str(e)}",
                "type_check_passed": False,
                "tests_passed": False,
                "has_errors": True,
            }
            
            history.insert(0, error_entry)
            if len(history) > 50:
                history = history[:50]
            
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    # 이 스레드에서 코드 품질 검사를 실행했음을 표시
    state["code_quality_checked"] = True
    
    # 상태 반환 (메시지 흐름 유지)
    return state
