from pico2d import *


class Ground:

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h

        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)

    def update(self):
        pass
