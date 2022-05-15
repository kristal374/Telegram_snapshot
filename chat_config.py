from telethon import *
from datebase import DataBase
from const import *

db = DataBase(name=DB_NAME)

def info(dialog):
    chat_id = dialog.id
    name = dialog.name
    class_ = {dialog.is_channel: "channel", dialog.is_group: "group", dialog.is_user: "user"}[True]
    phone = dialog.entity.phone if class_ == 'user' else 'NULL'
    phone = phone if phone else 'NULL'
    try:
        teg = dialog.entity.username
        teg = teg if teg else 'NULL'
    except AttributeError:
        teg = 'NULL'
    status = True
    return chat_id, name, class_, phone, teg, status


async def chat_update(client):
    async for dialog in client.iter_dialogs():
        db.transactions(ENTRY_CHECK.format(dialog.id))
        chat = db.cursor.fetchone()
        if chat:
            pass
        else:
            db.transactions(ADD_NOTE_CHAT.format(*info(dialog)))

