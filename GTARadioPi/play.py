### Utility methods to play audio ###

from genericpath import isfile
#Now just using pygame as keyboard is hella buggy, and lags other parts of the computer!
from random import randint
import files
import os

def advert(path):
    files.play_file(path + "/ADS/" + str(randint(0,184)) + ".wav")

def newsreel(path):
    files.play_file(path + "/NEWS/" + str(randint(0,176)) + ".wav")

def station_id(path, station_src):
    id_to_play = randint(0, files.count_files(path + station_src + "/ID"))
    files.play_file(path + station_src  + "/ID/ID_" + str(id_to_play) + ".wav")



# Split station play
def advert_intro(root, station_src):
    print("ADV INTRO : " + root + station_src + "/TO/AD")
    id_to_play = randint(1, files.count_files(root + station_src + "/TO/AD") - 1)
    files.play_file(root + station_src + "/TO/AD/TAD_" + str(id_to_play) + ".wav")

def newsreel_intro(root, station_src):
    print("NEWS INTRO : " + root + station_src + "/TO/NEWS")
    id_to_play = randint(1, files.count_files(root + station_src + "/TO/NEWS") - 1)
    files.play_file(root + station_src + "/TO/NEWS/TNEW_" + str(id_to_play) + ".wav")
    
def host_snippet(root, station_src):
    snippet_to_play = randint(0, files.count_files(root + station_src + "/HOST") - 1)
    files.play_file(root + station_src + "/HOST/" + str(snippet_to_play) + ".wav")
    
def track_intro(root, station_src, song):
    #count = len[f for f in os.listdir(path + station_src + "/INTRO") if f]

    #As naming starts @ 1, we check if one even exists
    if not os.path.exists(root + station_src + "/INTRO/" + str(song) + "_" + str(1) + ".wav"):
        return

    local_count = 1

    #count = len([name for name in os.listdir(src) if os.path.isfile(os.path.join(src, name))])
    while os.path.exists(root + station_src + "/INTRO/" + str(song) + "_" + str(local_count - 1) + ".wav"):
        local_count += 1

    intro_to_play = randint(1, local_count)
    files.play_file(root + station_src + "/INTRO/" + str(song) + "_" + str(intro_to_play) + ".wav")