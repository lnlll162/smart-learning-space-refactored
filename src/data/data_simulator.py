"""
数据模拟器
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging


class DataSimulator:
    """数据模拟器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 空间类型配置
        self.space_types = {
            'physical': {
                '图书馆': {'capacity': 200, 'noise_level': 'low', 'resources': ['books', 'computer', 'wifi']},
                '自习室': {'capacity': 50, 'noise_level': 'very_low', 'resources': ['desk', 'wifi']},
                '实验室': {'capacity': 30, 'noise_level': 'medium', 'resources': ['equipment', 'computer', 'wifi']},
                '教室': {'capacity': 100, 'noise_level': 'medium', 'resources': ['projector', 'whiteboard', 'wifi']},
                '咖啡厅': {'capacity': 40, 'noise_level': 'high', 'resources': ['wifi', 'food']}
            },
            'virtual': {
                '在线课堂': {'capacity': 1000, 'platform': 'zoom', 'features': ['video', 'chat', 'screen_share']},
                'VR学习空间': {'capacity': 50, 'platform': 'vr', 'features': ['immersive', '3d_models', 'interaction']},
                '学习社区': {'capacity': 500, 'platform': 'forum', 'features': ['discussion', 'resources', 'collaboration']}
            },
            'ubiquitous': {
                '移动学习': {'device': 'mobile', 'features': ['offline', 'sync', 'notifications']},
                '智能家居': {'device': 'iot', 'features': ['voice_control', 'environment_control']},
                '增强现实': {'device': 'ar', 'features': ['overlay', 'real_time', 'interactive']}
            }
        }
        
        # 用户行为模式
        self.behavior_patterns = {
            '早鸟型': {'peak_hours': [7, 8, 9, 10], 'prefer_quiet': True},
            '夜猫子型': {'peak_hours': [20, 21, 22, 23], 'prefer_quiet': True},
            '社交型': {'peak_hours': [14, 15, 16, 17], 'prefer_quiet': False},
            '专注型': {'peak_hours': [9, 10, 14, 15], 'prefer_quiet': True}
        }
    
    def generate_usage_data(self, days: int = 30, spaces: Optional[List[str]] = None) -> pd.DataFrame:
        """生成空间使用数据"""
        if spaces is None:
            spaces = list(self.space_types['physical'].keys())
        
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            for space in spaces:
                # 工作日和周末的使用模式不同
                is_weekend = current_date.weekday() >= 5
                base_usage = 0.6 if is_weekend else 0.8
                
                for hour in range(24):
                    # 根据时间段调整使用率
                    hour_factor = self._get_hour_factor(hour, is_weekend)
                    usage_rate = base_usage * hour_factor * random.uniform(0.7, 1.3)
                    usage_rate = max(0, min(1, usage_rate))  # 限制在0-1之间
                    
                    capacity = self.space_types['physical'].get(space, {}).get('capacity', 50)
                    actual_users = int(capacity * usage_rate)
                    
                    data.append({
                        'date': current_date.date(),
                        'hour': hour,
                        'space': space,
                        'users': actual_users,
                        'capacity': capacity,
                        'usage_rate': usage_rate,
                        'is_weekend': is_weekend
                    })
        
        return pd.DataFrame(data)
    
    def generate_environment_data(self, days: int = 30) -> pd.DataFrame:
        """生成环境数据"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        spaces = list(self.space_types['physical'].keys())
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            for space in spaces:
                # 每小时生成一次环境数据
                for hour in range(24):
                    timestamp = current_date.replace(hour=hour, minute=0, second=0)
                    
                    # 根据空间类型生成基础环境参数
                    base_temp = 22 + random.gauss(0, 2)
                    base_humidity = 45 + random.gauss(0, 5)
                    base_co2 = 400 + random.gauss(0, 50)
                    
                    # 根据使用率调整环境参数
                    usage_factor = self._get_hour_factor(hour, current_date.weekday() >= 5)
                    
                    data.append({
                        'timestamp': timestamp,
                        'space': space,
                        'temperature': base_temp + usage_factor * random.uniform(-1, 3),
                        'humidity': base_humidity + usage_factor * random.uniform(-5, 10),
                        'co2': base_co2 + usage_factor * random.uniform(0, 200),
                        'noise_level': self._get_noise_level(space, usage_factor),
                        'light_level': self._get_light_level(hour, usage_factor)
                    })
        
        return pd.DataFrame(data)
    
    def generate_learning_behavior_data(self, users: int = 100, days: int = 30) -> pd.DataFrame:
        """生成学习行为数据"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        # 生成用户档案
        users_profiles = self._generate_user_profiles(users)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            
            for user_id, profile in users_profiles.items():
                # 根据用户类型决定是否学习
                learning_probability = 0.3 if is_weekend else 0.8
                if random.random() > learning_probability:
                    continue
                
                # 生成学习会话
                sessions = self._generate_learning_sessions(user_id, profile, current_date)
                data.extend(sessions)
        
        return pd.DataFrame(data)
    
    def generate_performance_data(self, users: int = 100, days: int = 30) -> pd.DataFrame:
        """生成学习表现数据"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for user_id in range(1, users + 1):
            # 用户基础能力（影响表现趋势）
            base_ability = random.uniform(0.3, 0.9)
            learning_rate = random.uniform(0.001, 0.01)  # 学习进步率
            
            for day in range(days):
                current_date = start_date + timedelta(days=day)
                
                # 能力随时间增长
                current_ability = min(1.0, base_ability + learning_rate * day)
                
                # 添加随机波动
                daily_performance = current_ability * random.uniform(0.7, 1.3)
                daily_performance = max(0, min(1, daily_performance))
                
                # 生成具体指标
                data.append({
                    'date': current_date.date(),
                    'user_id': user_id,
                    'completion_rate': daily_performance,
                    'accuracy': daily_performance * random.uniform(0.8, 1.1),
                    'learning_time': int(daily_performance * random.uniform(60, 240)),  # 分钟
                    'engagement_score': daily_performance * random.uniform(0.6, 1.0),
                    'difficulty_level': random.choice([1, 2, 3, 4, 5])
                })
        
        return pd.DataFrame(data)
    
    def generate_resource_usage_data(self, days: int = 30) -> pd.DataFrame:
        """生成资源使用数据"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        resources = ['计算机', '图书', '实验设备', '投影仪', '网络', '打印机']
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            is_weekend = current_date.weekday() >= 5
            
            for resource in resources:
                # 工作日使用更频繁
                base_usage = 0.3 if is_weekend else 0.7
                
                for hour in range(8, 22):  # 开放时间
                    hour_factor = self._get_hour_factor(hour, is_weekend)
                    usage_count = int(base_usage * hour_factor * random.uniform(5, 30))
                    
                    data.append({
                        'timestamp': current_date.replace(hour=hour, minute=0),
                        'resource': resource,
                        'usage_count': usage_count,
                        'availability': random.uniform(0.8, 1.0),
                        'maintenance_status': random.choice(['正常', '正常', '正常', '维护中'])
                    })
        
        return pd.DataFrame(data)
    
    def _get_hour_factor(self, hour: int, is_weekend: bool) -> float:
        """获取小时因子（影响使用率）"""
        if is_weekend:
            # 周末模式：上午10点-下午6点较活跃
            if 10 <= hour <= 18:
                return 0.8
            elif 8 <= hour <= 22:
                return 0.4
            else:
                return 0.1
        else:
            # 工作日模式：上午9-11点，下午2-5点，晚上7-9点较活跃
            if hour in [9, 10, 11, 14, 15, 16, 17, 19, 20, 21]:
                return 1.0
            elif 8 <= hour <= 22:
                return 0.6
            else:
                return 0.1
    
    def _get_noise_level(self, space: str, usage_factor: float) -> float:
        """获取噪音水平"""
        base_noise = {
            '图书馆': 30, '自习室': 25, '实验室': 45,
            '教室': 40, '咖啡厅': 55
        }.get(space, 35)
        
        # 使用率影响噪音
        noise_increase = usage_factor * 15
        return base_noise + noise_increase + random.uniform(-5, 5)
    
    def _get_light_level(self, hour: int, usage_factor: float) -> float:
        """获取光照水平"""
        # 自然光变化
        if 6 <= hour <= 18:
            natural_light = 100 * (1 - abs(hour - 12) / 6)
        else:
            natural_light = 20
        
        # 人工光照
        artificial_light = 60 + usage_factor * 20
        
        return natural_light + artificial_light
    
    def _generate_user_profiles(self, count: int) -> Dict[int, Dict[str, Any]]:
        """生成用户档案"""
        profiles = {}
        behavior_types = list(self.behavior_patterns.keys())
        
        for user_id in range(1, count + 1):
            profiles[user_id] = {
                'behavior_type': random.choice(behavior_types),
                'preferred_spaces': random.sample(
                    list(self.space_types['physical'].keys()), 
                    random.randint(2, 4)
                ),
                'skill_level': random.choice(['初级', '中级', '高级']),
                'learning_style': random.choice(['视觉型', '听觉型', '动手型', '阅读型'])
            }
        
        return profiles
    
    def _generate_learning_sessions(self, user_id: int, profile: Dict[str, Any], date: datetime) -> List[Dict[str, Any]]:
        """生成学习会话"""
        sessions = []
        behavior = self.behavior_patterns[profile['behavior_type']]
        
        # 根据行为模式决定学习时间
        session_count = random.randint(1, 3)
        
        for _ in range(session_count):
            # 选择学习时间
            hour = random.choice(behavior['peak_hours'])
            start_time = date.replace(hour=hour, minute=random.randint(0, 59))
            
            # 学习时长
            duration = random.randint(30, 180)  # 30分钟到3小时
            
            # 选择空间
            space = random.choice(profile['preferred_spaces'])
            
            sessions.append({
                'user_id': user_id,
                'start_time': start_time,
                'duration_minutes': duration,
                'space': space,
                'activity_type': random.choice(['阅读', '编程', '写作', '研究', '讨论']),
                'focus_level': random.uniform(0.3, 1.0),
                'satisfaction': random.uniform(0.5, 1.0)
            })
        
        return sessions


# 兼容性别名
AdvancedDataSimulator = DataSimulator
