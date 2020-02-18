from pico2d import *
import game_world
import main_state
import game_framework
import random
from math import *
import os

from py_handgun import Handgun
from py_heavymachinegun import HeavyMachineGun
from py_lasergun import LaserGun
from py_grenade import Grenade
import py_map

# Boy Event
# enum 이랑 비슷 0, 1, 2, 3
RIGHT_KEY_DOWN, LEFT_KEY_DOWN, RIGHT_KEY_UP, LEFT_KEY_UP, UP_KEY_DOWN, UP_KEY_UP, DOWN_KEY_DOWN, DOWN_KEY_UP, \
A_KEY_DOWN, S_KEY_DOWN, D_KEY_DOWN, Q_KEY_DOWN, E_KEY_DOWN, W_KEY_DOWN = range(14)

FRONT_SIDE, TOP_SIDE, BOTTOM_SIDE = range(3)

PISTOL, MACHINE_GUN, LASER = range(3)

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 50.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 40.0  # Km / Hour
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_KEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_KEY_UP,
    (SDL_KEYUP, SDLK_UP): UP_KEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_KEY_UP,
    (SDL_KEYDOWN, SDLK_a): A_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_s): S_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_d): D_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_q): Q_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_w): W_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_e): E_KEY_DOWN
}


# Boy States
class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += RUN_SPEED_PPS
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= RUN_SPEED_PPS
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_KEY_UP:
            player.velocity += RUN_SPEED_PPS
        elif event == UP_KEY_DOWN:
            player.looking = TOP_SIDE
        elif event == UP_KEY_UP:
            player.looking = FRONT_SIDE
        elif event == DOWN_KEY_UP:
            player.looking = FRONT_SIDE

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and not player.jumping:
            player.jumping = True
            player.descending = False
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN
        if event == W_KEY_DOWN:
            player.weapon = LASER
        if event == DOWN_KEY_DOWN and player.jumping:
            player.looking = BOTTOM_SIDE

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.sit_y = 0

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(0, 300, 100, 100, player.cx, player.cy)
        elif player.direction < 0:
            player.image.clip_draw(0, 200, 100, 100, player.cx, player.cy)


class RunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += RUN_SPEED_PPS
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= RUN_SPEED_PPS
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_KEY_UP:
            player.velocity += RUN_SPEED_PPS
        elif event == UP_KEY_DOWN:
            player.looking = TOP_SIDE
        elif event == UP_KEY_UP:
            player.looking = FRONT_SIDE
        elif event == DOWN_KEY_UP:
            player.looking = FRONT_SIDE

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and not player.jumping:
            player.jumping = True
            player.descending = False
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN
        if event == W_KEY_DOWN:
            player.weapon = LASER
        if event == DOWN_KEY_DOWN and player.jumping:
            player.looking = BOTTOM_SIDE

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.sit_y = 0

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(int(player.frame) * 100, 100 * 1, 100, 100, player.cx, player.cy)
        elif player.direction < 0:
            player.image.clip_draw(int(player.frame) * 100, 100 * 0, 100, 100, player.cx, player.cy)


class SitState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += RUN_SPEED_PPS
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= RUN_SPEED_PPS
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_KEY_UP:
            player.velocity += RUN_SPEED_PPS
        elif event == DOWN_KEY_UP:
            player.looking = FRONT_SIDE

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and not player.jumping:
            player.jumping = True
            player.descending = False
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN
        if event == W_KEY_DOWN:
            player.weapon = LASER

    @staticmethod
    def do(player):
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        if not player.jumping:
            player.sit_y = -30
            player.muzzle_angle = 0.0
        else:
            player.sit_y = 0

    @staticmethod
    def draw(player):
        if player.jumping:
            player.image.clip_draw(0, 100 * 1, 50, 100, player.cx, player.cy + player.sit_y)
        elif player.direction > 0:
            player.image.clip_draw(0, 100, 100, 50, player.cx, player.cy + player.sit_y)
        elif player.direction < 0:
            player.image.clip_draw(0, 100, 100, 50, player.cx, player.cy + player.sit_y)


class CrawlState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += RUN_SPEED_PPS
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= RUN_SPEED_PPS
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_KEY_UP:
            player.velocity += RUN_SPEED_PPS

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and not player.jumping:
            player.jumping = True
            player.descending = False
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN
        if event == W_KEY_DOWN:
            player.weapon = LASER

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)

        if not player.jumping:
            player.sit_y = -30
            player.x += 0.5 * player.velocity * game_framework.frame_time
            player.looking = FRONT_SIDE
        else:
            player.sit_y = 0
            player.x += player.velocity * game_framework.frame_time

    @staticmethod
    def draw(player):
        if player.jumping:
            player.image.clip_draw(int(player.frame) * 100, 100 * 1, 50, 100, player.cx, player.cy +
                                   player.sit_y)
        elif player.direction > 0:
            player.image.clip_draw(int(player.frame) * 100, 100 * 1, 100, 50, player.cx, player.cy +
                                   player.sit_y)
        elif player.direction < 0:
            player.image.clip_draw(int(player.frame) * 100, 100 * 0, 100, 50,player.cx, player.cy +
                                   player.sit_y)


next_state_table = {
    IdleState: {RIGHT_KEY_DOWN: RunState, RIGHT_KEY_UP: RunState,
                LEFT_KEY_DOWN: RunState, LEFT_KEY_UP: RunState,
                DOWN_KEY_DOWN: SitState, DOWN_KEY_UP: SitState,
                UP_KEY_DOWN: IdleState, UP_KEY_UP: IdleState,
                A_KEY_DOWN: IdleState, S_KEY_DOWN: IdleState, D_KEY_DOWN: IdleState,
                Q_KEY_DOWN: IdleState, E_KEY_DOWN: IdleState, W_KEY_DOWN: IdleState},

    RunState: {RIGHT_KEY_DOWN: IdleState, RIGHT_KEY_UP: IdleState,
               LEFT_KEY_DOWN: IdleState, LEFT_KEY_UP: IdleState,
               DOWN_KEY_DOWN: CrawlState, DOWN_KEY_UP: CrawlState,
               UP_KEY_DOWN: RunState, UP_KEY_UP: RunState,
               A_KEY_DOWN: RunState, S_KEY_DOWN: RunState, D_KEY_DOWN: RunState,
               Q_KEY_DOWN: RunState, E_KEY_DOWN: RunState, W_KEY_DOWN: RunState},

    SitState: {RIGHT_KEY_DOWN: CrawlState, RIGHT_KEY_UP: CrawlState,
               LEFT_KEY_DOWN: CrawlState, LEFT_KEY_UP: CrawlState,
               DOWN_KEY_DOWN: IdleState, DOWN_KEY_UP: IdleState,
               UP_KEY_DOWN: IdleState, UP_KEY_UP: IdleState,
               A_KEY_DOWN: SitState, S_KEY_DOWN: SitState, D_KEY_DOWN: SitState,
               Q_KEY_DOWN: SitState, E_KEY_DOWN: SitState, W_KEY_DOWN: SitState},

    CrawlState: {RIGHT_KEY_DOWN: SitState, RIGHT_KEY_UP: SitState,
                 LEFT_KEY_DOWN: SitState, LEFT_KEY_UP: SitState,
                 DOWN_KEY_DOWN: RunState, DOWN_KEY_UP: RunState,
                 UP_KEY_DOWN: RunState, UP_KEY_UP: RunState,
                 A_KEY_DOWN: CrawlState, S_KEY_DOWN: CrawlState, D_KEY_DOWN: CrawlState,
                 Q_KEY_DOWN: CrawlState, E_KEY_DOWN: CrawlState, W_KEY_DOWN: CrawlState},
}


class Player:
    image = None
    descending = True

    def __init__(self):
        self.x, self.y = 100, 500
        self.w, self.h = 30, 80
        self.cx, self.cy = 0, 0
        self.frame = 0
        self.direction = 1
        self.velocity = 0
        self.bg = 0
        self.canvas_width, self.canvas_height = get_canvas_width(), get_canvas_height()
        self.jumping, self.jump_y, self.before_jump_y, self.sit_y = True, 0, 0, 0
        self.weapon = PISTOL
        self.shoot_delay = 0
        self.looking = FRONT_SIDE
        self.muzzle_angle = 0.0

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        os.chdir('image')
        if Player.image is None:
            Player.image = load_image('animation_sheet.png')
        os.chdir('..\\')

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        self.cx, self.cy = self.x - self.bg.window_left, self.y - self.bg.window_bot

        # 점프
        if not self.jumping:
            self.before_jump_y = self.y
        if self.y - self.before_jump_y >= 200:
            Player.descending = True
        if self.jumping and not Player.descending:
            self.y += JUMP_SPEED_PPS * game_framework.frame_time
        if self.jumping and Player.descending:
            self.y -= JUMP_SPEED_PPS * game_framework.frame_time
        # 총구 방향
        if self.looking == TOP_SIDE:
            if self.muzzle_angle < pi / 2:
                self.muzzle_angle += pi / 32
        if self.looking == BOTTOM_SIDE:
            if self.muzzle_angle > -pi / 2:
                self.muzzle_angle -= pi / 32
        if self.looking == FRONT_SIDE:
            if self.muzzle_angle == 0:
                self.muzzle_angle = 0
            elif self.muzzle_angle > 0:
                self.muzzle_angle -= pi / 32
            elif self.muzzle_angle < 0:
                self.muzzle_angle += pi / 32

        self.shoot_delay -= 1

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cx - self.w / 2, self.cy - self.h / 2, \
               self.cx + self.w / 2, self.cy + self.h / 2 + self.sit_y * 1.5

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def shoot(self):
        if self.weapon == PISTOL:
            if Handgun.max_pistol < 4:
                bullet = Handgun(self.x, self.y + self.jump_y + self.sit_y + 10, self.direction, self.muzzle_angle)
                game_world.add_object(bullet, 1)
                bullet.set_background(self.bg)
                Handgun.max_pistol += 1
        elif self.weapon == MACHINE_GUN and self.shoot_delay < 0:
            bullet = [HeavyMachineGun(self.x + random.randint(-15, 15) * sin(self.muzzle_angle) + self.direction * 15,
                                      self.y + self.jump_y + random.randint(-15, 15) * cos(self.muzzle_angle)
                                      + 10 + self.sit_y, self.direction, i*20, self.muzzle_angle) for i in range(4)]
            for i in range(4):
                game_world.add_object(bullet[i], 1)
                bullet[i].set_background(self.bg)
            self.shoot_delay = 55
        elif self.weapon == LASER:
            bullet = LaserGun(self.x, self.y + self.jump_y + self.sit_y + 10, self.direction, self.muzzle_angle)
            game_world.add_object(bullet, 1)

    def throw(self):
        if Grenade.max_grenade < 2:
            grenade = Grenade(self.x, self.y + self.jump_y, self.direction, self.velocity)
            game_world.add_object(grenade, 1)
            grenade.set_background(self.bg)
            Grenade.max_grenade += 1

    def landing(self):
        Player.descending = False
        self.jumping = False

    def falling(self):
        Player.descending = True
        self.jumping = True

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
