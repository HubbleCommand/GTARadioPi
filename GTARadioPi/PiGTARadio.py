import pygame
import mutagen
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
#Now just using pygame as keyboard is hella buggy, and lags other parts of the computer!
from random import randint
import os
import time
import pygame_gui

#Import & setup own shit
import display
import volume
import stations
stations_dict = stations.stations

pygame.init()
pygame.mixer.init()

#Dimensions of TFT screen on Pi
WIDTH  = 480
HEIGHT = 320

#FOR DEPLOYED VERSION, use
#SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

print(pygame.display.get_window_size())

audio = WAVE('D:/GTA SAVE/RAIN.wav')
print(audio.tags)

print("ARTIST")
print(audio.tags["TPE1"])
print("TITLE")
print(audio.tags["TIT2"])
print("DURATION")
print(audio.info.length)


path = "D:/GTA SAVE/"
path_icons = "D:/GTA Stations Icons/"
selected_station = randint(0, len(stations_dict) - 1) #6
selected_station = 22

display.display_station_name(SCREEN, stations_dict[selected_station]["name"])
display.display_station_icon(SCREEN, path_icons + stations_dict[selected_station]["icon"])

#Unlike the Arduino version, we are going purely functional here!
#Except we are using quite a few global variables, which isn't great...

def _switch_station(up):
    global selected_station
    global stations_dict
    stop()
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path, SCREEN
    intermission = False
    introducing_song = False
    song_countdown = 5

    if up: 
        selected_station += 1
    else: 
        selected_station -= 1

    if selected_station < 0:
        selected_station = len(stations_dict) - 1
    elif selected_station > len(stations_dict) - 1:
        selected_station = 0

    print("Selected Station")
    print(selected_station)

    display.display_station_name(SCREEN, stations_dict[selected_station]["name"])
    display.display_station_icon(SCREEN, path_icons + stations_dict[selected_station]["icon"])
    
    play()

def play_file(path):
    #Anytime we want to play a file, we unload the previously loaded file
    pygame.mixer.music.unload()

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def play_advert():
    advert_number = randint(0,184)
    pygame.mixer.music.load(path + "/ADS/" + str(advert_number) + ".wav")
    pygame.mixer.music.play()

def play_newsreel():
    reel_number = randint(0,176)
    pygame.mixer.music.load(path + "/NEWS/" + str(reel_number) + ".wav")
    pygame.mixer.music.play()

def count_files(src):
    #count = len([name for name in os.listdir(src) if os.path.isfile(name)])
    count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    print("COUNT")
    print(count)
    return count

def get_track_name(path):
    audio = WAVE(path)
    print("Track Name")
    print(audio.tags["TIT2"])
    print(type(audio.tags["TIT2"]))
    print(str(audio.tags["TIT2"]))
    #mutagen.id3.TIT2.
    return str(audio.tags["TIT2"])

    #print(audio.tags)

    #print("ARTIST")
    #print(audio.tags["TPE1"])
    #print("TITLE")
    #print(audio.tags["TIT2"])

def get_track_artist(path):
    audio = WAVE(path)
    return str(audio.tags["TPE1"])

def play_station_id(station_src):
    id_to_play = randint(0, count_files(path + station_src + "/ID"))
    pygame.mixer.music.load(path + station_src  + "/ID/ID_" + str(id_to_play) + ".wav")
    pygame.mixer.music.play()

#Talkshow station specific
def play_talkshow_station(station_data):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    print(station_data["name"])

    if intermission:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if intermission_counter <= 0:
            intermission = False
            play_station_id(station_data["src"])
        else:
            intermission_counter -= 1
            if randint(0, 2) > 1:
                play_newsreel()
            else:
                play_advert()
    else:
        intermission_counter = randint(3, 6)
        intermission = True
        
        show_count = count_files(path + station_data["src"] + "/MONO")
        show_selected = randint(0, show_count - 1)

        display.display_song_name(SCREEN, get_track_name(path + station_data["src"] + "/MONO/" + str(show_selected) + ".wav"))
        display.display_artist_name(SCREEN, "")
        play_file(path + station_data["src"] + "/MONO/" + str(show_selected) + ".wav")

#Split Station specific
#TODO this should be in dict...
introducing_song = False;
intermission = False;
intermission_counter = 0;
song_countdown = 5;
song_id = 0;
news = False;

def play_advert_intro(station_src):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    print("ADV INTRO")
    print(path + station_src + "/TO/AD")
    id_to_play = randint(1, count_files(path + station_src + "/TO/AD") - 1)
    play_file(path + station_src + "/TO/AD/TAD_" + str(id_to_play) + ".wav")

def play_newsreel_intro(station_src):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    print("NEWS INTRO")
    print(path + station_src + "/TO/NEWS")
    id_to_play = randint(1, count_files(path + station_src + "/TO/NEWS") - 1)
    play_file(path + station_src + "/TO/NEWS/TNEW_" + str(id_to_play) + ".wav")

def play_host_snippet(station_src):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    snippet_to_play = randint(0, count_files(path + station_src + "/HOST") - 1)
    play_file(path + station_src + "/HOST/" + str(snippet_to_play) + ".wav")

def play_track_intro(station_src, song):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    #count = len[f for f in os.listdir(path + station_src + "/INTRO") if f]

    #As naming starts @ 1, we check if one even exists
    if not os.path.exists(path + station_src + "/INTRO/" + str(song) + "_" + str(1) + ".wav"):
        return

    local_count = 1

    #count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    while os.path.exists(path + station_src + "/INTRO/" + str(song) + "_" + str(local_count - 1) + ".wav"):
        local_count += 1

    intro_to_play = randint(1, local_count)
    play_file(path + station_src + "/INTRO/" + str(song) + "_" + str(intro_to_play) + ".wav")

def play_split_station(station_data):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path
    print(station_data["name"])

    if introducing_song:
        display.display_song_name(SCREEN, get_track_name(path + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
        display.display_artist_name(SCREEN, get_track_artist(path + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
        introducing_song = False
        song_countdown -= 1
        play_file(path + station_data["src"] + "/SONGS/" + str(song_id) + ".wav")

    elif intermission:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if intermission_counter <= 0:
            intermission = False
            play_station_id(station_data["src"])
        else:
            intermission_counter -= 1
            if news:
                play_newsreel();
            else:
                play_advert();
    else:
        print("ELSE")
        if song_countdown <= 0:
            display.display_song_name(SCREEN, "")
            display.display_artist_name(SCREEN, "")
            intermission = True

            if(randint(0, 6) > 2):
                news = False
                intermission_counter = randint(3, 6)
                play_advert_intro(station_data["src"])
            else:
                news = True
                intermission_counter = randint(1, 4)
                play_newsreel_intro(station_data["src"])
        else:
            song_countdown = randint(3,8)

            selected_song = randint(0, count_files(path + station_data["src"] + "/SONGS") - 1)

            song_id = selected_song

            display.display_song_name(SCREEN, get_track_name(path + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
            display.display_artist_name(SCREEN, get_track_artist(path + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))

            introducing_song = True

            if randint(0, 10) > 7:
                play_host_snippet(station_data["src"])
            else:
                play_track_intro(station_data["src"], song_id)

## Unsplit specific
def unsplit_get_duration(path):
    track_info = OggVorbis(path)
    return track_info.info.length

def play_unsplit_station(station_data):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path, stations_dict, selected_station
    start_at = randint(0, int(unsplit_get_duration(path + stations_dict[selected_station]["src"] + "/SRC.ogg")))

    stations_dict[selected_station]["pos"] = start_at
    stations_dict[selected_station]["timestamp_seek_s"] = time.time()

    display.display_song_name(SCREEN, "")
    display.display_artist_name(SCREEN, "")
    print(station_data["name"])
    pygame.mixer.music.load(path + station_data["src"] + "/SRC.ogg")
    pygame.mixer.music.play(start = start_at)

#Main loop stuff
def play():
    global path, path_icons, stations_dict, selected_station, SCREEN, song_name

    #display.display_screen(
    #    SCREEN, 
    #    path_icons + stations_dict[selected_station]["icon"],
    #    stations_dict[selected_station]["name"],
    #    song_name
    #)

#    pygame.mixer.music.unload()

    current_station = stations_dict[selected_station]
    
    if current_station["type"] == 0:
        play_unsplit_station(current_station)
    elif current_station["type"] == 1:
        play_split_station(current_station)
    elif current_station["type"] == 2:
        play_talkshow_station(current_station)

def change_song(next):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news, path, stations_dict, selected_station

    if stations_dict[selected_station]["type"] == 0:
        if not "pos" in stations_dict[selected_station]:
            stations_dict[selected_station]["pos"] = 0
        if not "timestamp_seek_s" in stations_dict[selected_station]:
            stations_dict[selected_station]["timestamp_seek_s"] = time.time()

        print("UNSPLIT, SETTING POS")

        #get_pos returns how long it has been playing, not the position 
        #We find how much time has elapsed since we started playing the unsplit station, adding the last set position / seek position of the track
        current_pos = (time.time() - stations_dict[selected_station]["timestamp_seek_s"]) + stations_dict[selected_station]["pos"]

        if next:
            new_pos = current_pos + 60
        else:
            new_pos = current_pos - 60

        track_duration_seconds = unsplit_get_duration(path + stations_dict[selected_station]["src"] + "/SRC.ogg")

        print("Current position : " + str(current_pos))
        print("New Position : " + str(new_pos))
        print("TRACK LENGTH : " + str(track_duration_seconds))

        while new_pos > track_duration_seconds:
            new_pos -= track_duration_seconds

        while new_pos < 0:
            new_pos += track_duration_seconds

        stations_dict[selected_station]["pos"] = new_pos
        pygame.mixer.music.set_pos(new_pos)

    elif stations_dict[selected_station]["type"] == 1 or stations_dict[selected_station]["type"] == 2:
        print("CHANING TYPE 1 and 2")
        stop()

        track_path = "/SONGS"
        if stations_dict[selected_station]["type"] == 2:
            track_path = "/MONO"

        station_data = stations_dict[selected_station]
        intermission = False

        song_count = count_files(path + station_data["src"] + track_path) - 1

        if next:
            song_id += 1
        else:
            song_id -= 1

        if song_id > song_count:
            song_id = 0
        elif song_id < 0:
            song_id = song_count

        display.display_song_name(SCREEN, get_track_name(path + station_data["src"] + track_path +"/" + str(song_id) + ".wav"))

        if stations_dict[selected_station]["type"] == 2:
            display.display_artist_name(SCREEN, "")
        else:
            display.display_artist_name(SCREEN, get_track_artist(path + station_data["src"] + track_path + "/" + str(song_id) + ".wav"))

        play_file(path + station_data["src"] + track_path + "/" + str(song_id) + ".wav")

def stop():
    pygame.mixer.music.stop()

#Button setup
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

window_size = pygame.display.get_window_size()

#Note unlike pygame, pygame_gui rects are not (top-left, bottom-right) corners, but are (top-left, dimensions)
vol_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] * (2/3), window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='VOL ++',
                                             manager=manager)
vol_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] * (2/3), window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='VOL --',
                                             manager=manager)

station_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='STATION ++',
                                             manager=manager)
station_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='STATION --',
                                             manager=manager)

track_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] / 3, window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='TRACK ++',
                                             manager=manager)
track_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] / 3, window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='TRACK --',
                                             manager=manager)

is_running = True
while is_running:
    if not pygame.mixer.music.get_busy():
        play()

    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             is_running = False
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #if event.ui_element == hello_button:
            #    print('Hello World!')
            if event.ui_element == track_up_button:
                change_song(True)
            if event.ui_element == track_down_button:
                change_song(False)

            if event.ui_element == station_up_button:
                _switch_station(True)
            if event.ui_element == station_down_button:
                _switch_station(False)

            if event.ui_element == vol_up_button:
                volume.increase()
            if event.ui_element == vol_down_button:
                volume.decrease()

        
        manager.process_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                print("Key N has been pressed")
                _switch_station(False)
            if event.key == pygame.K_p:
                print("Key P has been pressed")
                _switch_station(True)
            if event.key == pygame.K_l:
                print("Key L has been pressed next song")
                change_song(True)
            if event.key == pygame.K_k:
                print("Key K has been pressed prev sont")
                change_song(False)

    manager.update(time_delta)
    manager.draw_ui(SCREEN)
    pygame.display.update()
