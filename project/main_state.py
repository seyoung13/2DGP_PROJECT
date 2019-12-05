import random
import json
import os

from pico2d import *

import game_framework
import game_world

from py_map import Map
from py_player import Player
from py_handgun import Handgun
from py_heavymachinegun import HeavyMachineGun
from py_grenade import Grenade
from py_background import Background
from py_infantry import Infantry
import py_spawn

name = "MainState"

foothold1, foothold2, foothold3 = None, None, None
background = None
player = None
handgun = None
heavy_machine_gun = None
grenade = None
infantry = None
font = None


def enter():
    global player,  handgun, infantry, grenade, heavy_machine_gun, background
    global foothold1, foothold2, foothold3
    foothold1 = Map(300, 30, 600, 60)
    foothold2 = Map(900, 90, 600, 60)
    foothold3 = Map(2000, 30, 1600, 60)
    player = Player()
    handgun = Handgun()
    heavy_machine_gun = HeavyMachineGun()
    grenade = Grenade()
    infantry = py_spawn.deploy_infantry()
    background = Background()

    game_world.add_object(background, 0)
    game_world.add_object(foothold1, 0)
    game_world.add_object(foothold2, 0)
    game_world.add_object(foothold3, 0)
    game_world.add_object(player, 1)
    game_world.add_object(handgun, 1)
    game_world.add_object(heavy_machine_gun, 1)
    game_world.add_object(grenade, 1)

    background.set_center_obj(player)
    player.set_background(background)
    foothold1.set_background(background)
    foothold2.set_background(background)
    foothold3.set_background(background)
    handgun.set_background(background)
    heavy_machine_gun.set_background(background)
    grenade.set_background(background)
    infantry.set_background(background)

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

    if Player.descending:
        if collide(player, foothold1):
            player.landing()
        elif collide(player, foothold2):
            player.landing()
        elif collide(player, foothold3):
            player.landing()
    if not Player.descending and not player.jumping:
        if not collide(player, foothold1) and not collide(player, foothold2) and not collide(player, foothold3):
            player.falling()


def collide(a, b):
    left_a, bot_a, right_a, top_a = a.get_bb()
    left_b, bot_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bot_b: return False
    if bot_a > top_b: return False

    return True


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()



