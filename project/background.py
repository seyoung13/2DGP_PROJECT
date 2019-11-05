from pico2d import*


class Background:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.image = load_image('KPU_GROUND_FULL.png')

    def draw(self):
        self.image.draw(self.w / 2, self.h / 2, self.w, self.h)

    def update(self):
        pass
