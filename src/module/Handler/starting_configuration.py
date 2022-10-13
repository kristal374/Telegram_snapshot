from ..Data_base_handler import *
from src.settings import Global
from .manager import *
import time


async def update():
    chats = requests.get_all_chat()
    if len(chats) != 0:
        pass
    else:
        await configuration_chats()


async def configuration_chats():
    tm = time.clock()
    async for dialog in Global.client.iter_dialogs():
        requests.add_new_chat(await get_chat_info(dialog))
        async for message in Global.client.iter_messages(dialog.id, reverse=True):
            requests.add_new_message(await get_message_info(message))
    print(time.clock()-tm)
