from pico2d import *
import game_world
from py_ground import Ground


class Map:

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.ground = 0

    def update(self):
        pass

    def draw(self):
        if self.ground == 0:
            ground = Ground(self.x, self.y, self.w, self.h)
            game_world.add_object(ground, 0)
            ground.set_background(self.bg)
            self.ground = 1

    def set_background(self, bg):
        self.bg = bg

    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2,\
               self.x + self.w/2, self.y + self.h/2
