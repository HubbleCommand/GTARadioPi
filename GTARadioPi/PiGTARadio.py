from genericpath import isfile
import pygame
import mutagen
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
#Now just using pygame as keyboard is hella buggy, and lags other parts of the computer!
from random import randint
import os
import time
import pygame_gui #https://pygame-gui.readthedocs.io/en/latest/quick_start.html
import argparse


#Import & setup own shit
import buttons
import display
import volume
import stations
import files
import play
from enum import Enum

stations_dict = stations.stations

pygame.init()
pygame.mixer.init()

### Configurable Variables ###
##############################
#Dimensions of TFT screen on Pi
WIDTH  = 480
HEIGHT = 320

#FOR DEPLOYED VERSION, use
#SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

PATH = "E:/audio"

##############################

PATH_STATIONS = PATH + "/STATIONS/"

##############################

#This shouldn't be used...
selected_station = randint(0, len(stations_dict) - 1) #6
selected_station = 22

#Split Station specific
#TODO this should be in dict...
introducing_song = False
intermission = True
intermission_counter = 3
song_countdown = 1
song_id = 0
news = False

def play_split_station(station_data):
    global introducing_song, intermission, intermission_counter, song_countdown, song_id, news
    print(station_data["name"])

    if introducing_song:
        display.display_song_name(SCREEN, files.get_track_name(PATH_STATIONS + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
        display.display_artist_name(SCREEN, files.get_track_artist(PATH_STATIONS + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
        introducing_song = False
        song_countdown -= 1
        files.play_file(PATH_STATIONS + station_data["src"] + "/SONGS/" + str(song_id) + ".wav")

    elif intermission:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if intermission_counter <= 0:
            intermission = False
            play.station_id(PATH_STATIONS, station_data["src"])
        else:
            intermission_counter -= 1
            if news:
                play.newsreel(PATH)
            else:
                play.advert(PATH)
    else:
        print("ELSE")
        if song_countdown <= 0:
            display.display_song_name(SCREEN, "")
            display.display_artist_name(SCREEN, "")
            intermission = True

            if(randint(0, 6) > 2):
                news = False
                intermission_counter = randint(3, 6)
                play.advert_intro(PATH_STATIONS, station_data["src"])
            else:
                news = True
                intermission_counter = randint(1, 4)
                play.newsreel_intro(PATH_STATIONS, station_data["src"])
        else:
            song_countdown = randint(3,8)

            song_id = randint(0, files.count_files(PATH_STATIONS + station_data["src"] + "/SONGS") - 1)

            display.display_song_name(SCREEN, files.get_track_name(PATH_STATIONS + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))
            display.display_artist_name(SCREEN, files.get_track_artist(PATH_STATIONS + station_data["src"] + "/SONGS/" + str(song_id) + ".wav"))

            introducing_song = True

            if randint(0, 10) > 7:
                play.host_snippet(PATH_STATIONS, station_data["src"])
            else:
                play.track_intro(PATH_STATIONS, station_data["src"], song_id)

def play_talkshow_station(station_data):
    global intermission, intermission_counter
    print(station_data["name"])

    if intermission:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if intermission_counter <= 0:
            intermission = False
            play.station_id(station_data["src"])
        else:
            intermission_counter -= 1
            if randint(0, 2) > 1:
                play.newsreel()
            else:
                play.advert()
    else:
        intermission_counter = randint(3, 6)
        intermission = True
        
        show_count = files.count_files(PATH_STATIONS + station_data["src"] + "/MONO")
        show_selected = randint(0, show_count - 1)

        display.display_song_name(SCREEN, files.get_track_name(PATH_STATIONS + station_data["src"] + "/MONO/" + str(show_selected) + ".wav"))
        display.display_artist_name(SCREEN, "")
        files.play_file(PATH_STATIONS + station_data["src"] + "/MONO/" + str(show_selected) + ".wav")

def play_unsplit_station(station_data):
    global stations_dict
    start_at = randint(0, int(files.get_track_duration(PATH_STATIONS + stations_dict[selected_station]["src"] + "/SRC.ogg")))

    stations_dict[selected_station]["pos"] = start_at
    stations_dict[selected_station]["timestamp_seek_s"] = time.time()

    display.display_song_name(SCREEN, "")
    display.display_artist_name(SCREEN, "")
    pygame.mixer.music.load(PATH_STATIONS + station_data["src"] + "/SRC.ogg")
    pygame.mixer.music.play(start = start_at)

#Main loop stuff
def play_station():
    current_station = stations_dict[selected_station]
    
    if current_station["type"] == 0:
        play_unsplit_station(current_station)
    elif current_station["type"] == 1:
        play_split_station(current_station)
    elif current_station["type"] == 2:
        play_talkshow_station(current_station)

def stop():
    pygame.mixer.music.stop()

def switch_station(up):
    global selected_station, introducing_song, intermission, song_countdown
    stop()
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

    print("Selected Station : " + str(selected_station))

    display.display_station_name(SCREEN, stations_dict[selected_station]["name"])
    display.display_station_icon(SCREEN, PATH_STATIONS + stations_dict[selected_station]["src"] + "/icon.png")
    
    play_station()

def change_song(next):
    global intermission, song_id, stations_dict

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

        track_duration_seconds = files.get_track_duration(PATH_STATIONS + stations_dict[selected_station]["src"] + "/SRC.ogg")

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

        song_count = files.count_files(PATH_STATIONS + station_data["src"] + track_path) - 1

        if next:
            song_id += 1
        else:
            song_id -= 1

        if song_id > song_count:
            song_id = 0
        elif song_id < 0:
            song_id = song_count

        display.display_song_name(SCREEN, files.get_track_name(PATH_STATIONS + station_data["src"] + track_path +"/" + str(song_id) + ".wav"))

        if stations_dict[selected_station]["type"] == 2:
            display.display_artist_name(SCREEN, "")
        else:
            display.display_artist_name(SCREEN, files.get_track_artist(PATH_STATIONS + station_data["src"] + track_path + "/" + str(song_id) + ".wav"))

        files.play_file(PATH_STATIONS + station_data["src"] + track_path + "/" + str(song_id) + ".wav")

#These global vars are fine, they are immutable
#Button setup
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
window_size = pygame.display.get_window_size()

vol_up_button = buttons.build_volume_up_button(manager, window_size)
vol_down_button = buttons.build_volume_down_button(manager, window_size)
station_up_button = buttons.build_station_up_button(manager, window_size)
station_down_button = buttons.build_station_down_button(manager, window_size)
track_up_button = buttons.build_track_up_button(manager, window_size)
track_down_button = buttons.build_track_down_button(manager, window_size)

seeker = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((window_size[0] * (2/3), window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
    start_value=0,
    value_range=(0,10),
    manager=manager)
seeker.hide()

def main():
    print("MAIN")
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="directory with the station audio", type=str)
    parser.add_argument("--width", help="screen width in pixels", type=int)
    parser.add_argument("--height", help="screen height in pixels", type=int)
    args = parser.parse_args()
    parser.parse_args()

    if args.width and not args.height or args.height and not args.width:
        parser.error("When defining screen size, both width and height are required")
    
    files.load_path(PATH)

    display.display_station_name(SCREEN, stations_dict[selected_station]["name"])
    display.display_station_icon(SCREEN, PATH_STATIONS + stations_dict[selected_station]["src"] + "/icon.png")

    is_running = True
    while is_running:
        if not pygame.mixer.music.get_busy():
            play_station()

        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == track_up_button:
                    change_song(True)
                if event.ui_element == track_down_button:
                    change_song(False)

                if event.ui_element == station_up_button:
                    switch_station(True)
                if event.ui_element == station_down_button:
                    switch_station(False)

                if event.ui_element == vol_up_button:
                    volume.increase()
                if event.ui_element == vol_down_button:
                    volume.decrease()
            
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                pass
                #TODO change seek position
                #issue is getting current playing audio length (exists in mixer.Sound, not mixer.Music), cannot get from pygame
                #so would need to get it every time the audio changes
                #pygame.mixer.music.set_pos(event.value)
            
            manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    print("Key N has been pressed")
                    switch_station(False)
                if event.key == pygame.K_p:
                    print("Key P has been pressed")
                    switch_station(True)
                if event.key == pygame.K_l:
                    print("Key L has been pressed next song")
                    change_song(True)
                if event.key == pygame.K_k:
                    print("Key K has been pressed prev song")
                    change_song(False)

        manager.update(time_delta)
        manager.draw_ui(SCREEN)
        pygame.display.update()

if __name__ == "__main__":
    main()
