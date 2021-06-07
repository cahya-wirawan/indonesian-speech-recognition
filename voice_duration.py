from pathlib import Path
import librosa
import datetime
from pydub import AudioSegment

data_dir = "/mnt/mldata/data/ASR/news/id-Wavenet"


def duration(dir, ext):
    path = Path(dir).glob(f'**/*.{ext}')
    duration = 0.0
    counter = 0
    for filename in path:
        if counter % 100 == 0:
            print(counter, datetime.timedelta(seconds=duration), filename)
        counter += 1
        if filename.is_file():
            duration += librosa.get_duration(filename=str(filename))
    # print(f'{duration}s, {duration/60}m, {duration/3600}h')
    return duration


def pduration(dir, ext):
    path = Path(dir).glob(f'**/*.{ext}')
    duration = 0.0
    counter = 0
    for filename in path:
        if counter % 100 == 0:
            print(counter, datetime.timedelta(seconds=duration/1000), filename)
        counter += 1
        if filename.is_file():
            sound = AudioSegment.from_file(filename, format=ext)
            duration += len(sound)
    # print(f'{duration}s, {duration/60}m, {duration/3600}h')
    return duration/1000


sound_length = duration(data_dir, "ogg")
print(str(datetime.timedelta(seconds=sound_length)))