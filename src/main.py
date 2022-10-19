import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from module.Handler import *
from src.settings import Global, Setup, VoiceSetup

load_dotenv()

API_ID = int(os.getenv('api_id'))
API_HASH = os.getenv('api_hash')

Global.client = TelegramClient('Alex', API_ID, API_HASH)
Global.setup = Setup()  # True, True, True, True, True, True, True, True
Global.transcribe = VoiceSetup(True)


# TODO Реализовать обработку новых сообщений
@Global.client.on(events.NewMessage(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def new_message_handler(event):
    """Событие нового сообщения"""

    new_message.main(Global.client, event)


# TODO Реализовать обработку прочитанных сообщений
@Global.client.on(events.MessageRead(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def read_handler(event):
    """Событие чтения сообщения"""
    read_massge.main(Global.client, event)


# TODO Реализовать редактирование сообщений
@Global.client.on(
    events.MessageEdited(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def edit_handler(event):
    """Событие редактирование сообщения"""
    edit_message.main(Global.client, event)


# TODO Реализовать удаление сообщений
@Global.client.on(
    events.MessageDeleted(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def delete_handler(event):
    """Событие удаление сообщения"""
    delete_message.main(Global.client, event)


# TODO Реализовать обработчик событий чата
@Global.client.on(events.ChatAction(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def chat_handler(event):
    """События чата"""
    if event.action_message:
        chat_event.action_message(Global.client, event)
    elif event.new_pin:
        chat_event.new_pin(Global.client, event)
    elif event.new_photo:
        if event.photo:
            chat_event.new_photo(Global.client, event)
        else:
            chat_event.delete_photo(Global.client, event)
    elif event.user_added:
        chat_event.user_added(Global.client, event)
    elif event.user_joined:
        chat_event.user_joined(Global.client, event)
    elif event.user_left:
        chat_event.user_left(Global.client, event)
    elif event.user_kicked:
        chat_event.user_kicked(Global.client, event)
    elif event.created:
        chat_event.created(Global.client, event)
    elif event.new_title:
        chat_event.new_title(Global.client, event)
    elif event.new_score:
        chat_event.new_score(Global.client, event)
    elif event.unpin:
        chat_event.unpin(Global.client, event)
    else:
        raise TypeError("Error type event")


# TODO Реализовать обработку событий пользователя
@Global.client.on(events.UserUpdate(func=lambda e: e.chat_id in Global.listen_chats or len(Global.listen_chats) == 0))
async def user_handler(event):
    """События пользователя"""
    user_event.main(Global.client, event)


# TODO  Реализовать изначальную настройку клиента
async def main():
    await starting_configuration.update()


if __name__ == '__main__':
    with Global.client:
        Global.client.loop.run_until_complete(main())
        Global.client.run_until_disconnected()
