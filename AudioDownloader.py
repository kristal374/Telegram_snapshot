import speech_recognition
from pydub import AudioSegment
import io


def audio_to_text(file):
    sample_audio = speech_recognition.AudioFile(convertFromOgg(file))
    recognizer = speech_recognition.Recognizer()
    with sample_audio as audio_file:
        recognizer.adjust_for_ambient_noise(audio_file)
        audio_content = recognizer.record(audio_file)
    try:
        text = recognizer.recognize_google(audio_content, language='ru')
    except speech_recognition.UnknownValueError:
        text = 'Текст не распознан'
    except speech_recognition.RequestError:
        text = 'Ошибка во время преобразования'
    return text


def convertFromOgg(in_path):
    buf = io.BytesIO()
    sound = AudioSegment.from_ogg(in_path)
    sound.export(buf, 'wav')
    return buf
