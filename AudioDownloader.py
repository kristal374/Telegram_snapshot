import speech_recognition as speech_recognizer
from pydub import AudioSegment
import io


def audio_to_text(file):
    sample_audio = speech_recognizer.AudioFile(convertFromOgg(file))
    recognizer = speech_recognizer.Recognizer()
    with sample_audio as audio_file:
        recognizer.adjust_for_ambient_noise(audio_file)
        audio_content = recognizer.record(audio_file)
    try:
        text = recognizer.recognize_google(audio_content, language='ru')
    except speech_recognizer.UnknownValueError:
        text = 'Текст не распознан...'
    return text


def convertFromOgg(in_path):
    buf = io.BytesIO()
    sound = AudioSegment.from_ogg(in_path)
    sound.export(buf, 'wav')
    return buf
