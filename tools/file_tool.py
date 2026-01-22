"""파일 처리 도구 - 파일 읽기/쓰기 작업을 수행합니다."""

import os
from pathlib import Path
from langchain_core.tools import tool


@tool
def read_file(file_path: str) -> str:
    """파일을 읽습니다.
    
    Args:
        file_path: 읽을 파일의 경로
    
    Returns:
        파일 내용을 반환합니다.
    """
    try:
        # 보안을 위해 현재 작업 디렉토리 내의 파일만 허용
        full_path = Path(file_path).resolve()
        current_dir = Path.cwd().resolve()
        
        # 상위 디렉토리 접근 방지
        try:
            full_path.relative_to(current_dir)
        except ValueError:
            return "오류: 현재 작업 디렉토리 외부의 파일은 읽을 수 없습니다."
        
        if not full_path.exists():
            return f"오류: 파일 '{file_path}'을(를) 찾을 수 없습니다."
        
        if not full_path.is_file():
            return f"오류: '{file_path}'은(는) 파일이 아닙니다."
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"파일 '{file_path}' 내용:\n\n{content}"
    except PermissionError:
        return f"오류: 파일 '{file_path}'에 대한 읽기 권한이 없습니다."
    except Exception as e:
        return f"파일 읽기 오류: {str(e)}"


@tool
def write_file(file_path: str, content: str, mode: str = "write") -> str:
    """파일에 내용을 씁니다.
    
    Args:
        file_path: 쓸 파일의 경로
        content: 파일에 쓸 내용
        mode: 쓰기 모드 ("write" - 덮어쓰기, "append" - 추가)
    
    Returns:
        작업 결과를 반환합니다.
    """
    try:
        # 보안을 위해 현재 작업 디렉토리 내의 파일만 허용
        full_path = Path(file_path).resolve()
        current_dir = Path.cwd().resolve()
        
        # 상위 디렉토리 접근 방지
        try:
            full_path.relative_to(current_dir)
        except ValueError:
            return "오류: 현재 작업 디렉토리 외부의 파일은 쓸 수 없습니다."
        
        # 디렉토리가 없으면 생성
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        write_mode = 'w' if mode == "write" else 'a'
        with open(full_path, write_mode, encoding='utf-8') as f:
            f.write(content)
        
        action = "쓰기" if mode == "write" else "추가"
        return f"파일 '{file_path}'에 {action} 완료."
    except PermissionError:
        return f"오류: 파일 '{file_path}'에 대한 쓰기 권한이 없습니다."
    except Exception as e:
        return f"파일 쓰기 오류: {str(e)}"


@tool
def list_files(directory: str = ".") -> str:
    """디렉토리의 파일 목록을 가져옵니다.
    
    Args:
        directory: 목록을 가져올 디렉토리 (기본값: 현재 디렉토리)
    
    Returns:
        파일 목록을 반환합니다.
    """
    try:
        # 보안을 위해 현재 작업 디렉토리 내의 디렉토리만 허용
        full_path = Path(directory).resolve()
        current_dir = Path.cwd().resolve()
        
        # 상위 디렉토리 접근 방지
        try:
            full_path.relative_to(current_dir)
        except ValueError:
            return "오류: 현재 작업 디렉토리 외부의 디렉토리는 조회할 수 없습니다."
        
        if not full_path.exists():
            return f"오류: 디렉토리 '{directory}'을(를) 찾을 수 없습니다."
        
        if not full_path.is_dir():
            return f"오류: '{directory}'은(는) 디렉토리가 아닙니다."
        
        files = []
        dirs = []
        
        for item in sorted(full_path.iterdir()):
            if item.is_file():
                files.append(f"📄 {item.name}")
            elif item.is_dir():
                dirs.append(f"📁 {item.name}/")
        
        result = f"디렉토리 '{directory}' 내용:\n\n"
        if dirs:
            result += "디렉토리:\n" + "\n".join(dirs) + "\n\n"
        if files:
            result += "파일:\n" + "\n".join(files)
        
        if not dirs and not files:
            result += "(비어있음)"
        
        return result
    except PermissionError:
        return f"오류: 디렉토리 '{directory}'에 대한 읽기 권한이 없습니다."
    except Exception as e:
        return f"디렉토리 조회 오류: {str(e)}"


ReadFileTool = read_file
WriteFileTool = write_file
ListFilesTool = list_files
