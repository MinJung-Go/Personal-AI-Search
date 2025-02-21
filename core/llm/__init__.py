'''
Author: qhr
Date: 2025-01-09 05:40:09
LastEditors: qhr
LastEditTime: 2025-02-21 06:34:39
# -*- Power By FocusAIM -*-
'''
from abc import ABC
from typing import Any, List, Optional, Union
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from core.llm.llm import LLM_TYPE, BaseLLM, GPT, Deepseek


class LLM(ABC):
    def __new__(
        cls,
        model: str,
        api: Optional[str] = None,
        time_out: Optional[int] = 240,
        role_system: Optional[dict] = None,
        max_tokens: Optional[int] = 2048,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        repetition_penalty: Optional[float] = 1,
        frequency_penalty: Optional[int] = 0,
        presence_penalty: Optional[int] = 0,
        top_k: Optional[int] = -1,
        stop: Optional[Union[str, List[str]]] = None,
        channel: Optional[str] = "OpenAI",
        **kwargs
    ) -> LLM_TYPE:
        """
        :param model: 大模型名称
        :param api: 接口地址
        :param time_out: 超时时间
        :param role_system: 角色
        :param max_tokens: 返回结果最大tokens
        :param temperature: 温度，用于控制生成文本的多样性
        :param top_p: 用于控制模型生成下一个 token 时，在概率分布中的选择范围
        :param repetition_penalty: 重复词惩罚，默认值 1.0 表示不产生作用
        :param frequency_penalty: 用于控制模型是否生成常见词汇：0 表示更有可能生成常见词汇，1 表示完全避免生成常见词汇
        :param presence_penalty: 用于控制模型是否生成已生成的词汇：0 表示更有可能生成重复内容，1 表示生成完全不重复的内容
        :param top_k: 作用与 top_p 类似，但限定的是 token 在概率分布中从大到小排名的前 k 个
        :param stop: 停止词，文本生成过程在遇到这里指定的词汇后被截停
        :param kwargs: 其他参数
        """

        kwargs = {
            'model': model,
            'time_out': time_out,
            'role_system': role_system,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'repetition_penalty': repetition_penalty,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty,
            'top_k': top_k,
            'stop': stop,
            'channel': channel,
        }
        if api:
            kwargs['api'] = api

        if 'gpt' in model.lower() or "o1" in model.lower():
            return GPT(**kwargs)
        elif 'deepseek' in model.lower():
            return Deepseek(**kwargs)
        else:
            return BaseLLM(**kwargs)


if __name__ == '__main__':

    model = 'deepseek-chat'
    model = 'gpt-4o-mini'
    model = 'Qwen2.5-1.5B'
    llm = LLM(model)
    messages = [
        {"role": "user", "content": "你是谁"},
    ]

    # res = llm.get_response(messages)
    # print(res)

    tools = [
        {
            "name": "get_current_temperature",
            "description": "获取指定位置的当前温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "地点，例如'San Francisco, CA, USA'"}
                },
                "required": ["location"]
            },
            "function": {  # 添加 function 字段
                "name": "get_current_temperature",
                "arguments": {
                    "location": "San Francisco, CA, USA"
                }
            }
        },
        {
            "name": "get_temperature_date",
            "description": "获取指定位置的未来日期的温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "地点"},
                    "date": {"type": "string", "description": "日期，例如'2024-10-01'"}
                },
                "required": ["location", "date"]
            },
            "function": {  # 添加 function 字段
                "name": "get_temperature_date",
                "arguments": {
                    "location": "San Francisco, CA, USA",
                    "date": "2024-10-01"
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": "You are Qwen, a helpful assistant."},
        {"role": "user", "content": "What's the temperature in San Francisco now? How about tomorrow?"}
    ]
    
    res = llm.get_response(messages, tools=tools)
    print(res)

    # for i in llm.stream_chat(messages):
    #     print(i)
