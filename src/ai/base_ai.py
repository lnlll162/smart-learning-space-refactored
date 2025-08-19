"""
AI服务基类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging


class BaseAI(ABC):
    """AI服务抽象基类"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        生成AI响应
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            **kwargs: 其他参数
        
        Returns:
            包含响应内容的字典
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        pass
    
    def format_error_response(self, error: str) -> Dict[str, Any]:
        """格式化错误响应"""
        return {
            "success": False,
            "error": error,
            "content": f"抱歉，服务暂时不可用：{error}"
        }
    
    def format_success_response(self, content: str, **metadata) -> Dict[str, Any]:
        """格式化成功响应"""
        return {
            "success": True,
            "content": content,
            "metadata": metadata
        }
    
    def log_request(self, messages: List[Dict[str, str]]):
        """记录请求日志"""
        user_message = next(
            (msg["content"] for msg in messages if msg["role"] == "user"),
            "No user message"
        )
        self.logger.info(f"AI request: {user_message[:100]}...")
    
    def log_response(self, response: Dict[str, Any]):
        """记录响应日志"""
        if response.get("success"):
            content = response.get("content", "")
            self.logger.info(f"AI response: {content[:100]}...")
        else:
            error = response.get("error", "Unknown error")
            self.logger.error(f"AI error: {error}")


class AIError(Exception):
    """AI服务异常"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class APIError(AIError):
    """API错误"""
    pass


class ConfigError(AIError):
    """配置错误"""
    pass


class RateLimitError(AIError):
    """限流错误"""
    pass
