from pico2d import *
import game_world
import random
import py_player
from py_infantry import Infantry


infantry = None


def deploy_infantry():
    global infantry
    infantry = Infantry(random.randint(100, 1000), random.randint(80, 120), 5)
    game_world.add_object(infantry, 1)
    return infantry


def draw():
    pass


def update():
    pass

