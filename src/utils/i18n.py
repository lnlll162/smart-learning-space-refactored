"""
国际化支持
"""

import streamlit as st
from ..config.constants import TEXT_MAP


def get_text(key: str) -> str:
    """获取多语言文本"""
    language = st.session_state.get("language", "zh")
    
    if key in TEXT_MAP:
        return TEXT_MAP[key].get(language, TEXT_MAP[key].get("zh", key))
    
    return key


def set_language(language: str):
    """设置语言"""
    if language in ["zh", "en"]:
        st.session_state.language = language
    else:
        st.session_state.language = "zh"


def get_available_languages() -> dict:
    """获取可用语言列表"""
    return {
        "zh": "中文",
        "en": "English"
    }
