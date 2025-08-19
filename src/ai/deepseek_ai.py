"""
DeepSeek AI服务实现
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional

from .base_ai import BaseAI, APIError, RateLimitError, ConfigError
from ..config.settings import AIConfig
from ..auth.security import rate_limiter


class DeepSeekAI(BaseAI):
    """DeepSeek AI服务"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        api_key = api_key or AIConfig.DEEPSEEK_API_KEY
        model = model or AIConfig.DEEPSEEK_MODEL
        
        super().__init__(api_key, model)
        
        self.base_url = AIConfig.DEEPSEEK_BASE_URL
        self.timeout = AIConfig.REQUEST_TIMEOUT
        self.max_retries = AIConfig.MAX_RETRIES
        self.max_tokens = AIConfig.MAX_TOKENS
        self.temperature = AIConfig.TEMPERATURE
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def validate_config(self) -> bool:
        """验证配置"""
        if not self.api_key:
            raise ConfigError("DeepSeek API密钥未配置")
        
        if not self.model:
            raise ConfigError("DeepSeek模型未配置")
        
        return True
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """生成AI响应"""
        try:
            # 验证配置
            self.validate_config()
            
            # 检查限流
            if not rate_limiter.is_allowed(f"deepseek_{self.api_key}", limit=10, window=60):
                raise RateLimitError("请求过于频繁，请稍后再试")
            
            # 记录请求
            self.log_request(messages)
            
            # 准备请求数据
            payload = self._prepare_payload(messages, **kwargs)
            
            # 发送请求
            response = await self._make_request(payload)
            
            # 处理响应
            result = self._process_response(response)
            
            # 记录响应
            self.log_response(result)
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"DeepSeek AI error: {error_msg}")
            return self.format_error_response(error_msg)
    
    def _prepare_payload(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """准备请求载荷"""
        # 确保消息格式正确
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": str(msg["content"])
                })
        
        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "stream": False
        }
        
        return payload
    
    async def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送HTTP请求"""
        url = f"{self.base_url}/chat/completions"
        
        for attempt in range(self.max_retries):
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(url, headers=self.headers, json=payload) as response:
                        response_data = await response.json()
                        
                        if response.status == 200:
                            return response_data
                        elif response.status == 429:
                            raise RateLimitError("API请求限流")
                        elif response.status == 401:
                            raise APIError("API密钥无效")
                        elif response.status == 402:
                            raise APIError("账户余额不足")
                        else:
                            error_msg = response_data.get("error", {}).get("message", f"HTTP {response.status}")
                            raise APIError(f"API请求失败: {error_msg}")
                
            except asyncio.TimeoutError:
                if attempt == self.max_retries - 1:
                    raise APIError("请求超时")
                await asyncio.sleep(2 ** attempt)  # 指数退避
            
            except aiohttp.ClientError as e:
                if attempt == self.max_retries - 1:
                    raise APIError(f"网络错误: {str(e)}")
                await asyncio.sleep(2 ** attempt)
    
    def _process_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理API响应"""
        try:
            if "choices" not in response_data or not response_data["choices"]:
                raise APIError("响应格式错误：缺少choices字段")
            
            choice = response_data["choices"][0]
            if "message" not in choice:
                raise APIError("响应格式错误：缺少message字段")
            
            content = choice["message"].get("content", "")
            
            # 提取元数据
            usage = response_data.get("usage", {})
            metadata = {
                "model": response_data.get("model", self.model),
                "usage": usage,
                "finish_reason": choice.get("finish_reason", "unknown")
            }
            
            return self.format_success_response(content, **metadata)
            
        except Exception as e:
            raise APIError(f"响应处理失败: {str(e)}")
    
    async def stream_response(self, messages: List[Dict[str, str]], **kwargs):
        """流式响应（生成器）"""
        try:
            self.validate_config()
            
            payload = self._prepare_payload(messages, **kwargs)
            payload["stream"] = True
            
            url = f"{self.base_url}/chat/completions"
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, headers=self.headers, json=payload) as response:
                    if response.status != 200:
                        error_data = await response.json()
                        error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status}")
                        raise APIError(f"API请求失败: {error_msg}")
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = line[6:]
                            if data == '[DONE]':
                                break
                            
                            try:
                                import json
                                chunk = json.loads(data)
                                if 'choices' in chunk and chunk['choices']:
                                    delta = chunk['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            self.logger.error(f"Stream response error: {str(e)}")
            yield f"错误: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            "provider": "DeepSeek",
            "model": self.model,
            "base_url": self.base_url,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
