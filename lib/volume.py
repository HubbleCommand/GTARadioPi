import pygame
from pynput.keyboard import Key,Controller
keyboard = Controller()

def __change_volume_pygame(increase):
    current_volume = pygame.mixer.music.get_volume()

    if increase:
        current_volume += 0.1
    else:
        current_volume -= 0.1

    pygame.mixer.music.set_volume(current_volume)

def __change_system_volume(increase):
    if increase:
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
    else:
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)

def increase():
    __change_system_volume(True)

def decrease():
    __change_system_volume(False)
