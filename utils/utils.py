
'''
Author: MinJung
Date: 2024-12-10 08:26:25
LastEditors: MinJung
LastEditTime: 2025-02-21 06:28:33
# -*- Power By FocusAIM -*-
'''

from functools import wraps
import time

def show_time(func):
    """
    计算函数运行时间
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        if hasattr(func, '__qualname__'):
            func_name = func.__qualname__
        else:
            func_name = func.__name__
        print(f"{func_name} 运行时间：{end_time - start_time} 秒")
        return result

    return wrapper

