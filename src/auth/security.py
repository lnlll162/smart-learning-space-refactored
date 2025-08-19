"""
安全工具类
"""

import secrets
import hashlib
import hmac
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

from ..config.settings import AppConfig, PerformanceConfig


class SecurityUtils:
    """安全工具类"""
    
    @staticmethod
    def generate_csrf_token() -> str:
        """生成CSRF令牌"""
        return secrets.token_hex(32)
    
    @staticmethod
    def validate_csrf_token(token: str, expected: str) -> bool:
        """验证CSRF令牌"""
        return secrets.compare_digest(token, expected)
    
    @staticmethod
    def hash_password_secure(password: str, salt: Optional[bytes] = None) -> tuple:
        """安全密码哈希（使用盐值）"""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 迭代次数
        )
        return salt + key, salt
    
    @staticmethod
    def verify_password_secure(stored_password: bytes, provided_password: str) -> bool:
        """验证安全密码"""
        salt = stored_password[:32]
        stored_key = stored_password[32:]
        
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt,
            100000
        )
        
        return stored_key == new_key
    
    @staticmethod
    def sign_data(data: str, secret_key: str) -> str:
        """数据签名"""
        return hmac.new(
            secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def verify_signature(data: str, signature: str, secret_key: str) -> bool:
        """验证数据签名"""
        expected_signature = SecurityUtils.sign_data(data, secret_key)
        return secrets.compare_digest(signature, expected_signature)


class RateLimiter:
    """限流器"""
    
    def __init__(self):
        self.requests = {}
        self.limit = PerformanceConfig.RATE_LIMIT
        self.window = PerformanceConfig.RATE_WINDOW
    
    def is_allowed(self, key: str, limit: Optional[int] = None, window: Optional[int] = None) -> bool:
        """检查是否允许请求"""
        current_time = time.time()
        limit = limit or self.limit
        window = window or self.window
        
        if key not in self.requests:
            self.requests[key] = []
        
        # 清理过期的请求记录
        cutoff_time = current_time - window
        self.requests[key] = [
            timestamp for timestamp in self.requests[key]
            if timestamp > cutoff_time
        ]
        
        # 检查是否超过限制
        if len(self.requests[key]) >= limit:
            logging.warning(f"Rate limit exceeded for key: {key}")
            return False
        
        # 记录当前请求
        self.requests[key].append(current_time)
        return True
    
    def get_remaining_requests(self, key: str) -> int:
        """获取剩余请求次数"""
        if key not in self.requests:
            return self.limit
        
        current_time = time.time()
        cutoff_time = current_time - self.window
        
        # 清理过期记录
        self.requests[key] = [
            timestamp for timestamp in self.requests[key]
            if timestamp > cutoff_time
        ]
        
        return max(0, self.limit - len(self.requests[key]))
    
    def reset_limit(self, key: str):
        """重置限制"""
        if key in self.requests:
            del self.requests[key]


class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """清理输入文本"""
        if not isinstance(text, str):
            return ""
        
        # 移除潜在的恶意字符
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        return text.strip()
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名格式"""
        if not isinstance(username, str):
            return False
        
        # 3-20个字符，只能包含字母、数字、下划线
        if not (3 <= len(username) <= 20):
            return False
        
        return username.replace('_', '').isalnum()
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if not isinstance(password, str):
            return False
        
        # 至少6个字符
        if len(password) < 6:
            return False
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        if not isinstance(email, str):
            return False
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class AuditLogger:
    """审计日志记录器"""
    
    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """设置审计日志器"""
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        handler = logging.FileHandler(self.log_file, encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_login(self, username: str, success: bool, ip: str = "unknown"):
        """记录登录事件"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"LOGIN {status} - User: {username}, IP: {ip}")
    
    def log_logout(self, username: str, ip: str = "unknown"):
        """记录登出事件"""
        self.logger.info(f"LOGOUT - User: {username}, IP: {ip}")
    
    def log_permission_change(self, admin_user: str, target_user: str, action: str):
        """记录权限变更"""
        self.logger.info(f"PERMISSION_CHANGE - Admin: {admin_user}, Target: {target_user}, Action: {action}")
    
    def log_data_access(self, username: str, resource: str, action: str):
        """记录数据访问"""
        self.logger.info(f"DATA_ACCESS - User: {username}, Resource: {resource}, Action: {action}")
    
    def log_security_event(self, event_type: str, details: str):
        """记录安全事件"""
        self.logger.warning(f"SECURITY_EVENT - Type: {event_type}, Details: {details}")


# 全局实例
rate_limiter = RateLimiter()
audit_logger = AuditLogger()
