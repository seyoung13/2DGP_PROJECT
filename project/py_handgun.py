from pico2d import *
import game_world
import main_state
import game_framework
import os
from math import *

PIXEL_PER_METER = (10.0 / 0.3)
MUZZLE_VELOCITY_KMPH = 150.0  # Km / Hour
MUZZLE_VELOCITY_MPM = (MUZZLE_VELOCITY_KMPH * 1000.0 / 60.0)
MUZZLE_VELOCITY_MPS = (MUZZLE_VELOCITY_MPM / 60.0)
MUZZLE_VELOCITY_PPS = (MUZZLE_VELOCITY_MPS * PIXEL_PER_METER)


class Handgun:
    image = None
    max_pistol = 1

    def __init__(self, x=0, y=0, direction=-1, muzzle_angle=0.0):
        self.x, self.y = x, y
        self.direction = direction
        self.hit = 0
        self.muzzle_angle = muzzle_angle
        self.size = 20
        os.chdir('image')
        if Handgun.image is None:
            Handgun.image = load_image('pistol_bullet.png')
        os.chdir('..\\')

    def update(self):
        # 이동
        if -pi/4 < self.muzzle_angle < pi/4:
            self.x += self.direction * MUZZLE_VELOCITY_PPS * game_framework.frame_time
        elif self.muzzle_angle == pi/2 or -pi/2:
            self.y += MUZZLE_VELOCITY_PPS * game_framework.frame_time * sin(self.muzzle_angle)

        # 화면 밖으로 넘어감
        if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            Handgun.max_pistol -= 1
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.size / 2, self.y - self.size / 2, \
               self.x + self.size / 2, self.y + self.size / 2

    def hit_target(self):
        Handgun.max_pistol -= 1
        game_world.remove_object(self)
