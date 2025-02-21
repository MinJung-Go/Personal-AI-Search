import os
import redis
import logging
logging.getLogger("httpx").setLevel(logging.ERROR)

# the personal redis pool
# For details about how to install redis, see: https://www.oryoy.com/news/python-huan-jing-xia-de-redis-an-zhuang-yu-pei-zhi-quan-gong-lve-xiao-bai-ye-neng-qing-song-shang-sh.html
MEMORY = redis.Redis(host=os.environ("REDIS_URL","****"), port=os.environ("REDIS_PORT","****"), db=0, password=os.environ("REDIS_PASSWORD", "****"))  

GPT_URL = os.environ.get("GPT_URL", "https://api.openai.com/v1/chat/completions") # The API URL of the GPT model
GPT_API_KEY = os.environ.get("GPT_API_KEY", "*************")
DEEPSEEK_URL = os.environ.get("DEEPSEEK_URL", "https://ark.cn-beijing.volces.com/api/v3/chat/completions") # The API URL of the DeepSeek model
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "*************")


BING_URL = os.environ.get("BING_URL", 'https://api.bing.microsoft.com/v7.0/search') # The API URL of the Bing Search
BING_API_KEY = os.environ.get("BING_API_KEY", "*************")