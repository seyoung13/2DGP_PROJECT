import random
import json
import os

from pico2d import *

import game_framework
import game_world

from file_map import Map
from file_player import Player
from file_handgun import Handgun
from file_heavymachinegun import HeavyMachineGun
from file_grenade import Grenade
from file_infantry import Infantry
from file_spawn import Spawn

name = "MainState"

map1 = None
player = None
pistol = None
machine_gun = None
grenade = None
infantry = None
font = None
spawn = None


def enter():
    global player, map1, pistol, infantry, grenade, machine_gun, spawn
    map1 = Map()
    player = Player()
    pistol = Handgun()
    machine_gun = HeavyMachineGun()
    grenade = Grenade()
    infantry = Infantry()
    spawn = Spawn()

    game_world.add_object(map1, 0)
    game_world.add_object(player, 1)
    game_world.add_object(pistol, 1)
    game_world.add_object(machine_gun, 1)
    game_world.add_object(grenade, 1)
    game_world.add_object(infantry, 1)
    game_world.add_object(spawn, 0)


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


def InRect(left, top, right, bottom, x, y):
    if left < x < right and bottom < y < top:
        return True
    else:
        return False
