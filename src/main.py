import os

from dotenv import load_dotenv
from telethon import TelegramClient, events

from module.handler import *

# func=lambda e: e.chat_id not in indexed_chats
load_dotenv()

API_ID = int(os.getenv('api_id'))
API_HASH = os.getenv('api_hash')

client = TelegramClient('Alex', API_ID, API_HASH)


# TODO Реализовать обработку новых сообщений
@client.on(events.NewMessage(func=None))
async def new_message_handler(event):
    """Событие нового сообщения"""
    new_message.main(client, event)


# TODO Реализовать обработку прочитанных сообщений
@client.on(events.MessageRead(func=None))
async def read_handler(event):
    """Событие чтения сообщения"""
    read_massge.main(client, event)


# TODO Реализовать редактирование сообщений
@client.on(events.MessageEdited(func=None))
async def edit_handler(event):
    """Событие редактирование сообщения"""
    edit_message.main(client, event)


# TODO Реализовать удаление сообщений
@client.on(events.MessageDeleted(func=None))
async def delete_handler(event):
    """Событие удаление сообщения"""
    delete_message.main(client, event)


# TODO Реализовать обработчик событий чата
@client.on(events.ChatAction(func=None))
async def chat_handler(event):
    """События чата"""
    chat_event.main(client, event)
    if event.action_message:
        ...
    elif event.new_pin:
        "Сообщение закреплено"
        ...
    elif event.new_photo:
        "Фото изменено"
        ...
        if event.photo:
            "Новое фото"
            ...
        else:
            "Фото удалено"
            ...
    elif event.user_added:
        "Кто-то добавил пользователя"
        ...
    elif event.user_joined:
        "Пользователь присоединился сам"
        ...
    elif event.user_left:
        "Пользователь покинул чат"
        ...
    elif event.user_kicked:
        "Пользователя кто-то удалил"
        ...
    elif event.created:
        "Чат был только что создан"
        ...
    elif event.new_title:
        "Изменено название чата"
        ...
    elif event.new_score:
        "Новая строка счета для игры, если применимо"
        ...
    elif event.unpin:
        "Сообщение откреплено"
        ...
    else:
        raise TypeError("Error type event")


# TODO Реализовать обработку событий пользователя
@client.on(events.UserUpdate(func=None))
async def user_handler(event):
    """События пользователя"""
    user_event.main(client, event)


# TODO  Реализовать изначальную настройку клиента
async def main():
    pass


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
