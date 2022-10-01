import speech_recognition as sr
from audio_format_converter import convert_from_ogg
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import wave
from src.module.const import *

SetLogLevel(-1)


class InterfaceConverter:
    def __init__(self, file):
        self.file = file
        self.recognizer = None

    def preparing_file(self):
        sample_audio = sr.AudioFile(convert_from_ogg(self.file))
        self.recognizer = sr.Recognizer()

        with sample_audio as audio_file:
            self.recognizer.adjust_for_ambient_noise(audio_file)
            with open("test_audio.wav", 'wb') as f:
                f.write(audio_file.filename_or_fileobject.read())
            audio_content = self.recognizer.record(audio_file)

        return audio_content

    def convert_in_text(self, lang="ru"):
        raise NotImplementedError("Method not implemented")


class GoogleRecognize(InterfaceConverter):
    def convert_in_text(self, lang="ru"):
        content = self.preparing_file()
        try:
            text = self.recognizer.recognize_google(content, language='ru')
        except sr.UnknownValueError:
            text = 'Текст не распознан'
        except sr.RequestError:
            text = 'Ошибка во время преобразования'
        return text


class MyModelRecognize(InterfaceConverter):
    def preparing_file(self):
        model = Model(PATH_MODEL)
        sample_audio = wave.open(convert_from_ogg(self.file), 'rb')

        self.recognizer = KaldiRecognizer(model, sample_audio.getframerate())
        self.recognizer.SetMaxAlternatives(10)
        self.recognizer.SetWords(True)
        return sample_audio

    def convert_in_text(self, lang="ru"):
        wf = self.preparing_file()
        data = wf.readframes(wf.getnframes())
        self.recognizer.AcceptWaveform(data)
        return json.loads(self.recognizer.FinalResult())


def audio_to_text(file, lang="ru"):
    recognizer = MyModelRecognize(file)
    return recognizer.convert_in_text(lang)


if __name__ == '__main__':
    audio_to_text(r"D:\PycharmProjects\Telegram_snapshot\mother.ogg")