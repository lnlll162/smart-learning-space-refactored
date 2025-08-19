"""
AI服务管理器
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from enum import Enum

from .base_ai import BaseAI, AIError
from .deepseek_ai import DeepSeekAI
from ..config.settings import AIConfig


class AIProvider(Enum):
    """AI服务提供商"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    CLAUDE = "claude"


class AIManager:
    """AI服务管理器"""
    
    def __init__(self):
        self.providers = {}
        self.default_provider = AIProvider.DEEPSEEK
        self.logger = logging.getLogger(__name__)
        self._initialize_providers()
    
    def _initialize_providers(self):
        """初始化AI服务提供商"""
        try:
            # 初始化DeepSeek
            if AIConfig.DEEPSEEK_API_KEY:
                self.providers[AIProvider.DEEPSEEK] = DeepSeekAI()
                self.logger.info("DeepSeek AI initialized")
            
            # 可以在这里添加其他AI提供商
            # if AIConfig.OPENAI_API_KEY:
            #     self.providers[AIProvider.OPENAI] = OpenAIService()
            
        except Exception as e:
            self.logger.error(f"Error initializing AI providers: {str(e)}")
    
    def get_provider(self, provider: Optional[AIProvider] = None) -> Optional[BaseAI]:
        """获取AI服务提供商实例"""
        provider = provider or self.default_provider
        return self.providers.get(provider)
    
    def is_available(self, provider: Optional[AIProvider] = None) -> bool:
        """检查AI服务是否可用"""
        ai_service = self.get_provider(provider)
        if not ai_service:
            return False
        
        try:
            return ai_service.validate_config()
        except Exception:
            return False
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[AIProvider] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """生成AI响应"""
        ai_service = self.get_provider(provider)
        
        if not ai_service:
            return {
                "success": False,
                "error": "AI服务不可用",
                "content": "抱歉，AI助手当前不可用。请稍后再试。"
            }
        
        try:
            return await ai_service.generate_response(messages, **kwargs)
        except Exception as e:
            self.logger.error(f"AI response generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": f"抱歉，生成响应时出错：{str(e)}"
            }
    
    async def chat(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_prompt: Optional[str] = None,
        provider: Optional[AIProvider] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """聊天对话接口"""
        messages = []
        
        # 添加系统提示
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加对话历史
        if conversation_history:
            messages.extend(conversation_history)
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_message})
        
        return await self.generate_response(messages, provider, **kwargs)
    
    async def analyze_learning_data(
        self,
        data: Dict[str, Any],
        analysis_type: str = "general",
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """分析学习数据"""
        prompts = {
            "general": "请分析以下学习数据，提供洞察和建议：",
            "behavior": "请分析学习行为模式，识别学习习惯和改进建议：",
            "performance": "请分析学习表现数据，评估进度和提供优化建议：",
            "space": "请分析学习空间使用数据，提供空间优化建议："
        }
        
        prompt = prompts.get(analysis_type, prompts["general"])
        user_message = f"{prompt}\n\n{str(data)}"
        
        system_prompt = """你是一个专业的学习数据分析师，擅长：
1. 分析学习行为模式
2. 识别学习效果趋势
3. 提供个性化建议
4. 优化学习策略

请用中文回答，提供清晰、实用的分析结果。"""
        
        return await self.chat(user_message, system_prompt=system_prompt, provider=provider)
    
    async def generate_learning_path(
        self,
        user_profile: Dict[str, Any],
        learning_goals: List[str],
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """生成学习路径"""
        user_message = f"""
请为以下用户生成个性化学习路径：

用户档案：{user_profile}
学习目标：{learning_goals}

请提供：
1. 详细的学习阶段划分
2. 每个阶段的具体目标
3. 推荐的学习资源
4. 时间安排建议
5. 评估方法
"""
        
        system_prompt = """你是一个专业的学习路径规划师，具有以下专长：
1. 个性化学习方案设计
2. 学习目标分解和规划
3. 学习资源匹配
4. 进度跟踪和调整

请提供结构化、可执行的学习路径方案。"""
        
        return await self.chat(user_message, system_prompt=system_prompt, provider=provider)
    
    async def recommend_learning_space(
        self,
        user_preferences: Dict[str, Any],
        available_spaces: List[Dict[str, Any]],
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """推荐学习空间"""
        user_message = f"""
基于用户偏好和可用空间，请推荐最适合的学习空间：

用户偏好：{user_preferences}
可用空间：{available_spaces}

请考虑：
1. 学习习惯匹配
2. 环境适宜性
3. 资源可用性
4. 干扰因素
5. 便利性
"""
        
        system_prompt = """你是一个智能学习空间推荐专家，专长于：
1. 学习环境分析
2. 个人偏好匹配
3. 空间效率优化
4. 学习体验提升

请提供详细的推荐理由和使用建议。"""
        
        return await self.chat(user_message, system_prompt=system_prompt, provider=provider)
    
    async def diagnose_learning_issues(
        self,
        learning_data: Dict[str, Any],
        performance_metrics: Dict[str, Any],
        provider: Optional[AIProvider] = None
    ) -> Dict[str, Any]:
        """诊断学习问题"""
        user_message = f"""
请分析学习数据，诊断可能存在的学习问题：

学习数据：{learning_data}
表现指标：{performance_metrics}

请识别：
1. 学习效率问题
2. 学习方法问题
3. 时间管理问题
4. 注意力问题
5. 动机问题

并提供具体的改进建议。
"""
        
        system_prompt = """你是一个学习问题诊断专家，具备：
1. 学习科学知识
2. 认知心理学背景
3. 数据分析能力
4. 教育咨询经验

请提供专业、实用的诊断和建议。"""
        
        return await self.chat(user_message, system_prompt=system_prompt, provider=provider)
    
    def get_available_providers(self) -> List[str]:
        """获取可用的AI服务提供商列表"""
        return [provider.value for provider in self.providers.keys()]
    
    def get_provider_info(self, provider: Optional[AIProvider] = None) -> Dict[str, Any]:
        """获取AI服务提供商信息"""
        ai_service = self.get_provider(provider)
        if not ai_service:
            return {"error": "服务不可用"}
        
        try:
            return ai_service.get_model_info()
        except AttributeError:
            return {"provider": provider.value if provider else "unknown"}
    
    def set_default_provider(self, provider: AIProvider):
        """设置默认AI服务提供商"""
        if provider in self.providers:
            self.default_provider = provider
            self.logger.info(f"Default AI provider set to {provider.value}")
        else:
            raise ValueError(f"Provider {provider.value} not available")


# 全局AI管理器实例
ai_manager = AIManager()
