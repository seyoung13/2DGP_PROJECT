from pico2d import*


class Background:
    image = None

    def __init__(self):
        self.w, self.h = 60000, 400
        self.canvas_width, self.canvas_height = get_canvas_width(), get_canvas_height()
        self.window_left, self.window_bot = 0, 0
        self.center_obj = None
        os.chdir('image')
        if Background.image is None:
            self.image = load_image('KPU_GROUND_FULL.png')
        os.chdir('..\\')

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bot, self.canvas_width, self.canvas_height, 0, 0)
        for i in range(5):
            self.image.clip_draw_to_origin(self.window_left + 6000 * (i+1), self.window_bot,
                                           self.canvas_width, self.canvas_height, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(self.center_obj.x) - self.canvas_width//2, self.w - self.canvas_width)
        self.window_bot = clamp(0, int(self.center_obj.y) - self.canvas_height//2, self.h - self.canvas_height)

    def set_center_obj(self, player):
        self.center_obj = player
