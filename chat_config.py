import telethon
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeImageSize, DocumentAttributeFilename, \
    DocumentAttributeSticker, MessageMediaContact, MessageMediaWebPage, MessageActionPhoneCall, MessageMediaPhoto, \
    MessageMediaDocument, MessageMediaGeo
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
            print('err')
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


async def new_message(event, client):
    chat_id = event.chat_id
    db.transactions("SELECT active FROM chat WHERE chat_id={}".format(chat_id))
    tracking = db.cursor.fetchone()[0]
    print(await get_member(event, client))
    print(await type_message(event.message))
    if tracking:
        print(event.message.to_dict()['message'])
    # else:
    #     print(event.message.to_dict()['message'])
