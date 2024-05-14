from random import randint
import time
import pygame
import pygame_gui #https://pygame-gui.readthedocs.io/en/latest/quick_start.html
import argparse

import lib.buttons as buttons
import lib.display as display
import lib.volume as volume
import lib.files as files
import lib.play as play
from lib.state import current_station, current_station_state, root_dir, make_default_state

pygame.init()
pygame.mixer.init()

##############################
PATH = ""
WIDTH  = 480
HEIGHT = 320
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #For fullscreen, add ´, pygame.FULLSCREEN)´
##############################

def play_split_station(state: dict) -> dict:
    if current_station_state(state)["introducing_track"]:
        display.display_song_name(SCREEN, files.get_track_name(current_station(state)["src"] + "/SONGS/" + str(current_station_state(state)["track_id"]) + ".wav"))
        display.display_artist_name(SCREEN, files.get_track_artist(current_station(state)["src"] + "/SONGS/" + str(current_station_state(state)["track_id"]) + ".wav"))
        state["stations"][state["current"]]["state"]["introducing_track"] = False
        state["stations"][state["current"]]["state"]["track_countdown"] -= 1
        files.play_file(current_station(state)["src"] + "/SONGS/" + str(current_station(state)["state"]["track_id"]) + ".wav")
    elif current_station_state(state)["intermission"]:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if state["stations"][state["current"]]["state"]["intermission_cnt"] <= 0:
            state["stations"][state["current"]]["state"]["intermission"] = False
            play.station_id(current_station(state)["src"])
        else:
            state["stations"][state["current"]]["state"]["intermission_cnt"] -= 1
            if state["stations"][state["current"]]["state"]["news"]:
                play.newsreel(root_dir(state))
            else:
                play.advert(root_dir(state))
    else:
        if current_station_state(state)["track_countdown"] <= 0:
            display.display_song_name(SCREEN, "")
            display.display_artist_name(SCREEN, "")
            state["stations"][state["current"]]["state"]["intermission"] = True
            state["stations"][state["current"]]["state"]["track_countdown"] = randint(3,8) #prep next programming
            if(randint(0, 6) > 2):
                state["stations"][state["current"]]["state"]["news"] = False
                state["stations"][state["current"]]["state"]["intermission_cnt"] = randint(3, 6)
                play.advert_intro(current_station(state)["src"])
            else:
                state["stations"][state["current"]]["state"]["news"] = True
                state["stations"][state["current"]]["state"]["intermission_cnt"] = randint(1, 4)
                play.newsreel_intro(current_station(state)["src"])
        else:
            #state["stations"][state["current"]]["state"]["track_countdown"] = randint(3,8)
            print("Track countdown: ", state["stations"][state["current"]]["state"]["track_countdown"])
            state["stations"][state["current"]]["state"]["track_id"] = randint(0, files.count_files(current_station(state)["src"] + "/SONGS") - 1)

            display.display_song_name(SCREEN, files.get_track_name(current_station(state)["src"] + "/SONGS/" + str(current_station_state(state)["track_id"]) + ".wav"))
            display.display_artist_name(SCREEN, files.get_track_artist(current_station(state)["src"] + "/SONGS/" + str(current_station_state(state)["track_id"]) + ".wav"))

            state["stations"][state["current"]]["state"]["introducing_track"] = True

            if randint(0, 10) > 7:
                play.host_snippet(current_station(state)["src"])
            else:
                play.track_intro(current_station(state)["src"], current_station_state(state)["track_id"])
    return state

def play_talkshow_station(state: dict) -> dict:
    print(current_station(state)["name"])

    if current_station_state(state)["intermission"]:
        display.display_song_name(SCREEN, "")
        display.display_artist_name(SCREEN, "")
        if current_station_state(state)["intermission_cnt"] <= 0:
            state["stations"][state["current"]]["state"]["intermission"] = False
            play.station_id(current_station(state)["src"])
        else:
            state["stations"][state["current"]]["state"]["intermission_cnt"] -= 1
            if randint(0, 2) > 1:
                play.newsreel(root_dir(state))
            else:
                play.advert(root_dir(state))
    else:
        state["stations"][state["current"]]["state"]["intermission_cnt"] = randint(3, 6)
        state["stations"][state["current"]]["state"]["intermission"] = True
        
        show_count = files.count_files(current_station(state)["src"] + "/MONO")
        state["stations"][state["current"]]["state"]["track_id"] = randint(0, show_count - 1)

        display.display_song_name(SCREEN, files.get_track_name(current_station(state)["src"] + "/MONO/" + str(current_station_state(state)["track_id"]) + ".wav"))
        display.display_artist_name(SCREEN, "")
        files.play_file(current_station(state)["src"] + "/MONO/" + str(current_station_state(state)["track_id"]) + ".wav")
    return state

def play_unsplit_station(state: dict) -> dict:
    start_at = randint(0, int(files.get_track_duration(current_station(state)["src"] + "/SRC.ogg")))

    state["stations"][state["current"]]["state"]["pos"] = start_at
    state["stations"][state["current"]]["state"]["timestamp_seek_s"] = time.time()

    display.display_song_name(SCREEN, "")
    display.display_artist_name(SCREEN, "")
    pygame.mixer.music.load(current_station(state)["src"] + "/SRC.ogg")
    pygame.mixer.music.play(start = start_at)
    return state

def play_station(state: dict) -> dict:
    if current_station(state)["type"] == 0:
        return play_unsplit_station(state)
    elif current_station(state)["type"] == 1:
        return play_split_station(state)
    elif current_station(state)["type"] == 2:
        return play_talkshow_station(state)
    print("INVALID FALLTHROUGH")
    pygame.quit()
    return state

def stop():
    pygame.mixer.music.stop()

def switch_station(state: dict, up: bool) -> dict:
    stop()

    #TODO update state based on when last opened...

    if up:
        state["current"] += 1
    else: 
        state["current"] -= 1

    if state["current"] < 0:
        state["current"] = len(state["stations"]) - 1
    elif state["current"] > len(state["stations"]) - 1:
        state["current"] = 0

    print("Selected Station : " + str(state["current"]))
    display.display_station_name(SCREEN, current_station(state)["name"])
    display.display_station_icon(SCREEN, current_station(state)["src"] + "/icon.png")
    
    return play_station(state)

def change_song(state: dict, next: bool) -> dict:
    if current_station(state)["type"] == 0:
        if not "pos" in current_station(state):
            state["stations"][state["current"]]["pos"] = 0
        if not "timestamp_seek_s" in current_station(state):
            state["stations"][state["current"]]["timestamp_seek_s"] = time.time()

        print("UNSPLIT, SETTING POS")

        #get_pos returns how long it has been playing, not the position 
        #We find how much time has elapsed since we started playing the unsplit station, adding the last set position / seek position of the track
        current_pos = (time.time() - current_station(state)["timestamp_seek_s"]) + current_station(state)["pos"]

        if next:
            new_pos = current_pos + 60
        else:
            new_pos = current_pos - 60

        track_duration_seconds = files.get_track_duration(current_station(state)["src"] + "/SRC.ogg")

        print("Current position : " + str(current_pos))
        print("New Position : " + str(new_pos))
        print("TRACK LENGTH : " + str(track_duration_seconds))

        while new_pos > track_duration_seconds:
            new_pos -= track_duration_seconds

        while new_pos < 0:
            new_pos += track_duration_seconds

        state["stations"][state["current"]]["pos"] = new_pos
        pygame.mixer.music.set_pos(new_pos)

    elif current_station(state)["type"] == 1 or current_station(state)["type"] == 2:
        print("CHANING TYPE 1 and 2")
        stop()

        state["stations"][state["current"]]["intermission"] = False

        track_path = "/SONGS"
        if current_station(state)["type"] == 2:
            track_path = "/MONO"

        song_count = files.count_files(current_station(state)["src"] + track_path) - 1

        song_id = current_station_state(state)["track_id"]
        if next:
            song_id += 1
        else:
            song_id -= 1

        if song_id > song_count:
            song_id = 0
        elif song_id < 0:
            song_id = song_count
        state["stations"][state["current"]]["state"]["track_id"] = song_id

        display.display_song_name(SCREEN, files.get_track_name(current_station(state)["src"] + track_path +"/" + str(song_id) + ".wav"))

        if current_station(state)["type"] == 2:
            display.display_artist_name(SCREEN, "")
        else:
            display.display_artist_name(SCREEN, files.get_track_artist(current_station(state)["src"] + track_path + "/" + str(song_id) + ".wav"))

        files.play_file(current_station(state)["src"] + track_path + "/" + str(song_id) + ".wav")
    return state

#Button setup
CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
WNDW_SIZE = pygame.display.get_window_size()

BTN_VOL_UP = buttons.build_volume_up_button(MANAGER, WNDW_SIZE)
BTN_VOL_DWN = buttons.build_volume_down_button(MANAGER, WNDW_SIZE)
BTN_STATION_UP = buttons.build_station_up_button(MANAGER, WNDW_SIZE)
BTN_STATION_DWN = buttons.build_station_down_button(MANAGER, WNDW_SIZE)
BTN_TRACK_UP = buttons.build_track_up_button(MANAGER, WNDW_SIZE)
BTN_TRACK_DWN = buttons.build_track_down_button(MANAGER, WNDW_SIZE)

SEEKER = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WNDW_SIZE[0] * (2/3), WNDW_SIZE[1] / 2), (WNDW_SIZE[0] / 3, WNDW_SIZE[1] / 4)),
    start_value=0,
    value_range=(0,10),
    manager=MANAGER)
SEEKER.hide()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="directory with the station audio", type=str)
    parser.add_argument("--width", help="screen width in pixels", type=int)
    parser.add_argument("--height", help="screen height in pixels", type=int)
    args = parser.parse_args()
    parser.parse_args()

    if args.width and not args.height or args.height and not args.width:
        parser.error("When defining screen size, both width and height are required")

    if not args.directory and not PATH:
        print("Directory required")
        return
    if args.directory:
        PATH = args.directory
    
    state = make_default_state(PATH)
    state = switch_station(state, True)

    is_running = True
    while is_running:
        if not pygame.mixer.music.get_busy():
            state = play_station(state)

        time_delta = CLOCK.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == BTN_TRACK_UP:
                    state = change_song(state, True)
                if event.ui_element == BTN_TRACK_DWN:
                    state = change_song(state, False)

                if event.ui_element == BTN_STATION_UP:
                    state= switch_station(state, True)
                if event.ui_element == BTN_STATION_DWN:
                    state = switch_station(state, False)

                if event.ui_element == BTN_VOL_UP:
                    volume.increase()
                if event.ui_element == BTN_VOL_DWN:
                    volume.decrease()
            
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                pass
                #TODO change seek position
                #issue is getting current playing audio length (exists in mixer.Sound, not mixer.Music), cannot get from pygame
                #so would need to get it every time the audio changes
                #pygame.mixer.music.set_pos(event.value)
            
            MANAGER.process_events(event)

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

        MANAGER.update(time_delta)
        MANAGER.draw_ui(SCREEN)
        pygame.display.update()

if __name__ == "__main__":
    main()
