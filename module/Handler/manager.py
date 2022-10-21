from dataclasses import dataclass
from module.settings import Global, MessageType, MessageEvent
from telethon.tl.functions import channels, users, messages
from telethon.tl.types import User, Channel, Chat,\
    MessageMediaPhoto, MessageMediaWebPage, MessageActionPhoneCall, MessageMediaGeo,\
    MessageMediaContact, MessageMediaPoll, MessageMediaUnsupported, MessageMediaDice,\
    MessageMediaDocument, MessageMediaGame, MessageMediaGeoLive, MessageMediaEmpty,\
    MessageMediaInvoice, MessageMediaVenue, MessageActionPinMessage, MessageActionEmpty,\
    MessageActionChatCreate, MessageActionChatEditTitle, MessageActionChatEditPhoto,\
    MessageActionChatDeletePhoto, MessageActionChatAddUser, MessageActionChatDeleteUser,\
    MessageActionChatJoinedByLink, MessageActionChannelCreate, MessageActionChatMigrateTo,\
    MessageActionChannelMigrateFrom, MessageActionHistoryClear, MessageActionGameScore, \
    MessageActionPaymentSentMe, MessageActionPaymentSent, MessageActionScreenshotTaken,\
    MessageActionCustomAction, MessageActionBotAllowed, MessageActionSecureValuesSentMe,\
    MessageActionSecureValuesSent, MessageActionContactSignUp, MessageActionGeoProximityReached,\
    MessageActionGroupCall, MessageActionInviteToGroupCall, MessageActionSetMessagesTTL,\
    MessageActionGroupCallScheduled, MessageActionSetChatTheme, MessageActionChatJoinedByRequest,\
    MessageActionWebViewDataSentMe, MessageActionWebViewDataSent, MessageActionGiftPremium
from telethon import utils, errors
from ..Data_base_handler import *
from ..Audio_translator import *
import io
import datetime
import time


async def get_name(id_):
    if not id_:
        return None
    info_author = requests.search_author(id_)

    if not info_author:
        this_author = AuthorStencil()
        try:
            profile = (await Global.client.get_entity(id_))
        except errors.rpcerrorlist.ChannelPrivateError:
            return "PrivateChannel"
        this_author.author_id = id_
        this_author.name = utils.get_display_name(profile)
        if not this_author.name:
            this_author.name = "RemoteAccount"
        if isinstance(profile, User):
            this_author.category = "user"
            this_author.phone = profile.phone
            this_author.tag = profile.username
        elif isinstance(profile, Channel):
            this_author.category = "channel"
        elif isinstance(profile, Chat):
            this_author.category = "group"
        else:
            raise TypeError("Непредвиденный тип группы/пользователя")
        requests.add_new_author(this_author)
        return this_author.name
    return info_author.name


async def original_sender(message):
    real_sender_id = None
    real_sender_name = None
    if message.forward is not None:
        real_sender_id = message.forward.sender_id
        if real_sender_id is None:
            real_sender_id = message.forward.chat_id
        if real_sender_id is None:
            real_sender_name = message.forward.from_name
    real_sender_name = real_sender_name if real_sender_name else await get_name(real_sender_id)
    return real_sender_name, real_sender_id


async def type_message(message):
    if isinstance(message.media, MessageMediaContact):
        type_mes = MessageType.CONTACT
    elif isinstance(message.media, MessageMediaDocument):
        if utils.is_audio(message.media):
            if message.voice:
                type_mes = MessageType.VOICE_MES
            else:
                type_mes = MessageType.MUSIC

        elif message.gif:
            type_mes = MessageType.GIF

        elif message.media.document.mime_type in ('image/jpeg', 'image/png'):
            type_mes = MessageType.PHOTO_FILE

        elif utils.is_video(message.media):
            if message.video_note:
                type_mes = MessageType.CIRCULAR_VIDEO
            elif message.video:
                type_mes = MessageType.VIDEO
            else:
                type_mes = MessageType.VIDEO_FILE
        elif message.sticker:
            type_mes = MessageType.STICKER
        else:
            type_mes = MessageType.FILE

    elif isinstance(message.media, MessageMediaGame):
        type_mes = MessageType.GAME
    elif isinstance(message.media, MessageMediaGeoLive):
        type_mes = MessageType.GEO_LIVE
    elif isinstance(message.media, MessageMediaPhoto):
        type_mes = MessageType.PHOTO
    elif isinstance(message.media, MessageMediaUnsupported):
        type_mes = MessageType.UNSUPPORTED
    elif isinstance(message.media, MessageMediaWebPage):
        type_mes = MessageType.LINK
    elif isinstance(message.media, MessageMediaDice):
        type_mes = MessageType.DICE
    elif isinstance(message.action, MessageMediaEmpty):
        type_mes = MessageType.EMPTY
    elif isinstance(message.media, MessageMediaGeo):
        type_mes = MessageType.GEO
    elif isinstance(message.media, MessageMediaInvoice):
        type_mes = MessageType.INVOICE
    elif isinstance(message.media, MessageMediaPoll):
        type_mes = MessageType.Poll
    elif isinstance(message.media, MessageMediaVenue):
        type_mes = MessageType.VENUE
    elif message.action:
        type_mes = {
            MessageActionEmpty: MessageEvent.EMPTY,
            MessageActionChatCreate: MessageEvent.CHAT_CREATE,
            MessageActionChatEditTitle: MessageEvent.EDIT_TITLE,
            MessageActionChatEditPhoto: MessageEvent.EDIT_PHOTO,
            MessageActionChatDeletePhoto: MessageEvent.DELETE_PHOTO,
            MessageActionChatAddUser: MessageEvent.ADD_USER,
            MessageActionChatDeleteUser: MessageEvent.DELETE_USER,
            MessageActionChatJoinedByLink: MessageEvent.JOINED_BY_LINK,
            MessageActionChannelCreate: MessageEvent.CHANNEL_CREATE,
            MessageActionChatMigrateTo: MessageEvent.CHAT_MIGRATE_TO,
            MessageActionChannelMigrateFrom: MessageEvent.CHAT_MIGRATE_FROM,
            MessageActionPinMessage: MessageEvent.PIN_MESSAGE,
            MessageActionHistoryClear: MessageEvent.HISTORY_CLEAR,
            MessageActionGameScore: MessageEvent.GAME_SCORE,
            MessageActionPaymentSentMe: MessageEvent.PAYMENT_SENT_ME,
            MessageActionPaymentSent: MessageEvent.PAYMENT_SENT,
            MessageActionPhoneCall: MessageEvent.PHONE_CALL,
            MessageActionScreenshotTaken: MessageEvent.SCREENSHOT_TAKEN,
            MessageActionCustomAction: MessageEvent.CUSTOM_ACTION,
            MessageActionBotAllowed: MessageEvent.BOT_ALLOWED,
            MessageActionSecureValuesSentMe: MessageEvent.SECURE_VALUES_SENT_ME,
            MessageActionSecureValuesSent: MessageEvent.SECURE_VALUES_SENT,
            MessageActionContactSignUp: MessageEvent.CONTACT_SIGN_UP,
            MessageActionGeoProximityReached: MessageEvent.GEO_PROXIMITY_REACHED,
            MessageActionGroupCall: MessageEvent.GROUP_CALL,
            MessageActionInviteToGroupCall: MessageEvent.INVITE_TO_GROUP_CALL,
            MessageActionSetMessagesTTL: MessageEvent.SET_MESSAGES_TTL,
            MessageActionGroupCallScheduled: MessageEvent.GROUP_CALL_SCHEDULED,
            MessageActionSetChatTheme: MessageEvent.SET_CHAT_THEME,
            MessageActionChatJoinedByRequest: MessageEvent.CHAT_JOINED_BY_REQUEST,
            MessageActionWebViewDataSentMe: MessageEvent.WEB_VIEW_DATA_SENT_ME,
            MessageActionWebViewDataSent: MessageEvent.WEB_VIEW_DATA_SENT,
            MessageActionGiftPremium: MessageEvent.GIFT_PREMIUM
        }[type(message.action)]
    elif message.text:
        type_mes = MessageType.TEXT
    else:
        type_mes = MessageType.ERROR_MESSAGE

    return type_mes


def get_message_extension(message, type_):
    def is_mime_type():
        try:
            if message.file.mime_type:
                return True
            else:
                return False
        except AttributeError:
            return False

    if type_ in (MessageType.CONTACT, MessageType.GAME, MessageType.GEO_LIVE,
                 MessageType.UNSUPPORTED, MessageType.LINK, MessageType.DICE,
                 MessageType.GEO, MessageType.Poll, MessageType.VENUE, MessageType.TEXT,
                 MessageType.ERROR_MESSAGE):
        return None
    elif type_ in (MessageType.PHOTO_FILE, MessageType.VIDEO_FILE, MessageType.VIDEO,
                   MessageType.PHOTO, MessageType.CIRCULAR_VIDEO):
        return f".{message.file.mime_type.split('/')[-1]}"
    elif type_ is MessageType.DOCUMENT:
        if is_mime_type:
            return f"mime_type|{message.file.mime_type}"
        return None
    elif type_ is MessageType.EMPTY:
        if is_mime_type:
            return f"mime_type|{message.file.mime_type}"
        return None
    elif type_ is MessageType.INVOICE:
        if is_mime_type:
            return f"mime_type|{message.file.mime_type}"
        return None
    elif type_ is MessageType.MUSIC:
        return f".{message.media.document.attributes[-1].file_name.split('.')[-1]}"
    elif type_ is MessageType.VOICE_MES:
        return ".ogg"
    elif type_ is MessageType.STICKER:
        if message.file.mime_type == 'application/x-tgsticker':
            return '.tgs'
        else:
            return '.webp'
    elif type_ is MessageType.GIF:
        return ".gif"
    elif type_ is MessageType.FILE:
        return f".{message.media.document.attributes[-1].file_name.split('.')[-1]}"


async def load_media(message, type_):
    if not message.media or not message.file:
        return None
    if Global.setup.download_this(type_, message.file.size):
        buf = io.BytesIO()
        await Global.client.download_media(message=message, file=buf)
        buf.seek(0)
        return buf
    return None


async def get_message_text(message, type_):
    if type_ == MessageType.VOICE_MES and Global.transcribe.transcribe:
        voice_message = await load_media(message, type_)
        if voice_message:
            return translator.audio_to_text(Global.transcribe.model_translator,
                                            voice_message,
                                            lang=Global.transcribe.lang)
        return None
    elif type_ == MessageEvent.ADD_USER:
        return message.action.users[0]  # Некорректно ибо может быть больше одного добавленного пользователя
    elif type_ == MessageEvent.JOINED_BY_LINK:
        return message.action.inviter_id
    elif type_ == MessageEvent.DELETE_USER:
        return message.action.user_id
    elif type_ == MessageType.Poll:
        json_object = {}
        json_object.setdefault("question", message.media.poll.question)
        json_object.setdefault("answers", {})
        for i in range(len(message.media.poll.answers)):
            key = message.media.poll.answers[i].text  # Текст ответа
            if message.media.results.results:
                val = message.media.results.results[i].voters  # Количество проголосовавших за данный ответ
            else:
                val = None
            json_object["answers"].setdefault(key, val)
        return json_object.__str__()
    elif type_ == MessageType.CONTACT:
        return {"first_name": message.contact.first_name,
                "last_name": message.contact.last_name,
                "phone_number": message.contact.phone_number}
    elif type_ == MessageType.GEO:
        return {"lat": message.geo.lat,
                "long": message.geo.long}
    return message.text if message.text else None


async def get_description_account(dialog):
    if dialog.is_user:
        bio = (await Global.client(users.GetFullUserRequest(dialog.entity.id))).full_user.about
    elif dialog.is_channel:
        bio = (await Global.client(channels.GetFullChannelRequest(dialog.entity.id))).full_chat.about
    else:
        bio = (await Global.client(messages.GetFullChatRequest(dialog.entity.id))).full_chat.about
    return bio if bio else None


async def load_photo_profile(dialog):
    photo = io.BytesIO()
    await Global.client.download_profile_photo(dialog.id, file=photo)
    photo.seek(0)
    return photo.read()


async def get_chat_info(dialog):
    this_chat = ChatStencil()

    this_chat.chat_id = dialog.id
    this_chat.name = dialog.title if dialog.title else "RemoteAccount"
    this_chat.category = {dialog.is_channel: "channel", dialog.is_group: "group", dialog.is_user: "user"}[True]
    this_chat.phone = dialog.entity.phone if this_chat.category == 'user' else None
    this_chat.tag = dialog.entity.__dict__.get("username")
    this_chat.photo = await load_photo_profile(dialog)
    this_chat.bio = await get_description_account(dialog)
    this_chat.status = True
    this_chat.active = True if this_chat.category is not "channel" else False

    return this_chat


async def get_message_info(message):
    await get_name(message.sender_id)
    this_message = MessageStencil()

    this_message.type = await type_message(message)

    this_message.chat_id = message.chat_id
    this_message.message_id = message.id
    this_message.author_id = message.sender_id if message.sender_id else message.to_id.channel_id
    this_message.real_author, this_message.real_author_id = await original_sender(message)
    this_message.text_message = await get_message_text(message, this_message.type)
    this_message.reply = message.reply_to.reply_to_msg_id if message.is_reply else None
    this_message.message = (await load_media(message, this_message.type))
    this_message.message = this_message.message.read() if this_message.message else None
    this_message.extension = get_message_extension(message, this_message.type)
    this_message.time = time.mktime(message.date.astimezone(Global.zone).timetuple())
    this_message.id_stack = message.grouped_id
    this_message.redacted = False

    return this_message


@dataclass
class ChatStencil:
    chat_id: int = None
    name: str = None
    category: str = None
    phone: int = None
    tag: str = None
    photo: bytes = None
    bio: str = None
    status: bool = None
    active: bool = None
    date_create: datetime.datetime = None


@dataclass
class MessageStencil:
    chat_id: int = None
    message_id: int = None
    author_id: int = None
    real_author: str = None
    real_author_id: int = None
    text_message: str = None
    reply: int = None
    message: bytes = None
    extension: str = None
    time: datetime.datetime = None
    id_stack: int = None
    type: str = None
    redacted: bool = None
    deleted: datetime.datetime = None


@dataclass
class AuthorStencil:
    name: str = None
    author_id: int = None
    category: str = None
    phone: int = None
    tag: str = None
