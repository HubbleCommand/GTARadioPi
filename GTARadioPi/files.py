import os
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis

def count_files(src):
    count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    print("COUNT")
    print(count)
    return count

def get_track_object(path):
    extension = os.path.splitext(path)[1]
    print("EXTENSION")
    print(extension)
    if extension == ".wav":
        print("Returning wav")
        return WAVE(path)
    elif extension == ".ogg":
        print("Returning ogg")
        return OggVorbis(path)

def get_track_name(path):
    audio = WAVE(path)
    print("Track Name")
    print(audio.tags["TIT2"])
    print(str(audio.tags["TIT2"]))
    return str(audio.tags["TIT2"])

def get_track_artist(path):
    audio = WAVE(path)
    return str(audio.tags["TPE1"])

def get_track_duration(path):
    track_info = get_track_object(path)
    return track_info.info.length

def count_files(src):
    count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    print("COUNT")
    print(count)
    return count
