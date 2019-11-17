from pico2d import *
import game_world
from ground import Ground
from background import Background


class Map:
    background = 0
    ground = 0

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h

    def update(self):
        pass

    def draw(self):
        if Map.background == 0:
            background = Background(1200, 800)
            game_world.add_object(background, 0)
            Map.background = 1

        if Map.ground == 0:
            ground = Ground(self.x, self.y, self.w, self.h)
            game_world.add_object(ground, 0)
            Map.ground = 1

    def get_bb(self):
        return self.x - self.w/2, self.y,\
               self.x + self.w/2, self.y - self.h/2
