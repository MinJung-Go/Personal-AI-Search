'''
Author: qhr
Date: 2024-12-10 08:26:25
LastEditors: qhr
LastEditTime: 2025-02-21 06:31:28
# -*- Power By FocusAIM -*-
'''

from abc import ABC
import json
import os
from typing import Any, List, Optional, TypeVar, Union, Dict
import uuid
import httpx
from config import GPT_URL, DEEPSEEK_URL, GPT_API_KEY, DEEPSEEK_API_KEY
from openai import OpenAI,  AsyncOpenAI

class BaseLLM(ABC):
    api : Optional[str] = None
    model: Optional[str] = None
    headers: Optional[object] = {"Content-Type": "application/json"}
    time_out: Optional[int] = 240
    role_system: Optional[Dict[str, str]] = None

    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.7
    repetition_penalty: Optional[float] = 1
    frequency_penalty: Optional[int] = 0
    presence_penalty: Optional[int] = 0
    top_k: Optional[int] = -1
    stop: Optional[Union[str, List[str]]] = None
    api_key: Optional[str] = "EMPTY"
    chanel: Optional[str] = None

    def __init__(self, **kwargs: Any):
        self.api: str = kwargs.get('api', self.api)
        self.model: str = kwargs.get('model', self.model)
        self.headers: object = kwargs.get('headers', self.headers)
        self.time_out: int = kwargs.get('time_out', self.time_out)
        self.role_system: Dict[str, str] = kwargs.get('role_system', self.role_system)
        self.max_tokens: int = kwargs.get('max_tokens', self.max_tokens)
        
        self.temperature: float = kwargs.get('temperature', self.temperature)
        self.top_p: float = kwargs.get('top_p', self.top_p)
        self.repetition_penalty: float = kwargs.get('repetition_penalty', self.repetition_penalty)
        self.frequency_penalty: int = kwargs.get('frequency_penalty', self.frequency_penalty)
        self.presence_penalty: int = kwargs.get('presence_penalty', self.presence_penalty)
        self.top_k: int = kwargs.get('top_k', self.top_k)
        self.stop: Union[str, List[str]] = kwargs.get('stop', self.stop)
        self.api_key: str = kwargs.get('api_key', self.api_key)
        self.chanel : str = kwargs.get('chanel', self.chanel)
        
    def get_json_content(self, **kwargs):
        json_content = {
                "model": self.model,
                "max_tokens": self.max_tokens if kwargs.get('max_tokens', None) is None else kwargs['max_tokens'],
                "temperature": self.temperature if kwargs.get('temperature', None) is None else kwargs['temperature'],
                "stream": False,
                "top_p": self.top_p if kwargs.get('top_p', None) is None else kwargs['top_p']
        }
        tools = kwargs.get("tools" , None)
        if tools:
            json_content["tools"] = tools
        return json_content
    
    def get_response(self, messages: List[Dict[str, str]], **kwargs):
        json_content = self.get_json_content(**kwargs)
        json_content['messages'] = messages     
        client = OpenAI(api_key=self.api_key , base_url=self.api)
        response = client.chat.completions.create(**json_content)
        try:
            res = response.choices[0].message
            responese_content = {
                "text": res.content,
                "functionCall":None
                }
            if res.tool_calls:
                responese_content['functionCall'] = {"name":res.tool_calls[0].function.name, "arguments": res.tool_calls[0].function.arguments}
        except Exception as e:
            responese_content = f"LLM Error: {e}"
            print(responese_content)
        return responese_content
    
    async def  get_response_async(self, messages: List[Dict[str, str]], **kwargs):
        json_content = self.get_json_content(**kwargs)
        json_content['messages'] = messages   
        async with AsyncOpenAI(api_key=self.api_key , base_url=self.api) as client:
            response = await client.chat.completions.create(**json_content)
            try:
                res = response.choices[0].message
                responese_content = {
                    "text": res.content,
                    "functionCall":None
                    }
                if res.tool_calls:
                    responese_content['functionCall'] = {"name":res.tool_calls[0].function.name, "arguments": res.tool_calls[0].function.arguments}
            except Exception as e:
                responese_content = f"LLM Error: {e}"
                print(responese_content)
        return responese_content
    
    def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        json_content = self.get_json_content(**kwargs)
        json_content['messages'] = messages
        json_content['stream'] = True
        response = httpx.post(f'{self.api}/chat/completions', headers=self.headers, json=json_content, timeout=self.time_out)
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    if line.startswith("data: "):
                        line = line[6:]
                        if line == "[DONE]":
                            continue
                        data = json.loads(line.strip().replace("\\", "").replace("\\n", ""))
                        text = data['choices'][0]['delta']['content']
                        if text == '':
                            continue
                        yield text


class GPT(BaseLLM):
    api = GPT_URL
    api_key = GPT_API_KEY
    model = 'Qwen2.5-1.5B'

class Deepseek(BaseLLM):
    api = DEEPSEEK_URL
    api_key = DEEPSEEK_API_KEY
    model = 'volcengine_deepseek-reasoner'


LLM_TYPE = TypeVar('LLM_TYPE', BaseLLM, GPT, Deepseek)
