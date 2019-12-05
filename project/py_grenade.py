from pico2d import *
import game_world
import main_state


class Grenade:
    image = None
    max_grenade = 1

    def __init__(self, x=0, y=0, direction=-1, velcocity=1):
        self.x, self.y = x, y
        self.cx, self.cy = 0, 0
        self.size = 30
        self.throw_y, self.throw_count = 0, 0
        self.direction = direction
        self.velocity = velcocity
        self.hit = 0
        os.chdir('image')
        if Grenade.image is None:
            Grenade.image = load_image('grenade.png')
        os.chdir('..\\')

    def update(self):
        # 이동
        self.throw_count += 0.6
        self.throw_y = -(1/20) * (self.throw_count ** 2) + (5 * self.throw_count)
        if self.velocity > 0:
            self.x += 2 * self.direction * +(self.velocity+0.5)
        elif self.velocity < 0:
            self.x += 2 * self.direction * -(self.velocity-0.5)
        elif self.velocity == 0:
            self.x += 2 * self.direction

        # 화면 밖으로 넘어감
        if self.x < self.bg.window_left or self.x > self.bg.window_left + 1200 or \
                self.y < self.bg.window_bot or self.y > self.bg.window_bot + 800:
            Grenade.max_grenade -= 1
            game_world.remove_object(self)

    def draw(self):
        self.cx, self.cy = self.x - self.bg.window_left, self.y - self.bg.window_bot
        self.image.clip_draw(0, 0, 60, 60, self.cx, self.cy + self.throw_y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cx - self.size / 2, self.cy - self.size / 2 + self.throw_y, \
               self.cx + self.size / 2, self.cy + self.size / 2 + self.throw_y

    def hit_target(self):
        Grenade.max_grenade -= 1
        game_world.remove_object(self)

    def set_background(self, bg):
        self.bg = bg