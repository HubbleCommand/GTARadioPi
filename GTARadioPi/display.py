import pygame
import os

pygame.font.init()

station_font = pygame.font.Font('assets/fonts/Robot Crush.ttf', 30)
song_font = pygame.font.Font('assets/fonts/Robot Crush.ttf', 18)

def aspect_scale(img, bx, by):
    #Taken from http://www.pygame.org/pcr/transform_scale/
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx,sy))

def display_screen(screen, icon_path, station_name, song_name):
    #screen.fill((255,255,255))
    station_icon = pygame.image.load(icon_path)
    position = (0,0)

    #Resize image keeping aspect ration, and center it
    station_icon = aspect_scale(station_icon, 128, 128)

    if station_icon.get_width() < 128:
        #If not wide enough to fit icon area, we set the position to the center
        position = ((128 - station_icon.get_width()) / 2 , position[1])
    if station_icon.get_height() < 128:
        position = (position[0], (128 - station_icon.get_height()) / 2)

    screen.blit(station_icon, position)
    pygame.display.flip()

def display_station_icon(screen, icon_path):
    station_icon = pygame.image.load(icon_path)
    position = (0,0)

    window_size = pygame.display.get_window_size() #NOTE : returns width, height, SO -> x, y
    icon_size = window_size[0] / 2

    if window_size[1] / 2 < icon_size:
        icon_size = window_size[1] / 2

    #We draw over the previous icon, as GTA IV station icons have transparency
    pygame.draw.rect(screen, (0,0,0), pygame.Rect((0, 0), (icon_size, icon_size)))

    #Resize image keeping aspect ration, and center it
    station_icon = aspect_scale(station_icon, icon_size, icon_size)

    if station_icon.get_width() < icon_size:
        #If not wide enough to fit icon area, we set the position to the center
        position = ((128 - station_icon.get_width()) / 2 , position[1])
    if station_icon.get_height() < icon_size:
        position = (position[0], (icon_size - station_icon.get_height()) / 2)

    screen.blit(station_icon, position)
    #pygame.display.update(pygame.Rect((0, 0),(128, 128)))
    pygame.display.flip()

def display_song_name(screen, song_name):
    global song_font

    #if not isinstance(song_name, bytes) and not isinstance(song_name, str) and not isinstance(song_name, type(u"")):
    if not song_name:
        print("PASSED WRONG TYPE FOR SONG NAME")
        song_name = ""
        #return

    print("Will display track name: ", song_name)
    #img = song_font.render("S : " +song_name, True, (255, 255, 255))
    img = song_font.render("  " + song_name, True, (255, 255, 255))

    window_size = pygame.display.get_window_size()

    #pygame.draw.rect(img, BLUE, rect, 1)
    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((0, (window_size[1] / 4) * 3), ((window_size[0] / 4) * 3, window_size[1])))  #We draw over the previous title
    #screen.blit(img, (0, (window_size[1] / 4) * 3))
    #pygame.display.update(pygame.Rect((144, 0),(256, 50)))

    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, (window_size[1] / 8) * 2), (window_size[0], (window_size[1] / 8) * 3)))  #We draw over the previous title
    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, (window_size[1] / 8) * 3), (window_size[0], (window_size[1] / 8) * 4)))  #We draw over the previous title #This draws over button icons
    pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, window_size[1] * (2/8)), (window_size[0], window_size[1] * (2/8))))  #We draw over the previous title
    screen.blit(img, (window_size[0] / 3, (window_size[1] / 8) * 3))

    pygame.display.flip()

def display_artist_name(screen, artist_name):
    global song_font
    #return
    #We display the song name at a fixed position...
    print("Will display artist: ", artist_name)
    #img = song_font.render("A : " + str(artist_name), True, (255, 255, 255))
    img = song_font.render("  " + str(artist_name), True, (255, 255, 255))

    window_size = pygame.display.get_window_size()
    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, (window_size[1] / 8) * 2), (window_size[0], window_size[1] / 2)))  #We draw over the previous title
    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, (window_size[1] / 8) * 2), (window_size[0], (window_size[1] / 8) * 3)))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, (window_size[1] / 8) * 1), (window_size[0], (window_size[1] / 8) * 2)))
    screen.blit(img, (window_size[0] / 3, (window_size[1] / 8) * 2))

    #pygame.draw.rect(screen, (0,0,0), pygame.Rect((144, 50),(500, 80)))  #We draw over the previous title
    #screen.blit(img, (144, 50))
    pygame.display.flip()

def display_station_name(screen, station_name):
    global station_font
    #We display the station name at a fixed position...
    img = station_font.render(station_name, True, (255, 255, 255))

    window_size = pygame.display.get_window_size()

    pygame.draw.rect(screen, (0,0,0), pygame.Rect((window_size[0] / 3, 0), (window_size[0], window_size[1] / 2)))  #We draw over the previous title
    screen.blit(img, (window_size[0] / 3, 0))
    pygame.display.flip()

def _build_button_icon(screen, index):
    window_size = pygame.display.get_window_size()

    if index == 0:
        icon_path = "assets/button_icons/radio.png"
        x0y0 = (0, window_size[1] / 2)
        x1y1 = (window_size[0] / 3, window_size[1] * (3/4))
    elif index == 1:
        icon_path = "assets/button_icons/track.png"
        x0y0 = (window_size[0] / 3, window_size[1] / 2)
        x1y1 = (window_size[0] * (2/3), window_size[1] * (3/4))
    elif index == 2:
        icon_path = "assets/button_icons/speaker.png"
        x0y0 = (window_size[0] * (2/3), window_size[1] / 2)
        x1y1 = (window_size[0], window_size[1] * (3/4))

    icon = pygame.image.load(icon_path)
    position = x0y0

    window_size = pygame.display.get_window_size() #NOTE : returns width, height, SO -> x, y
    icon_size = window_size[0] / 3

    if window_size[1] / 4 < icon_size:
        icon_size = window_size[1] / 4

    #We draw over the previous icon, as GTA IV station icons have transparency
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x0y0, x1y1))

    #Resize image keeping aspect ration
    icon = aspect_scale(icon, icon_size, icon_size)

    #If not wide enough to fit icon area, we set the position to the center
    if icon.get_width() < icon_size:
        position = ((icon_size - icon.get_width()) / 2 , position[1])
    if icon.get_height() < icon_size:
        position = (position[0], (icon_size - icon.get_height()) / 2)

    screen.blit(icon, position)

def display_button_icons(screen):
    #We display three icons, radio, track, speaker
    _build_button_icon(screen, 0)
    _build_button_icon(screen, 1)
    _build_button_icon(screen, 2)
    
    pygame.display.flip()