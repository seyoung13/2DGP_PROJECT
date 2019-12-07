from pico2d import *
import game_world
from py_grass import Ground

# 맵에다 그래스 다 몰아 넣기


def create_map(background):
    grassland = []
    x, y, w, h = [], [], [], []
    left, right, top, bot = [], [], [], []
    for i in range(10):
        x.append(300 + 600 * i)
        if 1 <= i <= 2 or 6 <= i <= 7:
            y.append(90)
        elif i == 5:
            y.append(150)
        else:
            y.append(30)
        w.append(600)
        h.append(60)

    grassland = [Ground(x[i], [i], w[i], h[i]) for i in range(10)]
    game_world.add_objects(grassland, 1)
    for i in range(10):
        grassland[i].set_background(background)


def draw(self):
    pass


def get_bb(self):
    pass


"""""
class Map:

    def __init__(self):
        self.creating = False
        self.x, self.y, self.w, self.h = [], [], [], []
        self.left, self.right, self.top, self.bot = [], [], [], []
        for i in range(10):
            self.x.append(300+600*i)
            if 1 <= i <= 2 or 6 <= i <= 7:
                self.y.append(90)
            elif i == 5:
                self.y.append(150)
            else:
                self.y.append(30)
            self.w.append(600)
            self.h.append(60)

    def set_background(self, bg):
        self.bg = bg

    def update(self):
        global grassland
        if not self.creating:
            grassland = [Ground(self.x[i], self.y[i], self.w[i], self.h[i], self.bg) for i in range(10)]
            game_world.add_objects(grassland, 1)
            self.creating = True

    def draw(self):
        pass

    def get_bb(self):
        for i in range(10):
            #return self.x[i] - self.w[i] / 2, self.y[i] - self.h[i] / 2, \
                  # self.x[i] + self.w[i] / 2, self.y[i] + self.h[i] / 2
            self.left, self.bot, self.right, self.top = grassland[i].get_bb()
            return self.left, self.bot, self.right, self.top
"""