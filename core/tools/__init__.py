'''
Author: MinJung
Date: 2024-12-10 08:26:25
LastEditors: MinJung
LastEditTime: 2025-02-21 06:41:55
# -*- Power By FocusAIM -*-
'''

from core.tools.web_search import WebSearch


TOOLS = {
    "web_search": {
        "function": WebSearch(),
        "function_call":{
                "name": "web_search",
                "description": "bing search and deep think, based key words to search web, and combined with the user's questions and search data, give a preliminary analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "userQuery": {
                            "type": "string",
                            "description": "the question from user"
                        },
                        "searchKeyWords": {
                            "type": "string",
                            "description": "the key words from user's query"
                        }
                    },
                    "required": ["userQuery","searchKeyWords"]
                }
        }
    },
}