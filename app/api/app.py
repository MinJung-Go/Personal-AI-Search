'''
Author: MinJung
Date: 2024-12-10 08:26:25
LastEditors: MinJung
LastEditTime: 2025-02-21 06:24:54
# -*- Power By FocusAIM -*-
'''


import chainlit as cl
import logging

from app.api.main import AgenticSearch

logging.getLogger("httpx").setLevel(logging.ERROR)

AS = AgenticSearch()
@cl.on_message
async def run_conversation(message: cl.Message):
    response = await AS.__call__({'input': message.content,'sessionId':cl.user_session.get("id")})

    msg = cl.Message(author="Assistant", content="")
    await msg.send()
    msg.content = response["data"]["intentData"]["text"]#message_gpt["text"]
    await msg.update()
    