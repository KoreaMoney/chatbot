"""단위 변환 도구 - 다양한 단위 간 변환을 수행합니다."""

from langchain_core.tools import tool


@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """온도를 변환합니다.
    
    Args:
        value: 변환할 값
        from_unit: 원본 단위 ("celsius", "fahrenheit", "kelvin")
        to_unit: 변환할 단위 ("celsius", "fahrenheit", "kelvin")
    
    Returns:
        변환된 온도 값을 반환합니다.
    """
    try:
        # 먼저 켈빈으로 변환
        if from_unit.lower() == "celsius":
            kelvin = value + 273.15
        elif from_unit.lower() == "fahrenheit":
            kelvin = (value - 32) * 5/9 + 273.15
        elif from_unit.lower() == "kelvin":
            kelvin = value
        else:
            return "지원되지 않는 단위입니다. 'celsius', 'fahrenheit', 'kelvin' 중 하나를 선택하세요."
        
        # 켈빈에서 목표 단위로 변환
        if to_unit.lower() == "celsius":
            result = kelvin - 273.15
        elif to_unit.lower() == "fahrenheit":
            result = (kelvin - 273.15) * 9/5 + 32
        elif to_unit.lower() == "kelvin":
            result = kelvin
        else:
            return "지원되지 않는 단위입니다. 'celsius', 'fahrenheit', 'kelvin' 중 하나를 선택하세요."
        
        return f"{value}°{from_unit[0].upper()} = {result:.2f}°{to_unit[0].upper()}"
    except Exception as e:
        return f"온도 변환 오류: {str(e)}"


@tool
def convert_length(value: float, from_unit: str, to_unit: str) -> str:
    """길이를 변환합니다.
    
    Args:
        value: 변환할 값
        from_unit: 원본 단위 ("mm", "cm", "m", "km", "inch", "foot", "yard", "mile")
        to_unit: 변환할 단위 ("mm", "cm", "m", "km", "inch", "foot", "yard", "mile")
    
    Returns:
        변환된 길이 값을 반환합니다.
    """
    try:
        # 미터로 변환
        to_meter = {
            "mm": 0.001,
            "cm": 0.01,
            "m": 1.0,
            "km": 1000.0,
            "inch": 0.0254,
            "foot": 0.3048,
            "yard": 0.9144,
            "mile": 1609.34
        }
        
        if from_unit.lower() not in to_meter or to_unit.lower() not in to_meter:
            return "지원되지 않는 단위입니다. 'mm', 'cm', 'm', 'km', 'inch', 'foot', 'yard', 'mile' 중 하나를 선택하세요."
        
        meters = value * to_meter[from_unit.lower()]
        result = meters / to_meter[to_unit.lower()]
        
        return f"{value} {from_unit} = {result:.6f} {to_unit}"
    except Exception as e:
        return f"길이 변환 오류: {str(e)}"


@tool
def convert_weight(value: float, from_unit: str, to_unit: str) -> str:
    """무게를 변환합니다.
    
    Args:
        value: 변환할 값
        from_unit: 원본 단위 ("mg", "g", "kg", "ton", "ounce", "pound")
        to_unit: 변환할 단위 ("mg", "g", "kg", "ton", "ounce", "pound")
    
    Returns:
        변환된 무게 값을 반환합니다.
    """
    try:
        # 그램으로 변환
        to_gram = {
            "mg": 0.001,
            "g": 1.0,
            "kg": 1000.0,
            "ton": 1000000.0,
            "ounce": 28.3495,
            "pound": 453.592
        }
        
        if from_unit.lower() not in to_gram or to_unit.lower() not in to_gram:
            return "지원되지 않는 단위입니다. 'mg', 'g', 'kg', 'ton', 'ounce', 'pound' 중 하나를 선택하세요."
        
        grams = value * to_gram[from_unit.lower()]
        result = grams / to_gram[to_unit.lower()]
        
        return f"{value} {from_unit} = {result:.6f} {to_unit}"
    except Exception as e:
        return f"무게 변환 오류: {str(e)}"


TemperatureConverterTool = convert_temperature
LengthConverterTool = convert_length
WeightConverterTool = convert_weight
