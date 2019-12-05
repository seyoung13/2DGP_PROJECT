from pico2d import *
import game_world
import main_state
import game_framework
from math import *
import os

PIXEL_PER_METER = (10.0 / 0.3)
MUZZLE_VELOCITY_KMPH = 150.0  # Km / Hour
MUZZLE_VELOCITY_MPM = (MUZZLE_VELOCITY_KMPH * 1000.0 / 60.0)
MUZZLE_VELOCITY_MPS = (MUZZLE_VELOCITY_MPM / 60.0)
MUZZLE_VELOCITY_PPS = (MUZZLE_VELOCITY_MPS * PIXEL_PER_METER)


class HeavyMachineGun:
    left_bullet = None
    right_bullet = None

    def __init__(self, x=0, y=0, direction=-1, delay=0, muzzle_angle=0):
        self.x, self.y = x, y
        self.w, self.h = 120, 20
        self.cx, self.cy = 0, 0
        self.direction = direction
        self.hit = 0
        self.delay = delay
        self.muzzle_angle = muzzle_angle

        os.chdir('image')
        if HeavyMachineGun.left_bullet is None:
            HeavyMachineGun.left_bullet = load_image('machine_gun_bullet_left.png')
        if HeavyMachineGun.right_bullet is None:
            HeavyMachineGun.right_bullet = load_image('machine_gun_bullet_right.png')
        os.chdir('..\\')

    def update(self):
        # 이동
        if self.delay > 0:
            self.delay -= 1

        if self.delay == 0:
            self.x += self.direction * MUZZLE_VELOCITY_PPS * game_framework.frame_time * cos(self.muzzle_angle)
            self.y += MUZZLE_VELOCITY_PPS * game_framework.frame_time * sin(self.muzzle_angle)

        # 화면 밖으로 넘어감
        if self.x < self.bg.window_left or self.x > self.bg.window_left + 1200 or \
                self.y < self.bg.window_bot or self.y > self.bg.window_bot + 800:
            game_world.remove_object(self)
        # 적을 맞힘

    def draw(self):
        self.cx, self.cy = self.x - self.bg.window_left, self.y - self.bg.window_bot
        if self.delay == 0:
            if self.direction < 0:
                self.left_bullet.clip_composite_draw(0, 0, 100, 100, -self.muzzle_angle, 'w',
                                                     self.cx, self.cy, self.w, self.h)
            elif self.direction > 0:
                self.right_bullet.clip_composite_draw(0, 0, 100, 100, self.muzzle_angle, 'w',
                                                      self.cx, self.cy, self.w, self.h)
            draw_rectangle(*self.get_bb())

    def set_background(self, bg):
        self.bg = bg

    def get_bb(self):
        return self.cx - self.w / 2, self.cy - self.h / 2, \
               self.cx + self.w / 2, self.cy + self.h / 2

    def hit_target(self):
        game_world.remove_object(self)
