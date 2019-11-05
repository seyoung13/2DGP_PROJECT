import random
import json
import os

from pico2d import *

import game_framework
import game_world

from map import Map
from player import Player
from pistol import Pistol
from machinegun import Machine_gun
from grenade import Grenade
from enemy import Enemy

name = "MainState"

map1 = None
player = None
pistol = None
machine_gun = None
grenade = None
enemy = None
font = None


def enter():
    global player, map1, pistol, enemy, grenade, machine_gun
    map1 = Map()
    player = Player()
    pistol = Pistol()
    machine_gun = Machine_gun()
    grenade = Grenade()
    enemy = Enemy()

    game_world.add_object(map1, 0)
    game_world.add_object(player, 1)
    game_world.add_object(pistol, 1)
    game_world.add_object(machine_gun, 1)
    game_world.add_object(grenade, 1)
    game_world.add_object(enemy, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    evnets = get_events()
    for event in evnets:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def inRect(left, top, right, bottom, x, y):
    if left < x < right and bottom < y < top:
        return True
    else:
        return False
