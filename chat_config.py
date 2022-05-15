from telethon import *
from datebase import DataBase
from const import *

db = DataBase(name=DB_NAME)

def info(dialog):
    chat_id = dialog.id
    name = dialog.name
    class_ = {dialog.is_channel: "channel", dialog.is_group: "group", dialog.is_user: "user"}[True]
    phone = dialog.entity.phone if class_ == 'user' else None
    phone = int(phone) if phone else None
    try:
        teg = dialog.entity.username
        teg = teg if teg else None
    except AttributeError:
        teg = None
    status = "1"
    active = "1" if class_ is not "channel" else "0"
    return chat_id, name, class_, phone, teg, status, active


async def chat_update(client):
    channel_id = []
    async for dialog in client.iter_dialogs():
        db.transactions(ENTRY_CHECK.format(dialog.id))
        chat = db.cursor.fetchone()
        config = info(dialog)
        channel_id.append(config[0])
        if not chat:
            db.defender_transaction(ADD_NOTE_CHAT, *config)
        elif config[:-2:] != chat[1:-2:]:
            ID = chat[0]
            db.transactions(UPDATE_NOTE.format(*config[1:-1:], ID))
    db.transactions(GET_CHANNEL_ID)
    for id_ in db.cursor.fetchmany(0):
        if id_[0] not in channel_id:
            db.transactions(UPDATE_STATUS.format(id_[0]))



