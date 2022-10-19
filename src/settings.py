from pytz import timezone
from src.module.Audio_translator.translator import *


class Global:
    client = None  # Главный экземпляр Telegram API
    setup = None  # Главный экземпляр настроек
    transcribe = None
    db = None
    zone = timezone('Europe/Kiev')
    listen_chats = [None]


class MessageType:
    CONTACT = 'Contact'
    DOCUMENT = "Document"
    GAME = "Game"
    GEO_LIVE = "GeoLive"
    PHOTO = 'Photo'
    UNSUPPORTED = 'MessageMediaUnsupported'
    LINK = 'Link'
    DICE = 'DICE'
    EMPTY = "Empty"
    GEO = 'GeoPosition'
    INVOICE = "Invoice"
    Poll = 'Poll'
    VENUE = "Venue"

    MUSIC = "Music"
    VOICE_MES = "VoiceMessage"
    STICKER = 'Sticker'
    GIF = "GIF"
    VIDEO = 'Video'
    CIRCULAR_VIDEO = "CircularVideo"
    PHOTO_FILE = 'PhotoFile'
    VIDEO_FILE = 'VideoFile'
    FILE = 'File'

    TEXT = 'Text'

    ERROR_MESSAGE = 'ErrorTypeFile'


class MessagesInfoEvent:
    GIFT_PREMIUM = "GiftPremium"
    WEB_VIEW_DATA_SENT = "WebViewDataSent"
    WEB_VIEW_DATA_SENT_ME = 'WebViewDataSentMe'
    CHAT_JOINED_BY_REQUEST = 'ChatJoinedByRequest'
    SET_CHAT_THEME = 'SetChatTheme'
    GROUP_CALL_SCHEDULED = 'GroupCallScheduled'
    SET_MESSAGES_TTL = 'SetMessagesTTL'
    INVITE_TO_GROUP_CALL = 'InviteToGroupCall'
    GROUP_CALL = 'GroupCall'
    GEO_PROXIMITY_REACHED = 'GeoProximityReached'
    CONTACT_SIGN_UP = 'ContactSignUp'
    SECURE_VALUES_SENT = 'SecureValuesSent'
    SECURE_VALUES_SENT_ME = 'SecureValuesSentMe'
    BOT_ALLOWED = 'BotAllowed'
    CUSTOM_ACTION = 'CustomAction'
    SCREENSHOT_TAKEN = 'ScreenshotTaken'
    PAYMENT_SENT = 'PaymentSent'
    PAYMENT_SENT_ME = 'PaymentSentMe'
    GAME_SCORE = 'WebViewDataSentMe'
    HISTORY_CLEAR = 'HistoryClear'
    PIN_MESSAGE = 'PinMessage'
    CHAT_MIGRATE_FROM = 'ChannelMigrateFrom'
    CHAT_MIGRATE_TO = 'ChatMigrateTo'
    CHANNEL_CREATE = 'ChannelCreate'
    JOINED_BY_LINK = 'ChatJoinedByLink'
    DELETE_USER = 'ChatDeleteUser'
    ADD_USER = 'ChatAddUser'
    DELETE_PHOTO = 'ChatDeletePhoto'
    EDIT_PHOTO = 'ChatEditPhoto'
    EDIT_TITLE = 'ChatEditTitle'
    CHAT_CREATE = 'ChatCreate'
    EMPTY = 'Empty'
    PHONE_CALL = 'PhoneCall'

    def __eq__(self, other):
        lst = (self.GIFT_PREMIUM,
               self.WEB_VIEW_DATA_SENT,
               self.WEB_VIEW_DATA_SENT_ME,
               self.CHAT_JOINED_BY_REQUEST,
               self.SET_CHAT_THEME,
               self.GROUP_CALL_SCHEDULED,
               self.SET_MESSAGES_TTL,
               self.INVITE_TO_GROUP_CALL,
               self.GROUP_CALL,
               self.GEO_PROXIMITY_REACHED,
               self.CONTACT_SIGN_UP,
               self.SECURE_VALUES_SENT,
               self.SECURE_VALUES_SENT_ME,
               self.BOT_ALLOWED,
               self.CUSTOM_ACTION,
               self.SCREENSHOT_TAKEN,
               self.PAYMENT_SENT,
               self.PAYMENT_SENT_ME,
               self.GAME_SCORE,
               self.HISTORY_CLEAR,
               self.PIN_MESSAGE,
               self.CHAT_MIGRATE_FROM,
               self.CHAT_MIGRATE_TO,
               self.CHANNEL_CREATE,
               self.JOINED_BY_LINK,
               self.DELETE_USER,
               self.ADD_USER,
               self.DELETE_PHOTO,
               self.EDIT_PHOTO,
               self.EDIT_TITLE,
               self.CHAT_CREATE,
               self.EMPTY,
               self.PHONE_CALL)
        return other in lst


class VoiceSetup:
    def __init__(self, transcribe=False, model_translator=GoogleRecognize, lang="ru"):
        self.transcribe = transcribe
        self.model_translator = model_translator
        self.lang = lang


class Setup:
    default = {
        MessageType.PHOTO: 15,
        MessageType.CIRCULAR_VIDEO: 20,
        MessageType.VIDEO: 50,
        MessageType.MUSIC: 7,
        MessageType.VOICE_MES: 15,
        MessageType.PHOTO_FILE: 15,
        MessageType.VIDEO_FILE: 50,
        MessageType.FILE: 25
    }

    def __init__(self, type_photo=False, type_circular_video=False, type_video=False,
                 type_music=False, type_voice_mes=False, type_photo_file=False,
                 type_video_file=False, type_file=False):
        """
        Каждый из параметров принимает на вход одно из следующих значений
        - False: Данный тип сообщений не будет загружаться.
        - True: Данный тип сообщений будет загружаться с настройками по умолчанию.
        - None: Данный тип сообщений будет загружен в не зависимости от размера сообщения.
        - int: Пользовательский тип. Позволяет указать максимальный допустимый размер media
        сообщения в МБ который будет загружен.
        """
        self.default[MessageType.PHOTO] = type_photo if self.__bring_to_format(type_photo) != -1 else self.default[MessageType.PHOTO]
        self.default[MessageType.CIRCULAR_VIDEO] = type_circular_video if self.__bring_to_format(type_circular_video) != -1 else self.default[MessageType.CIRCULAR_VIDEO]
        self.default[MessageType.VIDEO] = type_video if self.__bring_to_format(type_video) != -1 else self.default[MessageType.VIDEO]
        self.default[MessageType.MUSIC] = type_music if self.__bring_to_format(type_music) != -1 else self.default[MessageType.MUSIC]
        self.default[MessageType.VOICE_MES] = type_voice_mes if self.__bring_to_format(type_voice_mes) != -1 else self.default[MessageType.VOICE_MES]
        self.default[MessageType.PHOTO_FILE] = type_photo_file if self.__bring_to_format(type_photo_file) != -1 else self.default[MessageType.PHOTO_FILE]
        self.default[MessageType.VIDEO_FILE] = type_video_file if self.__bring_to_format(type_video_file) != -1 else self.default[MessageType.VIDEO_FILE]
        self.default[MessageType.FILE] = type_file if self.__bring_to_format(type_file) != -1 else self.default[MessageType.FILE]

    @staticmethod
    def __bring_to_format(val):
        if isinstance(val, int) and val < 0:
            raise TypeError("Значение не может быть меньше 0")
        if val is None:
            return None
        elif val is False:
            return False
        elif val is True:
            return -1
        else:
            return val

    def download_this(self, type_message, size):
        if self.default.get(type_message, -1) == -1:
            return False
        elif self.default[type_message] is False:
            return False
        elif self.default[type_message] is None:
            return True
        else:
            if self.default[type_message] >= int(size/(2**20)):
                return True
            return False


MessageEvent = MessagesInfoEvent()
