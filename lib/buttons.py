import pygame
import pygame_gui

#Note unlike pygame, pygame_gui rects are not (top-left, bottom-right) corners, but are (top-left, dimensions)
def build_volume_up_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] * (2/3), window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='VOL ++',
                                             manager=manager)
def build_volume_down_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] * (2/3), window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='VOL --',
                                             manager=manager)

def build_station_up_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='STATION ++',
                                             manager=manager)
def build_station_down_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='STATION --',
                                             manager=manager)

def build_track_up_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] / 3, window_size[1] / 2), (window_size[0] / 3, window_size[1] / 4)),
                                             text='TRACK ++',
                                             manager=manager)
def build_track_down_button(manager, window_size):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_size[0] / 3, window_size[1] * (3/4)), (window_size[0] / 3, window_size[1] / 4)),
                                             text='TRACK --',
                                             manager=manager)
