'''
Author: MinJung & Chen
Date: 2024-12-10 08:26:25
LastEditors: MinJung
LastEditTime: 2025-02-21 06:32:59
# -*- Power By FocusAIM -*-
'''

from bs4 import BeautifulSoup 
import httpx as requests
from concurrent.futures import ThreadPoolExecutor
from core.llm import LLM
from config import WST_PROMPT, BING_URL, BING_API_KEY

import chainlit as cl

class WebSearch:
    def __init__(self):
        self.subscription_key = BING_API_KEY # The Bing Search API Key from Azure
        self.endpoint = BING_URL

        self.llm = LLM(model="volcengine_deepseek-reasoner")
        self.llm_gpt = LLM(model="gpt-4o")

    def web_search_bing(self, query: str, page_num: int = 2):
        """
        Perform a web page search using the Bing Search API.

        Parameters:
        query (str): The search keyword.
        page_num (int): The number of pages to return, default is 2.

        Returns:
        tuple: A tuple containing a list of URLs and a list of titles.
        """
        search_urls = []
        titles = []
        mkt = 'en-US'
        params = { 'q': query, 'mkt': mkt,'count': page_num*10 }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }
        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            web_content = response.json()
            search_urls = [single_page["url"] for single_page in web_content["webPages"]["value"]]
            titles = [single_page["name"] for single_page in web_content["webPages"]["value"]]
        except Exception as e:
            print(e)
        return search_urls,titles
    def extract_url_content(self, url: str):
        """
        Extracts the text content from the HTML at the specified URL.
        
        Parameters:
        url (str): The URL from which to extract content.
        
        Returns:
        str: The extracted text content, or an empty string if the extraction fails.
        """
        # Set request headers to simulate a browser visit
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            # Send a GET request to the specified URL with headers and timeout settings
            response = requests.get(url, headers=headers, timeout=3)
            # If the request is successful, process the response content
            if response.status_code == 200:
                response.raise_for_status()  # 检查请求是否成功
                # Use BeautifulSoup to remove HTML tags
                soup = BeautifulSoup(response.content.decode('utf-8', errors='ignore'), 'html.parser')
                # Return the text content after removing tags
                text_content = soup.get_text(strip=True)
            else:
                # If the request status code is not 200, print an error message and return an empty string
                text_content = ""
                print(f"REQUEST ERROR: {response.status_code}")
        except Exception as e:
            # If an exception occurs during the request, print an error message and return an empty string
            print(f"REQUEST ERROR: {e}")
            return ""

        # Return the extracted text content
        return text_content
    
    async def __call__(self, userQuery: str, searchKeyWords: str, page_num: int = 2, **kwargs):
        """
        Asynchronous call method that processes user queries and searches for information.
        
        Parameters:
        - userQuery: User's query string.
        - searchKeyWords: Keywords for search.
        - page_num: Number of search result pages, default is 2.
        - **kwargs: Additional arguments, such as input for context.
        
        Returns:
        - respone_content: A dictionary containing search result content.
        - think_answer: A dictionary containing the output of deep thinking.
        """
        
        # Perform web search and multi-threaded processing of search results
        async with cl.Step(name="Bing Search", type="tool") as step:
            userQuery = searchKeyWords
            search_urls, search_title = self.web_search_bing(searchKeyWords, page_num)
            with ThreadPoolExecutor(max_workers=len(search_urls)) as executor:
                res = list(executor.map(self.extract_url_content, search_urls))
            
            respone_content = {}
            for idx in range(len((res))):
                # Store search results and titles in a dictionary for subsequent processing
                respone_content[f"Reference {idx}"] = search_title[idx] +"\n"+ res[idx]+"\n\n"
        
            step.output = respone_content
    
        # Perform deep thinking using a language model
        async with cl.Step(name="DeepThink",type="llm") as child_step:
            child_step.input = {"The Current User Question": kwargs["input"],"Supplementary":str(userQuery)}
            Conversation = [{
                "role": "system",
                "content": WST_PROMPT.format(ref_content=str(respone_content))
            },
            {"role": "user", "content": str({"The Current User Question":kwargs["input"],"Supplementary":str(userQuery)})}]
            think_answer = await self.llm.get_response_async(Conversation)
            child_step.output = think_answer['reasoningContent']
    
            return respone_content, think_answer["text"]

