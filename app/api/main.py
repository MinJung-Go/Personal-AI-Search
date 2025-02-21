'''
Author: MinJung
Date: 2024-12-10 08:26:25
LastEditors: MinJung
LastEditTime: 2025-02-21 06:31:00
# -*- Power By FocusAIM -*-
'''

import json
import ast
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from config import MEMORY, SYSTEM_PROMPT
from utils.utils import (show_time)
from core.tools import TOOLS
from core.agents import Agent
from core.llm import LLM


class AgenticSearch(Agent):

    def __init__(self, model="gpt-4o"):
        
        super().__init__()
        self.memory = MEMORY
        self.memory_official = MEMORY
        self.name = "AI-Search"
        self.model = model
        self.max_tokens = 16000
        self.llm = LLM(model=model, max_tokens=self.max_tokens)
        self.functions = [TOOLS[func_key]["function_call"] for func_key in TOOLS.keys()]
        self.instructions = SYSTEM_PROMPT

    async def apply_func_obj(self, func_obj, **kwargs):
        """
        Asynchronously applies a given function object with keyword arguments.
    
        This method demonstrates a design pattern where a function object, along with its arguments,
        is passed to another function for execution. It's primarily used for executing asynchronous operations,
        allowing for the dynamic execution of different functions based on runtime decisions.
    
        Arguments:
        - func_obj: A coroutine function object that is to be executed. Its type is a callable that accepts keyword arguments.
        - **kwargs: Arbitrary keyword arguments that are passed to the `func_obj`. This allows for flexible function calls,
          adapting to the requirements of `func_obj`.
    
        Returns:
        - A dictionary containing the key "result", with its value being the result of executing `func_obj` with `**kwargs`.
          This design facilitates the standardization of return values, making it easier to handle results at the call site.
        """
        # Executes the passed coroutine function object with the given keyword arguments and returns the result in a dictionary
        return {"result": await func_obj(**kwargs)}

    @show_time
    async def judge_intent(self, content: Dict[str, str], sessionId: str, reflection_text: str) -> dict:
        """
        Determine the user's intent and return the corresponding response.

        Args:
            content (Dict[str, str]): User input content in dictionary format, containing "role" and "content" keys.
            sessionId (str): Session ID used to identify the current user's session.

        Returns:
            dict: Dictionary containing response information, including "role", "content", and possibly other related keys.
        """
        # Try to load the session memory from storage
        try:
            mentarc_memory = json.loads(self.memory.get(sessionId))
        except:
            mentarc_memory = None
        # Initialize session memory if it does not exist
        if mentarc_memory is None:
            message = [{"role": "system", "content": self.instructions},]
            mentarc_memory = {
                "websearch_messages": message,
            }
        else:
            message = mentarc_memory["websearch_messages"]

        # Truncate messages if they exceed a certain length to manage memory efficiently
        if len(message) > 20:
            last_messages = message[-10:]
            pre_messages = message[:-10]
            temp_message = []
            for temp_msg in pre_messages[::-1]:
                if temp_msg["role"] == "user":
                    temp_message.append(temp_msg)
                    break
                temp_message.append(temp_msg)
            message = [message[0]] + temp_message[::-1] + last_messages

        # Update the system message with the current date
        temp_systemp = message[0]["content"]
        start_index = temp_systemp.find('$$')
        end_index = start_index + 2
        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        message[0]["content"] = temp_systemp[:end_index] + str({"Current Time is":f"{year}年{month}月{day}日"})

        # Append the user's input to the message history
        message.append(content)

        # Get the response from the language model if the last message is not a function call（For reduce time）
        if message[-1]["role"] != "function": 
            inquiry_response = self.llm.get_response(message, tools=self.functions, max_tokens=self.max_tokens)
        else:
            inquiry_response = {"text": content["content"],"functionCall":None}
            
        # Handle function calls in the response
        if inquiry_response['functionCall']:

            message.append(
                {"role": "assistant", "functionCall": inquiry_response['functionCall']})

            # Parse the function call arguments
            productData = ast.literal_eval(
                inquiry_response['functionCall']["arguments"])
            
            # Update session memory with the new message history
            mentarc_memory["websearch_messages"] = message
            self.memory.set(sessionId, json.dumps(mentarc_memory))

            # Return the function call result
            return {"role": "function", "name": inquiry_response['functionCall']["name"], "content": f"{productData} has completed its search and display to customer!", }, productData

        else:
            # Append the assistant's response to the message history
            message.append(
                {"role": "assistant", "content": inquiry_response["text"], })
            
            # Update session memory with the new message history
            mentarc_memory["websearch_messages"] = message
            self.memory.set(sessionId, json.dumps(mentarc_memory))

            # Return the assistant's response
            return {"role": "assistant", "content": inquiry_response["text"], }, None


async def __call__(self, data: Union[Dict[str, Any], List[str]], **kwargs) -> dict:
    """
    Asynchronous callable method that processes input data and determines the intent to perform corresponding operations.

    Parameters:
    - data: A dictionary or list containing the input information, including "input" and "sessionId" fields.
    - **kwargs: Additional keyword arguments.

    Returns:
    - dict: The result of the operation.
    """
    # Initialize user input content
    content = {"role": "user", "content": data["input"]}

    # Initialize role and reflection text
    role = "function"
    reflection_text = ""

    # if_source = False # Tag:判断是否需要sourcing产品
    # Loop until the role is "assistant"
    while role != "assistant":
        # Judge intent and get response content
        content, productData = await self.judge_intent(
            content, data['sessionId'], reflection_text)
        role = content["role"]
        if productData is not None:
            # Get function object based on content name
            func_obj = TOOLS[content["name"].lower()]["function"]
            # Execute function and get result
            productData['sessionId'] = data['sessionId']
            productData["test"] = data["test"]
            productData["input"] = data["input"]
            func_call_info = await self.apply_func_obj(func_obj, **productData)
            # Update reflection information
            content["content"] = str(func_call_info["result"][1])  # reflection_text

    # Return the final content
    return content["content"]