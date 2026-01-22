"""코드 품질 검사 도구 - 타입 체크 및 테스트 실행을 수행합니다."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool


def run_command(command: list[str], cwd: Optional[str] = None) -> tuple[str, str, int]:
    """명령어를 실행하고 결과를 반환합니다.
    
    Args:
        command: 실행할 명령어 리스트
        cwd: 작업 디렉토리 (기본값: 현재 디렉토리)
    
    Returns:
        (stdout, stderr, return_code) 튜플
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd or ".",
            timeout=300,  # 5분 타임아웃
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "오류: 명령어 실행 시간 초과 (5분)", 1
    except FileNotFoundError:
        return "", f"오류: '{command[0]}' 명령어를 찾을 수 없습니다. 설치되어 있는지 확인하세요.", 1
    except Exception as e:
        return "", f"명령어 실행 오류: {str(e)}", 1


def check_type_checker_available(checker: str) -> bool:
    """타입 체커가 설치되어 있는지 확인합니다.
    
    Args:
        checker: 체크할 타입 체커 이름 ("mypy", "pyright", 또는 "pyrefly")
    
    Returns:
        설치되어 있으면 True, 아니면 False
    """
    try:
        if checker == "mypy":
            subprocess.run(
                ["mypy", "--version"],
                capture_output=True,
                timeout=5,
            )
            return True
        elif checker == "pyright":
            subprocess.run(
                ["pyright", "--version"],
                capture_output=True,
                timeout=5,
            )
            return True
        elif checker == "pyrefly":
            subprocess.run(
                ["pyrefly", "--version"],
                capture_output=True,
                timeout=5,
            )
            return True
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@tool
def check_code_quality(
    target_path: str = ".",
    type_checker: str = "pyrefly",
    run_tests: bool = True,
) -> str:
    """코드 품질을 검사합니다 (타입 체크 + 테스트 실행).
    
    Args:
        target_path: 검사할 경로 (기본값: 현재 디렉토리)
        type_checker: 사용할 타입 체커 ("mypy", "pyright", 또는 "pyrefly", 기본값: "pyrefly")
        run_tests: 테스트를 실행할지 여부 (기본값: True)
    
    Returns:
        검사 결과를 구조화된 문자열로 반환합니다.
    """
    results: list[str] = []
    results.append("=" * 60)
    results.append("코드 품질 검사 시작")
    results.append("=" * 60)
    results.append("")
    
    # 경로 검증
    target = Path(target_path).resolve()
    if not target.exists():
        return f"오류: 경로 '{target_path}'을(를) 찾을 수 없습니다."
    
    # 타입 체크
    results.append("📋 타입 체크 실행 중...")
    type_checker_available = check_type_checker_available(type_checker)
    
    if not type_checker_available:
        results.append(
            f"⚠️  경고: '{type_checker}'가 설치되어 있지 않습니다."
        )
        results.append("")
        results.append("설치 방법:")
        results.append(f"  • pip: pip install {type_checker}")
        results.append(f"  • uv: uv add {type_checker}")
        results.append("")
        results.append("타입 체크를 건너뜁니다.")
        results.append("")
    else:
        if type_checker == "mypy":
            # mypy 실행
            # Python 파일만 검사하도록 설정
            command = [
                "mypy",
                str(target),
                "--ignore-missing-imports",
                "--no-strict-optional",
                "--show-error-codes",
            ]
        elif type_checker == "pyright":
            # pyright 실행
            command = [
                "pyright",
                str(target),
            ]
        elif type_checker == "pyrefly":
            # pyrefly 실행
            command = [
                "pyrefly",
                "check",
                str(target),
            ]
        else:
            results.append(f"⚠️  경고: 지원하지 않는 타입 체커 '{type_checker}'입니다.")
            results.append("")
            type_checker_available = False
            command = []  # 초기화
        
        if type_checker_available and command:
            stdout, stderr, return_code = run_command(command, cwd=str(target.parent))
            
            if return_code == 0:
                results.append("✅ 타입 체크 통과!")
                if stdout.strip():
                    results.append(stdout.strip())
            else:
                results.append("❌ 타입 체크 실패:")
                if stdout.strip():
                    results.append(stdout.strip())
                if stderr.strip():
                    results.append(stderr.strip())
            results.append("")
    
    # 테스트 실행
    if run_tests:
        results.append("🧪 테스트 실행 중...")
        
        # pytest가 설치되어 있는지 확인
        pytest_available = False
        try:
            subprocess.run(
                ["pytest", "--version"],
                capture_output=True,
                timeout=5,
            )
            pytest_available = True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pytest_available = False
        
        if not pytest_available:
            results.append(
                "⚠️  경고: pytest가 설치되어 있지 않습니다. "
                "설치하려면 'pip install pytest' 또는 'uv add pytest'를 실행하세요."
            )
            results.append("")
        else:
            # pytest 실행
            # 테스트 파일을 찾아서 실행
            command = [
                "pytest",
                str(target),
                "-v",
                "--tb=short",
            ]
            
            stdout, stderr, return_code = run_command(command, cwd=str(target.parent))
            
            # "no tests ran" 메시지 확인
            output_text = (stdout + stderr).lower()
            no_tests_ran = "no tests ran" in output_text or "collected 0 items" in output_text
            
            if no_tests_ran:
                results.append("ℹ️  테스트 파일이 없습니다.")
                results.append("테스트를 작성하려면 'test_'로 시작하는 파일을 만들거나 pytest를 사용하세요.")
                if stdout.strip():
                    # 간단한 정보만 표시
                    results.append("")
                    results.append("pytest 출력:")
                    results.append("\n".join(stdout.strip().split("\n")[-3:]))  # 마지막 몇 줄만
            elif return_code == 0:
                results.append("✅ 모든 테스트 통과!")
                if stdout.strip():
                    # 출력이 너무 길면 마지막 부분만 표시
                    output_lines = stdout.strip().split("\n")
                    if len(output_lines) > 50:
                        results.append("\n".join(output_lines[:10]))
                        results.append("...")
                        results.append("\n".join(output_lines[-10:]))
                    else:
                        results.append(stdout.strip())
            else:
                results.append("❌ 테스트 실패:")
                if stdout.strip():
                    output_lines = stdout.strip().split("\n")
                    if len(output_lines) > 100:
                        results.append("\n".join(output_lines[:20]))
                        results.append("...")
                        results.append("\n".join(output_lines[-20:]))
                    else:
                        results.append(stdout.strip())
                if stderr.strip():
                    results.append(stderr.strip())
            results.append("")
    
    # 요약
    results.append("=" * 60)
    results.append("코드 품질 검사 완료")
    results.append("=" * 60)
    
    return "\n".join(results)


CodeQualityTool = check_code_quality
