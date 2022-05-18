import telethon
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeImageSize, DocumentAttributeFilename, \
    DocumentAttributeSticker, MessageMediaContact, MessageMediaWebPage, MessageActionPhoneCall, MessageMediaPhoto, \
    MessageMediaDocument, MessageMediaGeo
from datebase import DataBase
from const import *
from pytz import timezone
import time

zone = timezone('Europe/Kiev')
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
    status = 1
    active = 1 if class_ is not "channel" else 0
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
            db.defender_transaction(UPDATE_NOTE.format(ID), *config[1:-1:])
    db.transactions(GET_CHANNEL_ID)
    for id_ in db.cursor.fetchmany(0):
        if id_[0] not in channel_id:
            db.transactions(UPDATE_STATUS.format(id_[0]))

async def get_member(event, client):
    async def get_name(ID):
        if not ID:
            return None
        db.transactions(SELECT_AUTHOR.format(ID))
        name = db.cursor.fetchone()
        if not name:
            try:
                name = (await client.get_entity(ID))
                name = f"{name.first_name} {name.last_name if name.last_name else ''}".strip()
            except:
                name = (await client.get_entity(ID)).title
            class_ = {event.is_channel: "channel", event.is_group: "group", event.is_private: "user"}[True]
            db.defender_transaction(ADD_AUTHOR, name, ID, class_)
            return name
        return name[0]

    message = event.message
    sender_id = message.sender_id  # id user which send message
    real_sender_id = None
    real_sender_name = None
    if message.forward is not None:  # replace message
        real_sender_id = message.forward.sender_id
        if real_sender_id is None:
            real_sender_id = message.forward.chat_id
        if real_sender_id is None:
            real_sender_name = message.forward.from_name
    real_sender_name = real_sender_name if real_sender_name else await get_name(real_sender_id)
    return await get_name(sender_id), sender_id, real_sender_name, real_sender_id

async def type_message(message):
    type_mes = None
    if isinstance(message.media, MessageMediaPhoto):
        type_mes = 'Photo'
    elif isinstance(message.media, MessageMediaWebPage):
        type_mes = 'Link'
    elif isinstance(message.action, MessageActionPhoneCall):
        type_mes = 'PhoneCall'
    elif isinstance(message.media, MessageMediaGeo):
        type_mes = 'GeoPosition'
    elif isinstance(message.media, MessageMediaContact):
        type_mes = 'Contact'
    elif isinstance(message.media, MessageMediaDocument) and message.video is not None:  # video
        if message.video.attributes[0].round_message is True:
            type_mes = "CircularVideo"
        elif len(message.video.attributes) in (1, 2):
            type_mes = 'Video'
        elif len(message.video.attributes) == 3:
            type_mes = "GIF"
    elif message.media is not None:
        if isinstance(message.media.document.attributes[0], DocumentAttributeAudio):
            if len(message.media.document.attributes) == 2:
                type_mes = "Music"
            else:
                type_mes = "VoiceMessage"
        elif isinstance(message.media.document.attributes[0], DocumentAttributeImageSize):
            target = message.media.document.attributes
            if type(target[1]) == DocumentAttributeSticker:
                type_mes = 'Sticker'
            elif type(target[1]) == DocumentAttributeFilename:
                type_mes = 'PhotoFile'
        elif isinstance(message.media.document.attributes[0], DocumentAttributeFilename):
            if message.media.document.mime_type == 'application/pdf':
                type_mes = 'PDF'
            elif message.media.document.thumbs is not None:
                type_mes = 'VideoFile'
            else:
                type_mes = 'File'
    elif message.text != 'Text':
        type_mes = 'Text'
    else:
        type_mes = 'ErrorTypeFile'
    return type_mes

async def new_chat(client, chat_id):
    async for dialog in client.iter_dialogs():
        if dialog.id == chat_id:
            db.defender_transaction(ADD_NOTE_CHAT, *info(dialog))
            return
    return

async def new_message(event, client):
    chat_id = event.chat_id
    db.transactions(DETECTED.format(chat_id))

    res = db.cursor.fetchone()
    if res is None:
        await new_chat(client, chat_id)
        db.transactions(DETECTED.format(chat_id))
        res = db.cursor.fetchone()
    elif res is not None and not res[1]:
        return
    id_ = res[0]
    author, author_id, real_author, real_author_id = await get_member(event, client)
    text_message = event.message.text
    date = time.mktime(event.message.date.astimezone(zone).timetuple())
    id_stack = event.message.grouped_id
    type_ = await type_message(event.message)
    message = LOAD_FILE.get(type_)
    note = (author, author_id, real_author, real_author_id, text_message, message, date, id_stack, type_, 0)

    db.transactions(DETECTED.format(id_))
    if not db.cursor.fetchone():
        db.transactions(CREATE_CHAT_LOG.format(id_))
    db.defender_transaction(ADD_CHAT_MESSAGE.format(id_), *note)
