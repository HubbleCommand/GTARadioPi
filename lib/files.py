import os
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
import pygame
import random

def count_files(src) -> int:
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

def get_track_name(path) -> str:
    audio = WAVE(path)
    print("Track Name: ", audio.tags["TIT2"], " | ", str(audio.tags["TIT2"]))
    return str(audio.tags["TIT2"])

def get_track_artist(path) -> str:
    audio = WAVE(path)
    return str(audio.tags["TPE1"])

def get_track_duration(path):
    track_info = get_track_object(path)
    return track_info.info.length

def read_station_name(path: str) -> str:
    if not os.path.exists(os.path.join(path, "name.txt")):
        return ""
    file = open(os.path.join(path, "name.txt"), 'r')
    name = file.read()
    file.close()
    return name

def determine_station_type(path: str) -> int:
    #type is 0,1,2 (unsplit, split, talkshow)
    if os.path.exists(os.path.join(path, "SRC.wav")):
        return 0
    
    if os.path.exists(os.path.join(path, "SONGS")):
        return 1
    
    if os.path.exists(os.path.join(path, "MONO")):
        return 2
    
    return -1

def load_path(path: str) -> list:
    if not os.path.exists(path) or not os.path.exists(os.path.join(path, "STATIONS")):
        print("BAD")
        return {}
    
    dirs = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]
    print(dirs)

    ret = []
    stations_dir = os.path.join(path, "STATIONS")
    stations = [dir for dir in os.listdir(stations_dir) if os.path.isdir(os.path.join(stations_dir, dir))]
    for station in stations:
        path_abs = os.path.join(path, "STATIONS", station)
        
        name    = read_station_name(path_abs)
        type    = determine_station_type(path_abs)

        #Initialize various state members based on type
        if type == 0:
            #State will be initialized during playback
            state = {}
        elif type == 1:
            state = {
                #"intermission": bool(random.getrandbits(1)),
                "intermission": True,
                "news":  bool(random.getrandbits(1)),
                "intermission_cnt": 3,
                "track_countdown": 1, ##only type 1 ?
                
                "introducing_track": False,
                "track_id": 1,
            }
        elif type == 2: #pretty sure it's the same? just some slight variations in number of ads etc
            state = {
                "intermission": bool(random.getrandbits(1)),
                "news":  bool(random.getrandbits(1)),
                "intermission_cnt": 5,
                
                "track_id": 1,
            }

        ret.append({
            "type": type,
            "name": name,
            "src":  path_abs,
            "state": state
        })

    return ret