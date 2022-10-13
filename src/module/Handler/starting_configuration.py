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
    async for dialog in Global.client.iter_dialogs():
        await get_chat_info(dialog)

