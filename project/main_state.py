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

foothold1, foothold2 = None, None
player = None
handgun = None
heavy_machine_gun = None
grenade = None
infantry = None
font = None
spawn = None


def enter():
    global player, foothold1, foothold2, handgun, infantry, grenade, heavy_machine_gun, spawn
    foothold1 = Map(300, 30, 600, 60)
    foothold2 = Map(900, 90, 600, 120)
    player = Player()
    handgun = Handgun()
    heavy_machine_gun = HeavyMachineGun()
    grenade = Grenade()
    infantry = Infantry()
    spawn = Spawn()

    game_world.add_object(foothold1, 0)
    game_world.add_object(foothold2, 0)
    game_world.add_object(player, 1)
    game_world.add_object(handgun, 1)
    game_world.add_object(heavy_machine_gun, 1)
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
    if collide(handgun, infantry):
        infantry.damaged(1)
        handgun.hit_target()
    if collide(heavy_machine_gun, infantry):
        infantry.damaged(1)
        heavy_machine_gun.hit_target()
    if collide(grenade, infantry):
        infantry.damaged(5)
        grenade.hit_target()
    if collide(player, foothold1) and Player.descending == 1:
        player.landing()
    if collide(player, foothold2) and Player.descending == 1:
        player.landing()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    left_a, top_a, right_a, bot_a = a.get_bb()
    left_b, top_b, right_b, bot_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True
