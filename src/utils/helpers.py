"""
通用工具函数
"""

import time
import logging
import functools
from typing import Any, Callable, Dict, Optional
import pandas as pd
from io import BytesIO
import streamlit as st


def safe_data_operation(func: Callable) -> Callable:
    """安全数据操作装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            st.error(f"数据操作失败: {str(e)}")
            return None
    return wrapper


def cached_operation(ttl: int = 300):
    """缓存操作装饰器"""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            current_time = time.time()
            
            # 检查缓存
            if cache_key in cache:
                cached_time, cached_result = cache[cache_key]
                if current_time - cached_time < ttl:
                    return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache[cache_key] = (current_time, result)
            
            # 清理过期缓存
            expired_keys = [
                key for key, (cached_time, _) in cache.items()
                if current_time - cached_time >= ttl
            ]
            for key in expired_keys:
                del cache[key]
            
            return result
        
        return wrapper
    return decorator


@safe_data_operation
def export_data(data: pd.DataFrame, filename: str = "data_export", format_type: str = "csv") -> BytesIO:
    """导出数据"""
    buffer = BytesIO()
    
    if format_type.lower() == "csv":
        csv_data = data.to_csv(index=False, encoding='utf-8-sig')
        buffer.write(csv_data.encode('utf-8-sig'))
    
    elif format_type.lower() == "excel":
        data.to_excel(buffer, index=False, engine='openpyxl')
    
    elif format_type.lower() == "json":
        json_data = data.to_json(orient='records', ensure_ascii=False, indent=2)
        buffer.write(json_data.encode('utf-8'))
    
    buffer.seek(0)
    return buffer


def format_number(value: float, precision: int = 2, percentage: bool = False) -> str:
    """格式化数字"""
    if value is None:
        return "N/A"
    
    if percentage:
        return f"{value:.{precision}%}"
    else:
        return f"{value:,.{precision}f}"


def format_duration(minutes: int) -> str:
    """格式化时长"""
    if minutes < 60:
        return f"{minutes}分钟"
    elif minutes < 1440:  # 小于24小时
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}小时{mins}分钟"
    else:
        days = minutes // 1440
        hours = (minutes % 1440) // 60
        return f"{days}天{hours}小时"


def generate_color_palette(n_colors: int) -> list:
    """生成颜色调色板"""
    default_colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]
    
    if n_colors <= len(default_colors):
        return default_colors[:n_colors]
    
    # 如果需要更多颜色，生成渐变色
    import colorsys
    colors = []
    for i in range(n_colors):
        hue = i / n_colors
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(hex_color)
    
    return colors


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> tuple:
    """验证DataFrame格式"""
    if df is None or df.empty:
        return False, "数据为空"
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"缺少必要的列: {missing_columns}"
    
    return True, "验证通过"


def log_user_activity(username: str, action: str, timestamp, details: Optional[Dict[str, Any]] = None):
    """记录用户活动"""
    logger = logging.getLogger("user_activity")
    log_msg = f"User {username} - {action} at {timestamp}"
    if details:
        log_msg += f" - {details}"
    logger.info(log_msg)
