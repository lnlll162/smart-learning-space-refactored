"""
应用配置管理模块
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class AppConfig:
    """应用基础配置"""
    
    # Streamlit 页面配置
    PAGE_CONFIG = {
        "page_title": "5A智慧学习空间",
        "page_icon": "🎓",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "menu_items": {
            'Get Help': 'https://github.com/yourusername/your-repo',
            'Report a bug': "https://github.com/yourusername/your-repo/issues",
            'About': "# 5A智慧学习空间\n这是一个智能学习空间管理系统。"
        }
    }
    
    # 应用基本信息
    APP_NAME = "5A智慧学习空间数据大屏"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 安全配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
    LOCKOUT_TIME = int(os.getenv("LOCKOUT_TIME", "30"))  # 分钟
    
    # 文件路径
    USERS_FILE = "users.json"
    LOG_FILE = "app.log"
    
    # 日志配置
    LOG_CONFIG = {
        'filename': LOG_FILE,
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }


class DatabaseConfig:
    """数据库配置"""
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data.db')
    
    # 备用存储配置
    USE_JSON_STORAGE = os.getenv("USE_JSON_STORAGE", "True").lower() == "true"
    DATA_DIR = "data"
    

class AIConfig:
    """AI服务配置"""
    
    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL = "deepseek-chat"
    
    # OpenAI API 配置（备用）
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # API请求配置
    REQUEST_TIMEOUT = int(os.getenv("AI_REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", "3"))
    
    # AI响应配置
    MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))


class CacheConfig:
    """缓存配置"""
    
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 秒
    MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "1000"))
    
    # Redis配置（如果使用）
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    USE_REDIS = os.getenv("USE_REDIS", "False").lower() == "true"


class PerformanceConfig:
    """性能配置"""
    
    # 数据处理配置
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    
    # 限流配置
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))
    RATE_WINDOW = int(os.getenv("RATE_WINDOW", "60"))  # 秒


def get_config() -> Dict[str, Any]:
    """获取所有配置"""
    return {
        "app": AppConfig,
        "database": DatabaseConfig,
        "ai": AIConfig,
        "cache": CacheConfig,
        "performance": PerformanceConfig
    }


def get_settings() -> AppConfig:
    """获取应用设置"""
    return AppConfig()
