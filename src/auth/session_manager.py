"""
会话管理器
"""

import os
import json
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

from ..config.settings import AppConfig


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self.session_file = "sessions.json"
        self.session_timeout = 3600  # 会话超时时间（秒）
        self.init_sessions()
    
    def init_sessions(self):
        """初始化会话文件"""
        if not os.path.exists(self.session_file):
            with open(self.session_file, "w", encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def create_session(self, username: str, user_data: Optional[Dict] = None) -> str:
        """创建新会话"""
        session_id = secrets.token_hex(32)
        session_data = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "user_data": user_data or {}
        }
        
        if self._save_session(session_id, session_data):
            logging.info(f"Session created for user {username}")
            return session_id
        return ""
    
    def validate_session(self, session_id: str) -> Optional[Dict]:
        """验证会话有效性"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            if session_id not in sessions:
                return None
            
            session_data = sessions[session_id]
            last_activity = datetime.fromisoformat(session_data["last_activity"])
            
            # 检查会话是否超时
            if datetime.now() - last_activity > timedelta(seconds=self.session_timeout):
                self.destroy_session(session_id)
                return None
            
            # 更新最后活动时间
            session_data["last_activity"] = datetime.now().isoformat()
            sessions[session_id] = session_data
            
            with open(self.session_file, "w", encoding='utf-8') as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)
            
            return session_data
            
        except Exception as e:
            logging.error(f"Error validating session {session_id}: {str(e)}")
            return None
    
    def update_session(self, session_id: str, data: Dict) -> bool:
        """更新会话数据"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            if session_id not in sessions:
                return False
            
            sessions[session_id]["user_data"].update(data)
            sessions[session_id]["last_activity"] = datetime.now().isoformat()
            
            with open(self.session_file, "w", encoding='utf-8') as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Error updating session {session_id}: {str(e)}")
            return False
    
    def destroy_session(self, session_id: str) -> bool:
        """销毁会话"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            if session_id in sessions:
                username = sessions[session_id].get("username", "unknown")
                del sessions[session_id]
                
                with open(self.session_file, "w", encoding='utf-8') as f:
                    json.dump(sessions, f, ensure_ascii=False, indent=2)
                
                logging.info(f"Session destroyed for user {username}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error destroying session {session_id}: {str(e)}")
            return False
    
    def cleanup_expired_sessions(self):
        """清理过期会话"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in sessions.items():
                last_activity = datetime.fromisoformat(session_data["last_activity"])
                if current_time - last_activity > timedelta(seconds=self.session_timeout):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del sessions[session_id]
            
            if expired_sessions:
                with open(self.session_file, "w", encoding='utf-8') as f:
                    json.dump(sessions, f, ensure_ascii=False, indent=2)
                
                logging.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
        except Exception as e:
            logging.error(f"Error cleaning up sessions: {str(e)}")
    
    def get_active_sessions(self) -> Dict[str, Dict]:
        """获取所有活跃会话"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            # 清理过期会话
            self.cleanup_expired_sessions()
            
            # 重新读取清理后的会话
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            return sessions
            
        except Exception as e:
            logging.error(f"Error getting active sessions: {str(e)}")
            return {}
    
    def get_session_count(self) -> int:
        """获取活跃会话数量"""
        return len(self.get_active_sessions())
    
    def _save_session(self, session_id: str, session_data: Dict) -> bool:
        """保存会话数据"""
        try:
            with open(self.session_file, "r", encoding='utf-8') as f:
                sessions = json.load(f)
            
            sessions[session_id] = session_data
            
            with open(self.session_file, "w", encoding='utf-8') as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Error saving session {session_id}: {str(e)}")
            return False
