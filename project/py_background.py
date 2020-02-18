from pico2d import*


class Background:
    image = None

    def __init__(self, w, h):
        self.w, self.h = w, h
        os.chdir('image')
        if Background.image is None:
            self.image = load_image('KPU_GROUND_FULL.png')
        os.chdir('..\\')

    def draw(self):
        self.image.draw(self.w / 2, self.h / 2, self.w, self.h)

    def update(self):
        pass
