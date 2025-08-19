"""
装饰器工具
"""

import time
import functools
import streamlit as st
from typing import Callable, Any

from ..auth.security import rate_limiter


def rate_limit_decorator(key_func: Callable = None, limit: int = 10, window: int = 60):
    """限流装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成限流键
            if key_func:
                rate_key = key_func(*args, **kwargs)
            else:
                # 使用用户session或IP作为键
                rate_key = st.session_state.get('username', 'anonymous')
            
            # 检查限流
            if not rate_limiter.is_allowed(rate_key, limit, window):
                st.error(f"操作过于频繁，请等待{window}秒后再试")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def login_required(func: Callable) -> Callable:
    """登录验证装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('logged_in', False):
            st.warning("请先登录")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def performance_monitor(func: Callable) -> Callable:
    """性能监控装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if execution_time > 1.0:  # 超过1秒的操作记录警告
            st.warning(f"操作 {func.__name__} 执行时间较长: {execution_time:.2f}秒")
        
        return result
    return wrapper
