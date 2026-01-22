"""프롬프트 모듈 - 에이전트용 프롬프트 템플릿을 정의합니다."""

from .agent_prompts import (
    AGENT_SYSTEM_PROMPT,
    AGENT_USER_PROMPT_TEMPLATE,
)

__all__ = [
    "AGENT_SYSTEM_PROMPT",
    "AGENT_USER_PROMPT_TEMPLATE",
]
