"""병원 예약 도구 - 병원 예약 관련 기능을 제공합니다."""

from langchain_core.tools import tool


@tool
def search_hospitals(location: str, department: str = "") -> str:
    """병원을 검색합니다.
    
    Args:
        location: 병원 위치 (도시명 또는 지역명)
        department: 진료과 (선택사항, 예: "내과", "외과", "정형외과", "산부인과", "소아과", "이비인후과", "안과", "치과", "피부과", "정신건강의학과")
    
    Returns:
        병원 검색 결과를 반환합니다.
    """
    try:
        hospitals = [
            {
                "name": f"{location} 종합병원",
                "address": f"{location}시 중앙로 123",
                "departments": ["내과", "외과", "정형외과", "산부인과", "소아과", "이비인후과", "안과", "피부과"],
                "rating": 4.6,
                "phone": "02-1234-5678",
                "hours": "평일 09:00-18:00, 토요일 09:00-13:00"
            },
            {
                "name": f"{location} 대학병원",
                "address": f"{location}시 대학로 456",
                "departments": ["내과", "외과", "정형외과", "산부인과", "소아과", "이비인후과", "안과", "치과", "피부과", "정신건강의학과"],
                "rating": 4.8,
                "phone": "02-2345-6789",
                "hours": "평일 08:30-17:30, 토요일 08:30-12:30"
            },
            {
                "name": f"{location} 의원",
                "address": f"{location}시 상가로 789",
                "departments": ["내과", "소아과", "이비인후과"],
                "rating": 4.4,
                "phone": "02-3456-7890",
                "hours": "평일 09:00-19:00, 토요일 09:00-15:00"
            }
        ]
        
        # 진료과 필터링
        if department:
            department_str = str(department)
            hospitals = [
                h
                for h in hospitals
                if isinstance(depts := h.get("departments", []), list)
                and department_str in depts
            ]
        
        if not hospitals:
            return f"{location} 지역에서 {department} 진료과가 있는 병원을 찾을 수 없습니다."
        
        result = f"""{location} 지역 병원 검색 결과:
{f'{department} 진료과가 있는 병원' if department else ''}

"""
        for i, hospital in enumerate(hospitals, 1):
            result += f"""{i}. {hospital['name']}
   주소: {hospital['address']}
   평점: {'⭐' * int(hospital['rating'])} ({hospital['rating']})
   전화: {hospital['phone']}
   진료 시간: {hospital['hours']}
   진료과: {', '.join(hospital['departments'])}
   
"""
        
        return result
    
    except Exception as e:
        return f"병원 검색 오류: {str(e)}"


@tool
def get_department_info(department: str) -> str:
    """진료과 정보를 조회합니다.
    
    Args:
        department: 진료과명 (예: "내과", "외과", "정형외과", "산부인과", "소아과", "이비인후과", "안과", "치과", "피부과", "정신건강의학과")
    
    Returns:
        진료과 정보를 반환합니다.
    """
    try:
        department_info = {
            "내과": {
                "description": "내부 장기 질환을 진단하고 치료합니다.",
                "common_conditions": ["감기", "고혈압", "당뇨", "위염", "간질환", "신장질환"],
                "typical_duration": "30분~1시간"
            },
            "외과": {
                "description": "수술이 필요한 질환을 진단하고 치료합니다.",
                "common_conditions": ["맹장염", "담석", "탈장", "종양 제거"],
                "typical_duration": "1시간~2시간"
            },
            "정형외과": {
                "description": "뼈, 관절, 근육 질환을 진단하고 치료합니다.",
                "common_conditions": ["허리 디스크", "무릎 관절염", "골절", "어깨 통증"],
                "typical_duration": "30분~1시간"
            },
            "산부인과": {
                "description": "여성 생식기 질환과 임신, 출산을 관리합니다.",
                "common_conditions": ["산전 검진", "부인과 질환", "생리 불순", "갱년기"],
                "typical_duration": "30분~1시간"
            },
            "소아과": {
                "description": "소아 및 청소년 질환을 진단하고 치료합니다.",
                "common_conditions": ["소아 감기", "예방접종", "성장 발달 상담", "알레르기"],
                "typical_duration": "20분~40분"
            },
            "이비인후과": {
                "description": "귀, 코, 목 질환을 진단하고 치료합니다.",
                "common_conditions": ["중이염", "비염", "축농증", "인후통", "알레르기성 비염"],
                "typical_duration": "20분~40분"
            },
            "안과": {
                "description": "눈 질환을 진단하고 치료합니다.",
                "common_conditions": ["시력 검사", "녹내장", "백내장", "안구 건조증", "알레르기성 결막염"],
                "typical_duration": "30분~1시간"
            },
            "치과": {
                "description": "치아 및 구강 질환을 진단하고 치료합니다.",
                "common_conditions": ["충치 치료", "스케일링", "임플란트", "교정", "발치"],
                "typical_duration": "30분~2시간"
            },
            "피부과": {
                "description": "피부 질환을 진단하고 치료합니다.",
                "common_conditions": ["여드름", "아토피", "습진", "알레르기", "모발 질환"],
                "typical_duration": "20분~40분"
            },
            "정신건강의학과": {
                "description": "정신 건강 및 정신 질환을 진단하고 치료합니다.",
                "common_conditions": ["우울증", "불안장애", "불면증", "스트레스 관리", "상담"],
                "typical_duration": "30분~1시간"
            }
        }
        
        info = department_info.get(department)
        if not info:
            return f"'{department}' 진료과 정보를 찾을 수 없습니다. 지원되는 진료과: {', '.join(department_info.keys())}"
        
        result = f"""{department} 진료과 정보:

설명: {info['description']}

주요 진료 질환:
{chr(10).join(f'- {condition}' for condition in info['common_conditions'])}

일반적인 진료 시간: {info['typical_duration']}

예약을 도와드릴까요?"""
        
        return result
    
    except Exception as e:
        return f"진료과 정보 조회 오류: {str(e)}"


@tool
def check_hospital_availability(hospital_name: str, department: str, date: str, 
                               time: str = "") -> str:
    """병원 예약 가능 시간을 확인합니다.
    
    Args:
        hospital_name: 병원 이름
        department: 진료과
        date: 예약 날짜 (YYYY-MM-DD 형식)
        time: 희망 시간 (HH:MM 형식, 선택사항)
    
    Returns:
        예약 가능 시간 정보를 반환합니다.
    """
    try:
        # 실제 구현에서는 병원 예약 시스템과 연동
        available_times = [
            "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
            "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"
        ]
        
        result = f"""{hospital_name} {department} 예약 가능 시간:

예약 날짜: {date}

예약 가능한 시간:
{chr(10).join(f'- {t}' for t in available_times)}
"""
        
        if time:
            if time in available_times:
                result += f"\n✅ {time} 시간대 예약이 가능합니다."
            else:
                result += f"\n⚠️ {time} 시간대는 예약이 불가능합니다. 위의 시간 중에서 선택해주세요."
        
        result += "\n원하시는 시간을 알려주시면 예약을 진행해드리겠습니다."
        
        return result
    
    except Exception as e:
        return f"예약 가능 시간 확인 오류: {str(e)}"


SearchHospitalsTool = search_hospitals
GetDepartmentInfoTool = get_department_info
CheckHospitalAvailabilityTool = check_hospital_availability
