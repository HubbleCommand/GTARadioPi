import os
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
import pygame
from enum import Enum
import json

def count_files(src):
    count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    print("count: ", count)
    return count

def play_file(path):
    #Anytime we want to play a file, we unload the previously loaded file
    pygame.mixer.music.unload()

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def get_track_object(path):
    extension = os.path.splitext(path)[1]
    print("ext: ", extension)
    if extension == ".wav":
        print("Returning wav")
        return WAVE(path)
    elif extension == ".ogg":
        print("Returning ogg")
        return OggVorbis(path)

def get_track_name(path):
    audio = WAVE(path)
    print("Track Name: ", audio.tags["TIT2"], " | ", str(audio.tags["TIT2"]))
    return str(audio.tags["TIT2"])

def get_track_artist(path):
    audio = WAVE(path)
    return str(audio.tags["TPE1"])

def get_track_duration(path):
    track_info = get_track_object(path)
    return track_info.info.length

def read_station_name(path: str) -> str:
    if not os.path.exists(path + "name.txt"):
        return ""
    file = open(path + "name.txt", 'r')
    name = file.read()
    file.close()
    return name

class Station(Enum):
    UNSPLIT = 0
    SPLIT = 1
    TALKSHOW = 2
#Station = Enum('Station', ['UNSPLIT', 'SPLIT', 'TALKSHOW'])
def determine_station_type(path: str) -> Station|int:
    #type is 0,1,2 (unsplit, split, talkshow)
    if os.path.exists(path + "SRC.wav"):
        return Station.UNSPLIT
    
    if os.path.exists(path + "SONGS/"):
        return Station.SPLIT
    
    if os.path.exists(path + "MONO/"):
        return Station.TALKSHOW
    
    return -1

def load_path(path: str) -> dict:
    if not os.path.exists(path) or not os.path.exists(os.path.join(path, "STATIONS")):
        print("BAD")
        return {}
    
    dirs = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]
    print(dirs)
    
