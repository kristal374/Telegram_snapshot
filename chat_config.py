from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeImageSize, DocumentAttributeFilename, \
    DocumentAttributeSticker, MessageMediaContact, MessageMediaWebPage, MessageActionPhoneCall, MessageMediaPhoto, \
    MessageMediaDocument, MessageMediaGeo
from datebase import DataBase
from const import *
from pytz import timezone
import time
import io
import AudioDownloader

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

async def update_chat_log(client):
    pass

async def all_message(client, chat):
    id_ = exist_chat(chat)[0]
    if not exist_chat(id_):
        db.transactions(CREATE_CHAT_LOG.format(id_))

    cursor = db.cursor_transactions(ALL_MESSAGE.format(id_))
    async for message in client.iter_messages(chat, reverse=True):
        for row in cursor:
            id_bd, mes_id, mes_text, type_ = row
            mes_db = (mes_id, mes_text)
            mes_ch = (message.id, message.text if message.text else None)
            if mes_db[0] == mes_ch[0]:
                if mes_db[1] != mes_ch[1] and type_ != 'VoiceMessage':
                    db.transactions(MESSAGE_UPDATE.format(id_, mes_ch[1], id_bd))
                break
            else:
                db.transactions(MESSAGE_DELETE.format(id_, id_bd))
        else:
            await add_message(client, message, chat)
    else:
        for row in cursor:
            id_bd, *_ = row
            db.transactions(MESSAGE_DELETE.format(id_, id_bd))

async def add_message(client, message, chat, config=None):
    res = exist_chat(chat)
    if res is None:
        await new_chat(client, chat)
        res = exist_chat(chat)
    elif res is not None and not res[1]:
        return
    id_ = res[0]
    configure = await config_message(client, message) if not config else config
    log_message_add(id_, configure)

async def get_member(message, client):
    async def get_name(ID):
        if not ID:
            return None
        db.transactions(SELECT_AUTHOR.format(ID))
        name = db.cursor.fetchone()
        if not name:
            try:
                name = (await client.get_entity(ID))
                name = f"{name.first_name} {name.last_name if name.last_name else ''}".strip()
            except AttributeError:
                name = (await client.get_entity(ID)).title
            except:
                name = 'UNEXPECTED_ERROR'
            class_ = {message.is_channel: "channel", message.is_group: "group", message.is_private: "user"}[True]
            db.defender_transaction(ADD_AUTHOR, name, ID, class_)
            return name
        return name[0]

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
        type_mes = TYPE_PHOTO
    elif isinstance(message.media, MessageMediaWebPage):
        type_mes = TYPE_LINK
    elif isinstance(message.action, MessageActionPhoneCall):
        type_mes = TYPE_PHONE_CALL
    elif isinstance(message.media, MessageMediaGeo):
        type_mes = TYPE_GEO
    elif isinstance(message.media, MessageMediaContact):
        type_mes = TYPE_CONTACT
    elif isinstance(message.media, MessageMediaDocument) and message.video is not None:  # video
        if message.video.attributes[0].round_message is True:
            type_mes = TYPE_CIRCULAR_VIDEO
        elif len(message.video.attributes) in (1, 2):
            type_mes = TYPE_VIDEO
        elif len(message.video.attributes) == 3:
            type_mes = TYPE_GIF
    elif message.media is not None:
        if isinstance(message.media.document.attributes[0], DocumentAttributeAudio):
            if len(message.media.document.attributes) == 2:
                type_mes = TYPE_MUSIC
            else:
                type_mes = TYPE_VOICE_MES
        elif isinstance(message.media.document.attributes[0], DocumentAttributeImageSize):
            target = message.media.document.attributes
            if type(target[1]) == DocumentAttributeSticker:
                type_mes = TYPE_STICKER
            elif type(target[1]) == DocumentAttributeFilename:
                type_mes = TYPE_PHOTO_FILE
        elif isinstance(message.media.document.attributes[0], DocumentAttributeFilename):
            if message.media.document.mime_type == 'application/pdf':
                type_mes = TYPE_PDF
            elif message.media.document.thumbs is not None:
                type_mes = TYPE_VIDEO_FILE
            else:
                type_mes = TYPE_FILE
    elif message.text != '':
        type_mes = TYPE_TEXT
    else:
        type_mes = TYPE_ERROR_FILE
    return type_mes

async def new_chat(client, chat_id):
    async for dialog in client.iter_dialogs():
        if dialog.id == chat_id:
            db.defender_transaction(ADD_NOTE_CHAT, *info(dialog))
            return
    return

async def get_text(client, message):
    buf = io.BytesIO()
    await client.download_media(message=message, file=buf)
    buf.seek(0)
    return AudioDownloader.audio_to_text(buf)

async def config_message(client, message):  # config message
    message_id = message.id
    author, author_id, real_author, real_author_id = await get_member(message, client)
    type_ = await type_message(message)
    text_message = message.text if type_ != 'VoiceMessage' else await get_text(client, message)
    text_message = text_message if text_message != '' else None
    date = time.mktime(message.date.astimezone(zone).timetuple())
    id_stack = message.grouped_id
    message = LOAD_FILE.get(type_)
    note = (message_id, author, author_id, real_author, real_author_id, text_message, message, date, id_stack, type_, 0, 0, None)
    return note

def exist_chat(chat_id):  # test on life log_chat
    db.transactions(DETECTED.format(chat_id))
    return db.cursor.fetchone()

def log_message_add(id_, conf):  # add message configuration in db chat
    if not exist_chat(id_):
        db.transactions(CREATE_CHAT_LOG.format(id_))
    db.defender_transaction(ADD_CHAT_MESSAGE.format(id_), *conf)

async def new_message_event(event, client):
    await add_message(client, event.message, event.chat_id)
