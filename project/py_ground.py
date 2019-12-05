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
        self.cx, self.cy = self.x - self.bg.window_left, self.y - self.bg.window_bot
        self.image.draw(self.cx, self.cy, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.cx - self.w/2, self.cy - self.h/2,\
               self.cx + self.w/2, self.cy + self.h/2

    def set_background(self, bg):
        self.bg = bg
