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


class FixedBackground:
    image = None

    def __init__(self):
        os.chdir('image')
        if FixedBackground.image is None:
            self.image = load_image('KPU_GROUND_FULL.png')
        os.chdir('..\\')

        self.center_object = None
        self.window_left, self.window_bot = 0, 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def set_center_object(self, player):
        self.center_object = player

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bot,
                                       self.canvas_width, self.canvas_height,
                                       0, 0)

    def update(self):
        self.window_left = clamp(0,
                                 int(self.center_object.x)-self.canvas_width//2,
                                 self.w-self.canvas_width)
        self.window_bot = clamp(0,
                                int(self.center_object.y)-self.canvas_height//2,
                                self.h-self.canvas_height)

    def handle_event(self, event):
        pass
