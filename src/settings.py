
class Global:
    client = None  # Главный экземпляр Telegram API
    setup = None  # Главный экземпляр настроек
    db = None


class Setup:
    default = {
        "type_photo": 15,
        "type_circular_video": 20,
        "type_video": 50,
        "type_music": 7,
        "type_voice_mes": 15,
        "type_photo_file": 15,
        "type_video_file": 50,
        "type_pdf": 25,
        "type_file": 25
    }

    def __init__(self, type_photo=False, type_circular_video=False, type_video=False,
                 type_music=False, type_voice_mes=False, type_photo_file=False,
                 type_video_file=False, type_pdf=False, type_file=False):
        """
        Каждый из параметров принимает на вход одно из следующих значений
        - False: Данный тип сообщений не будет загружаться.
        - True: Данный тип сообщений будет загружаться с настройками по умолчанию.
        - None: Данный тип сообщений будет загружен в не зависимости от размера сообщения.
        - int: Пользовательский тип. Позволяет указать максимальный допустимый размер media
        сообщения в МБ который будет загружен.
        """
        self.type_photo = type_photo
        self.type_circular_video = type_circular_video
        self.type_video = type_video
        self.type_music = type_music
        self.type_voice_mes = type_voice_mes
        self.type_photo_file = type_photo_file
        self.type_video_file = type_video_file
        self.type_pdf = type_pdf
        self.type_file = type_file

    def download_this(self, type_message, size):
        if not type_message:
            return False
        elif type_message is None:
            return True
        elif type_message:
            # if self.default.type_message > size:
            #     return True
            return False
        else:
            return True
