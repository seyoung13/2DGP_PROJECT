from pico2d import *
import game_world
import main_state


class Grenade:
    image = None
    max_grenade = 1

    def __init__(self, x=0, y=0, direction=-1, velcocity=1):
        self.x, self.y = x, y
        self.size = 30
        self.throw_y, self.throw_count = 0, 0
        self.direction = direction
        self.velocity = velcocity
        self.hit = 0
        if Grenade.image is None:
            Grenade.image = load_image('grenade.png')

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
        if self.x < 0 or self.x > 1200 or (self.y+self.throw_y) < 0:
            Grenade.max_grenade -= 1
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y + self.throw_y, self.size, self.size)

    def get_bb(self):
        return self.x - self.size / 2, self.y + self.size / 2, \
               self.x + self.size / 2, self.y - self.size / 2

    def hit_target(self):
        Grenade.max_grenade -= 1
        game_world.remove_object(self)
