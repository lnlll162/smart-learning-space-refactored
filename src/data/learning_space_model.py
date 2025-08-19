"""
学习空间模型
"""

import random
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging


class LearningSpaceModel:
    """学习空间模型"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 物理学习空间配置
        self.physical_spaces = {
            "安静区域": {
                "capacity": 50,
                "noise_level": "低",
                "equipment": ["桌椅", "台灯", "电源"],
                "suitable_activities": ["阅读", "写作", "思考"],
                "comfort_score": 8.5
            },
            "协作区域": {
                "capacity": 30,
                "noise_level": "中",
                "equipment": ["桌椅", "白板", "投影仪"],
                "suitable_activities": ["讨论", "小组学习", "演示"],
                "comfort_score": 7.8
            },
            "技术区域": {
                "capacity": 40,
                "noise_level": "中",
                "equipment": ["电脑", "高速网络", "打印机"],
                "suitable_activities": ["编程", "设计", "研究"],
                "comfort_score": 8.2
            },
            "创新实验室": {
                "capacity": 20,
                "noise_level": "高",
                "equipment": ["实验设备", "工具", "材料"],
                "suitable_activities": ["实验", "制作", "测试"],
                "comfort_score": 7.5
            },
            "休闲区域": {
                "capacity": 25,
                "noise_level": "中高",
                "equipment": ["沙发", "咖啡机", "娱乐设施"],
                "suitable_activities": ["休息", "非正式讨论", "放松"],
                "comfort_score": 8.0
            }
        }
        
        # 虚拟学习空间配置
        self.virtual_spaces = {
            "在线课堂": {
                "platform": "Zoom/Teams",
                "max_participants": 500,
                "features": ["视频会议", "屏幕共享", "录制"],
                "interaction_level": "高",
                "technical_requirements": "稳定网络"
            },
            "VR学习环境": {
                "platform": "VR设备",
                "max_participants": 50,
                "features": ["沉浸式体验", "3D交互", "虚拟现实"],
                "interaction_level": "极高",
                "technical_requirements": "VR头盔"
            },
            "学习管理系统": {
                "platform": "LMS",
                "max_participants": 1000,
                "features": ["课程管理", "作业提交", "成绩跟踪"],
                "interaction_level": "中",
                "technical_requirements": "基础设备"
            },
            "协作平台": {
                "platform": "在线工具",
                "max_participants": 100,
                "features": ["文档协作", "项目管理", "实时沟通"],
                "interaction_level": "高",
                "technical_requirements": "网络连接"
            }
        }
        
        # 泛在学习空间配置
        self.ubiquitous_spaces = {
            "移动学习": {
                "devices": ["智能手机", "平板电脑"],
                "accessibility": "随时随地",
                "features": ["离线学习", "同步", "通知"],
                "limitations": "屏幕尺寸",
                "convenience_score": 9.0
            },
            "智能家居": {
                "devices": ["智能音箱", "智能显示屏"],
                "accessibility": "家庭环境",
                "features": ["语音交互", "环境控制", "个性化"],
                "limitations": "设备依赖",
                "convenience_score": 8.0
            },
            "增强现实": {
                "devices": ["AR眼镜", "智能手机"],
                "accessibility": "任何环境",
                "features": ["信息叠加", "实时交互", "情境学习"],
                "limitations": "技术成熟度",
                "convenience_score": 7.5
            },
            "物联网学习": {
                "devices": ["传感器", "智能设备"],
                "accessibility": "环境感知",
                "features": ["自动适应", "数据收集", "智能建议"],
                "limitations": "隐私安全",
                "convenience_score": 8.5
            }
        }
        
        # 用户偏好权重
        self.preference_weights = {
            "安静程度": 0.25,
            "设备齐全": 0.20,
            "空间舒适": 0.20,
            "便利程度": 0.15,
            "社交需求": 0.10,
            "技术支持": 0.10
        }
    
    def recommend_space(self, user_profile: Dict[str, Any], current_context: Dict[str, Any]) -> Dict[str, Any]:
        """推荐学习空间"""
        recommendations = {}
        
        # 分析物理空间
        physical_scores = self._evaluate_physical_spaces(user_profile, current_context)
        recommendations["physical"] = physical_scores
        
        # 分析虚拟空间
        virtual_scores = self._evaluate_virtual_spaces(user_profile, current_context)
        recommendations["virtual"] = virtual_scores
        
        # 分析泛在空间
        ubiquitous_scores = self._evaluate_ubiquitous_spaces(user_profile, current_context)
        recommendations["ubiquitous"] = ubiquitous_scores
        
        # 综合推荐
        best_recommendation = self._get_best_recommendation(recommendations)
        
        return {
            "recommendations": recommendations,
            "best_choice": best_recommendation,
            "analysis": self._generate_recommendation_analysis(user_profile, best_recommendation)
        }
    
    def _evaluate_physical_spaces(self, user_profile: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """评估物理学习空间"""
        scores = {}
        
        for space_name, space_info in self.physical_spaces.items():
            score = 0
            
            # 噪音偏好匹配
            user_noise_pref = user_profile.get("noise_preference", "低")
            space_noise = space_info["noise_level"]
            if user_noise_pref == space_noise:
                score += 0.3
            elif abs(self._noise_level_to_score(user_noise_pref) - self._noise_level_to_score(space_noise)) <= 1:
                score += 0.15
            
            # 活动类型匹配
            user_activity = context.get("activity_type", "学习")
            if user_activity in space_info["suitable_activities"]:
                score += 0.25
            
            # 舒适度评分
            score += space_info["comfort_score"] / 10 * 0.2
            
            # 容量可用性
            current_usage = context.get("current_usage", {}).get(space_name, 0)
            capacity = space_info["capacity"]
            if current_usage < capacity * 0.8:  # 80%以下认为可用
                score += 0.15
            elif current_usage < capacity:
                score += 0.05
            
            # 设备需求匹配
            required_equipment = user_profile.get("required_equipment", [])
            available_equipment = space_info["equipment"]
            equipment_match = len(set(required_equipment) & set(available_equipment)) / max(len(required_equipment), 1)
            score += equipment_match * 0.1
            
            scores[space_name] = min(1.0, score)
        
        return scores
    
    def _evaluate_virtual_spaces(self, user_profile: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """评估虚拟学习空间"""
        scores = {}
        
        for space_name, space_info in self.virtual_spaces.items():
            score = 0
            
            # 技术能力匹配
            user_tech_level = user_profile.get("tech_proficiency", "中")
            required_tech = space_info["technical_requirements"]
            if self._tech_requirement_met(user_tech_level, required_tech):
                score += 0.3
            else:
                score += 0.1
            
            # 交互需求匹配
            user_interaction_need = user_profile.get("interaction_preference", "中")
            space_interaction = space_info["interaction_level"]
            if user_interaction_need == space_interaction:
                score += 0.25
            
            # 学习目标匹配
            learning_goal = context.get("learning_goal", "一般学习")
            if self._virtual_space_suits_goal(space_name, learning_goal):
                score += 0.2
            
            # 时间灵活性
            if context.get("time_flexibility", True):
                score += 0.15
            
            # 参与人数适配
            group_size = context.get("group_size", 1)
            max_participants = space_info["max_participants"]
            if group_size <= max_participants:
                score += 0.1
            
            scores[space_name] = min(1.0, score)
        
        return scores
    
    def _evaluate_ubiquitous_spaces(self, user_profile: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, float]:
        """评估泛在学习空间"""
        scores = {}
        
        for space_name, space_info in self.ubiquitous_spaces.items():
            score = 0
            
            # 便利性评分
            score += space_info["convenience_score"] / 10 * 0.3
            
            # 设备可用性
            user_devices = user_profile.get("available_devices", [])
            required_devices = space_info["devices"]
            device_match = len(set(user_devices) & set(required_devices)) / len(required_devices)
            score += device_match * 0.25
            
            # 学习场景适配
            current_location = context.get("location", "未知")
            accessibility = space_info["accessibility"]
            if self._location_matches_accessibility(current_location, accessibility):
                score += 0.2
            
            # 移动性需求
            mobility_need = user_profile.get("mobility_preference", "中")
            if mobility_need == "高" and "移动" in space_name:
                score += 0.15
            
            # 特殊功能匹配
            special_needs = context.get("special_requirements", [])
            space_features = space_info["features"]
            feature_match = len(set(special_needs) & set(space_features)) / max(len(special_needs), 1)
            score += feature_match * 0.1
            
            scores[space_name] = min(1.0, score)
        
        return scores
    
    def _get_best_recommendation(self, recommendations: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """获取最佳推荐"""
        best_score = 0
        best_space = None
        best_type = None
        
        for space_type, spaces in recommendations.items():
            for space_name, score in spaces.items():
                if score > best_score:
                    best_score = score
                    best_space = space_name
                    best_type = space_type
        
        return {
            "space_name": best_space,
            "space_type": best_type,
            "score": best_score,
            "confidence": "高" if best_score > 0.8 else "中" if best_score > 0.6 else "低"
        }
    
    def _generate_recommendation_analysis(self, user_profile: Dict[str, Any], recommendation: Dict[str, Any]) -> str:
        """生成推荐分析"""
        space_name = recommendation["space_name"]
        space_type = recommendation["space_type"]
        score = recommendation["score"]
        
        analysis = f"推荐 {space_type} 类型的 '{space_name}' (匹配度: {score:.1%})\n\n"
        
        if space_type == "physical":
            space_info = self.physical_spaces[space_name]
            analysis += f"推荐理由：\n"
            analysis += f"- 噪音水平: {space_info['noise_level']}\n"
            analysis += f"- 可用设备: {', '.join(space_info['equipment'])}\n"
            analysis += f"- 适合活动: {', '.join(space_info['suitable_activities'])}\n"
            analysis += f"- 舒适度评分: {space_info['comfort_score']}/10"
        
        elif space_type == "virtual":
            space_info = self.virtual_spaces[space_name]
            analysis += f"推荐理由：\n"
            analysis += f"- 平台: {space_info['platform']}\n"
            analysis += f"- 主要功能: {', '.join(space_info['features'])}\n"
            analysis += f"- 交互水平: {space_info['interaction_level']}\n"
            analysis += f"- 技术要求: {space_info['technical_requirements']}"
        
        elif space_type == "ubiquitous":
            space_info = self.ubiquitous_spaces[space_name]
            analysis += f"推荐理由：\n"
            analysis += f"- 支持设备: {', '.join(space_info['devices'])}\n"
            analysis += f"- 可访问性: {space_info['accessibility']}\n"
            analysis += f"- 主要特性: {', '.join(space_info['features'])}\n"
            analysis += f"- 便利度评分: {space_info['convenience_score']}/10"
        
        return analysis
    
    def get_space_availability(self, space_type: str, space_name: str, datetime_obj: datetime) -> Dict[str, Any]:
        """获取空间可用性"""
        if space_type == "physical":
            space_info = self.physical_spaces.get(space_name, {})
            capacity = space_info.get("capacity", 0)
            
            # 模拟当前使用情况
            hour = datetime_obj.hour
            is_weekend = datetime_obj.weekday() >= 5
            
            # 根据时间段计算使用率
            if is_weekend:
                base_usage = 0.3
            else:
                if 9 <= hour <= 17:
                    base_usage = 0.7
                elif 18 <= hour <= 21:
                    base_usage = 0.5
                else:
                    base_usage = 0.2
            
            current_users = int(capacity * base_usage * random.uniform(0.7, 1.3))
            current_users = max(0, min(capacity, current_users))
            
            return {
                "capacity": capacity,
                "current_users": current_users,
                "available_spots": capacity - current_users,
                "usage_rate": current_users / capacity if capacity > 0 else 0,
                "status": "可用" if current_users < capacity else "已满"
            }
        
        elif space_type == "virtual":
            space_info = self.virtual_spaces.get(space_name, {})
            max_participants = space_info.get("max_participants", 0)
            
            # 虚拟空间通常有更高的可用性
            current_users = random.randint(0, max_participants // 2)
            
            return {
                "max_participants": max_participants,
                "current_participants": current_users,
                "available_spots": max_participants - current_users,
                "usage_rate": current_users / max_participants if max_participants > 0 else 0,
                "status": "可用",
                "technical_status": "正常"
            }
        
        elif space_type == "ubiquitous":
            # 泛在空间通常总是可用的
            return {
                "status": "可用",
                "accessibility": "随时",
                "device_requirements": self.ubiquitous_spaces.get(space_name, {}).get("devices", []),
                "network_status": "正常"
            }
        
        return {"status": "未知空间"}
    
    # 辅助方法
    def _noise_level_to_score(self, noise_level: str) -> int:
        """噪音级别转换为数值"""
        return {"低": 1, "中": 2, "中高": 3, "高": 4}.get(noise_level, 2)
    
    def _tech_requirement_met(self, user_level: str, requirement: str) -> bool:
        """检查技术要求是否满足"""
        user_scores = {"低": 1, "中": 2, "高": 3}
        req_scores = {"基础设备": 1, "稳定网络": 2, "VR头盔": 3, "网络连接": 2}
        
        user_score = user_scores.get(user_level, 2)
        req_score = req_scores.get(requirement, 2)
        
        return user_score >= req_score
    
    def _virtual_space_suits_goal(self, space_name: str, learning_goal: str) -> bool:
        """检查虚拟空间是否适合学习目标"""
        goal_space_mapping = {
            "协作学习": ["在线课堂", "协作平台"],
            "沉浸式学习": ["VR学习环境"],
            "自主学习": ["学习管理系统"],
            "项目管理": ["协作平台"]
        }
        
        suitable_spaces = goal_space_mapping.get(learning_goal, [])
        return space_name in suitable_spaces
    
    def _location_matches_accessibility(self, location: str, accessibility: str) -> bool:
        """检查位置是否匹配可访问性"""
        location_mapping = {
            "家": ["家庭环境", "随时随地"],
            "办公室": ["任何环境", "随时随地"],
            "户外": ["随时随地", "任何环境"],
            "交通工具": ["随时随地"]
        }
        
        suitable_accessibility = location_mapping.get(location, ["随时随地"])
        return accessibility in suitable_accessibility
