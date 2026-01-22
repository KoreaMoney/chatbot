"""테스트 코드 생성 도구 - 소스 코드를 분석하여 테스트 코드를 자동 생성합니다."""

import ast
import inspect
import json
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool


def analyze_python_file(file_path: str) -> dict:
    """Python 파일을 분석하여 함수, 클래스, 메서드 정보를 추출합니다.
    
    Args:
        file_path: 분석할 Python 파일 경로
    
    Returns:
        분석 결과 딕셔너리 (functions, classes, imports 등)
    """
    try:
        full_path = Path(file_path).resolve()
        current_dir = Path.cwd().resolve()
        
        # 보안: 현재 작업 디렉토리 내의 파일만 허용
        try:
            full_path.relative_to(current_dir)
        except ValueError:
            return {"error": "현재 작업 디렉토리 외부의 파일은 분석할 수 없습니다."}
        
        if not full_path.exists():
            return {"error": f"파일 '{file_path}'을(를) 찾을 수 없습니다."}
        
        if not full_path.is_file():
            return {"error": f"'{file_path}'은(는) 파일이 아닙니다."}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {"error": f"파일 구문 오류: {str(e)}"}
        
        analysis = {
            "file_path": str(full_path),
            "functions": [],
            "classes": [],
            "imports": [],
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 함수 정보 추출
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                }
                
                # docstring 추출
                docstring = ast.get_docstring(node)
                if docstring:
                    func_info["docstring"] = docstring
                
                # 데코레이터 확인 (예: @tool)
                func_info["decorators"] = []
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        func_info["decorators"].append(decorator.id)
                    elif isinstance(decorator, ast.Attribute):
                        func_info["decorators"].append(f"{decorator.attr}")
                
                analysis["functions"].append(func_info)
            
            elif isinstance(node, ast.ClassDef):
                # 클래스 정보 추출
                class_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [],
                }
                
                # docstring 추출
                docstring = ast.get_docstring(node)
                if docstring:
                    class_info["docstring"] = docstring
                
                # 메서드 추출
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            "name": item.name,
                            "line": item.lineno,
                            "args": [arg.arg for arg in item.args.args],
                        }
                        method_docstring = ast.get_docstring(item)
                        if method_docstring:
                            method_info["docstring"] = method_docstring
                        class_info["methods"].append(method_info)
                
                analysis["classes"].append(class_info)
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    analysis["imports"].append(f"{module}.{alias.name}")
        
        return analysis
    
    except Exception as e:
        return {"error": f"파일 분석 오류: {str(e)}"}


@tool
def generate_test_code(
    source_file_path: str,
    test_file_path: Optional[str] = None,
    test_framework: str = "pytest",
) -> str:
    """소스 코드 파일을 분석하여 테스트 코드를 생성합니다.
    
    이 도구는 소스 파일을 분석하고, 함수와 클래스를 파악한 후,
    적절한 테스트 코드 생성 가이드를 제공합니다.
    실제 테스트 코드 생성은 agent의 LLM이 수행합니다.
    
    Args:
        source_file_path: 테스트를 생성할 소스 파일 경로
        test_file_path: 생성할 테스트 파일 경로 (기본값: 자동 생성)
        test_framework: 사용할 테스트 프레임워크 ("pytest" 또는 "unittest", 기본값: "pytest")
    
    Returns:
        테스트 코드 생성 가이드 및 분석 결과
    """
    # 파일 분석
    analysis = analyze_python_file(source_file_path)
    
    if "error" in analysis:
        return f"오류: {analysis['error']}"
    
    # 테스트 파일 경로 자동 생성
    if not test_file_path:
        source_path = Path(source_file_path)
        # tools/calculator_tool.py -> tests/test_calculator_tool.py
        # nodes/agent_nodes.py -> tests/test_agent_nodes.py
        if "tools" in str(source_path):
            test_file_path = f"tests/test_{source_path.stem}.py"
        elif "nodes" in str(source_path):
            test_file_path = f"tests/test_{source_path.stem}.py"
        else:
            test_file_path = f"tests/test_{source_path.stem}.py"
    
    # 분석 결과 요약
    result: list[str] = []
    result.append("=" * 60)
    result.append("테스트 코드 생성 가이드")
    result.append("=" * 60)
    result.append("")
    result.append(f"소스 파일: {analysis['file_path']}")
    result.append(f"테스트 파일: {test_file_path}")
    result.append(f"테스트 프레임워크: {test_framework}")
    result.append("")
    
    # 함수 정보
    if analysis["functions"]:
        result.append(f"📋 발견된 함수 ({len(analysis['functions'])}개):")
        for func in analysis["functions"]:
            result.append(f"  • {func['name']}({', '.join(func['args'])})")
            if "docstring" in func:
                doc = func["docstring"].split("\n")[0] if func["docstring"] else ""
                if doc:
                    result.append(f"    설명: {doc}")
        result.append("")
    
    # 클래스 정보
    if analysis["classes"]:
        result.append(f"📋 발견된 클래스 ({len(analysis['classes'])}개):")
        for cls in analysis["classes"]:
            result.append(f"  • {cls['name']}")
            if "docstring" in cls:
                doc = cls["docstring"].split("\n")[0] if cls["docstring"] else ""
                if doc:
                    result.append(f"    설명: {doc}")
            if cls["methods"]:
                result.append(f"    메서드: {', '.join([m['name'] for m in cls['methods']])}")
        result.append("")
    
    # 테스트 코드 생성 가이드
    result.append("=" * 60)
    result.append("테스트 코드 생성 지침")
    result.append("=" * 60)
    result.append("")
    result.append("다음과 같은 테스트 코드를 생성해야 합니다:")
    result.append("")
    
    if test_framework == "pytest":
        result.append("1. pytest를 사용하여 테스트를 작성하세요.")
        result.append("2. 각 함수와 메서드에 대해 테스트 함수를 작성하세요.")
        result.append("3. 테스트 함수 이름은 'test_'로 시작해야 합니다.")
        result.append("4. 일반적인 케이스, 엣지 케이스, 오류 케이스를 모두 테스트하세요.")
        result.append("5. @pytest.fixture를 사용하여 공통 설정을 재사용하세요.")
        result.append("")
        result.append("예시 구조:")
        result.append("```python")
        result.append("import pytest")
        result.append("from your_module import your_function")
        result.append("")
        result.append("def test_your_function_basic():")
        result.append("    # 일반적인 케이스 테스트")
        result.append("    result = your_function('input')")
        result.append("    assert result == 'expected'")
        result.append("")
        result.append("def test_your_function_edge_case():")
        result.append("    # 엣지 케이스 테스트")
        result.append("    ...")
        result.append("")
        result.append("def test_your_function_error():")
        result.append("    # 오류 케이스 테스트")
        result.append("    with pytest.raises(ValueError):")
        result.append("        your_function('invalid')")
        result.append("```")
    else:
        result.append("1. unittest를 사용하여 테스트를 작성하세요.")
        result.append("2. unittest.TestCase를 상속받는 테스트 클래스를 작성하세요.")
        result.append("3. 각 테스트 메서드는 'test_'로 시작해야 합니다.")
        result.append("4. 일반적인 케이스, 엣지 케이스, 오류 케이스를 모두 테스트하세요.")
        result.append("")
        result.append("예시 구조:")
        result.append("```python")
        result.append("import unittest")
        result.append("from your_module import your_function")
        result.append("")
        result.append("class TestYourFunction(unittest.TestCase):")
        result.append("    def test_basic(self):")
        result.append("        # 일반적인 케이스 테스트")
        result.append("        result = your_function('input')")
        result.append("        self.assertEqual(result, 'expected')")
        result.append("```")
    
    result.append("")
    result.append("=" * 60)
    result.append("다음 단계")
    result.append("=" * 60)
    result.append("")
    result.append(f"1. 소스 파일 '{source_file_path}'의 내용을 확인하세요.")
    result.append(f"2. 위의 분석 결과를 바탕으로 테스트 코드를 작성하세요.")
    result.append(f"3. 테스트 파일 '{test_file_path}'에 테스트 코드를 저장하세요.")
    result.append("4. 테스트를 실행하여 모든 테스트가 통과하는지 확인하세요.")
    result.append("")
    
    # 상세 분석 정보 (JSON 형태로 제공)
    result.append("=" * 60)
    result.append("상세 분석 정보")
    result.append("=" * 60)
    result.append("")
    result.append(json.dumps(analysis, ensure_ascii=False, indent=2))
    
    return "\n".join(result)


TestGeneratorTool = generate_test_code
