from pydub import AudioSegment
import io


def convert_from_ogg(in_path):
    buf = io.BytesIO()
    sound = AudioSegment.from_ogg(in_path)
    sound = sound.set_channels(1)
    sound.export(buf, 'wav')
    return buf
