from pico2d import *
import os


class Ground:

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        os.chdir('image')
        self.image = load_image('grass.png')
        os.chdir('..\\')

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2,\
               self.x + self.w/2, self.y + self.h/2

