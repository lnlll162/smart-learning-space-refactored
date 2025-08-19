"""
用户认证管理器
"""

import os
import json
import hashlib
import logging
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta

from ..config.settings import AppConfig
from ..config.constants import DEFAULT_USERS


class AuthManager:
    """用户认证管理器"""
    
    def __init__(self):
        self.users_file = AppConfig.USERS_FILE
        self.max_login_attempts = AppConfig.MAX_LOGIN_ATTEMPTS
        self.lockout_time = AppConfig.LOCKOUT_TIME
        self.login_attempts = {}  # 登录尝试记录
        self.init_users()
    
    def init_users(self):
        """初始化用户文件"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w", encoding='utf-8') as f:
                json.dump(DEFAULT_USERS, f, ensure_ascii=False, indent=2)
            logging.info("Created default users file")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_user(self, username: str, password: str) -> bool:
        """验证用户凭据"""
        # 检查是否被锁定
        if self._is_locked_out(username):
            return False
        
        try:
            with open(self.users_file, "r", encoding='utf-8') as f:
                users = json.load(f)
            
            is_valid = username in users and users[username] == self.hash_password(password)
            
            if is_valid:
                # 清除登录尝试记录
                self.login_attempts.pop(username, None)
                logging.info(f"User {username} logged in successfully")
            else:
                # 记录失败尝试
                self._record_failed_attempt(username)
                logging.warning(f"Failed login attempt for user {username}")
            
            return is_valid
            
        except Exception as e:
            logging.error(f"Error verifying user {username}: {str(e)}")
            return False
    
    def add_user(self, username: str, password: str) -> Tuple[bool, str]:
        """添加新用户"""
        try:
            # 验证用户名和密码
            if not self._validate_credentials(username, password):
                return False, "用户名或密码不符合要求"
            
            with open(self.users_file, "r", encoding='utf-8') as f:
                users = json.load(f)
            
            if username in users:
                return False, "用户名已存在"
            
            users[username] = self.hash_password(password)
            
            with open(self.users_file, "w", encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            
            logging.info(f"New user {username} registered")
            return True, "注册成功"
            
        except Exception as e:
            logging.error(f"Error adding user {username}: {str(e)}")
            return False, "系统错误"
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """修改用户密码"""
        try:
            # 验证旧密码
            if not self.verify_user(username, old_password):
                return False, "原密码错误"
            
            # 验证新密码
            if not self._validate_password(new_password):
                return False, "新密码不符合要求"
            
            with open(self.users_file, "r", encoding='utf-8') as f:
                users = json.load(f)
            
            users[username] = self.hash_password(new_password)
            
            with open(self.users_file, "w", encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Password changed for user {username}")
            return True, "密码修改成功"
            
        except Exception as e:
            logging.error(f"Error changing password for user {username}: {str(e)}")
            return False, "系统错误"
    
    def delete_user(self, username: str) -> Tuple[bool, str]:
        """删除用户"""
        try:
            # 不允许删除管理员用户
            if username == "admin":
                return False, "不能删除管理员用户"
            
            with open(self.users_file, "r", encoding='utf-8') as f:
                users = json.load(f)
            
            if username not in users:
                return False, "用户不存在"
            
            del users[username]
            
            with open(self.users_file, "w", encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            
            logging.info(f"User {username} deleted")
            return True, "用户删除成功"
            
        except Exception as e:
            logging.error(f"Error deleting user {username}: {str(e)}")
            return False, "系统错误"
    
    def list_users(self) -> list:
        """获取用户列表"""
        try:
            with open(self.users_file, "r", encoding='utf-8') as f:
                users = json.load(f)
            return list(users.keys())
        except Exception as e:
            logging.error(f"Error listing users: {str(e)}")
            return []
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        """验证用户名和密码格式"""
        # 用户名要求：3-20个字符，只能包含字母、数字、下划线
        if not (3 <= len(username) <= 20) or not username.replace('_', '').isalnum():
            return False
        
        return self._validate_password(password)
    
    def _validate_password(self, password: str) -> bool:
        """验证密码格式"""
        # 密码要求：至少6个字符
        return len(password) >= 6
    
    def _record_failed_attempt(self, username: str):
        """记录失败的登录尝试"""
        now = datetime.now()
        if username not in self.login_attempts:
            self.login_attempts[username] = []
        
        self.login_attempts[username].append(now)
        
        # 清理超过时间窗口的记录
        cutoff_time = now - timedelta(minutes=self.lockout_time)
        self.login_attempts[username] = [
            attempt for attempt in self.login_attempts[username]
            if attempt > cutoff_time
        ]
    
    def _is_locked_out(self, username: str) -> bool:
        """检查用户是否被锁定"""
        if username not in self.login_attempts:
            return False
        
        now = datetime.now()
        cutoff_time = now - timedelta(minutes=self.lockout_time)
        
        # 清理过期的尝试记录
        self.login_attempts[username] = [
            attempt for attempt in self.login_attempts[username]
            if attempt > cutoff_time
        ]
        
        return len(self.login_attempts[username]) >= self.max_login_attempts
    
    def get_lockout_info(self, username: str) -> Optional[Dict]:
        """获取锁定信息"""
        if not self._is_locked_out(username):
            return None
        
        attempts = self.login_attempts.get(username, [])
        if not attempts:
            return None
        
        latest_attempt = max(attempts)
        unlock_time = latest_attempt + timedelta(minutes=self.lockout_time)
        remaining_time = unlock_time - datetime.now()
        
        return {
            "attempts": len(attempts),
            "unlock_time": unlock_time,
            "remaining_minutes": max(0, remaining_time.total_seconds() / 60)
        }
