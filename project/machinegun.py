from pico2d import *
import game_world
import main_state


class Machine_gun:
    bullet_right = None
    bullet_left = None
    bullet_top = None
    bullet_bot = None

    def __init__(self, x=0, y=0, direction=-1, delay=0, is_above=0):
        self.x, self.y = x, y
        self.direction = direction
        self.hit = 0
        self.delay = delay
        self.is_above = is_above
        if Machine_gun.bullet_right is None:
            Machine_gun.bullet_right = load_image('machine_gun_bullet_right.png')
        if Machine_gun.bullet_left is None:
            Machine_gun.bullet_left = load_image('machine_gun_bullet_left.png')
        if Machine_gun.bullet_top is None:
            Machine_gun.bullet_top = load_image('machine_gun_bullet_top.png')
        if Machine_gun.bullet_bot is None:
            Machine_gun.bullet_bot = load_image('machine_gun_bullet_bot.png')

    def update(self):
        # 이동
        if self.delay > 0:
            self.delay -= 1

        if self.delay == 0:
            if self.is_above == 0:
                self.x += self.direction * 5
            elif self.is_above == 1:
                self.y += 5
            else:
                self.y -= 5

        # 화면 밖으로 넘어감
        if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            game_world.remove_object(self)
        # 적을 맞힘
        elif main_state.inRect(main_state.enemy.x - 10, main_state.enemy.y + 50,
                               main_state.enemy.x + 10, main_state.enemy.y - 50, self.x, self.y):
            main_state.enemy.hp -= 1
            main_state.enemy.hit = 1
            game_world.remove_object(self)

    def draw(self):
        if self.delay == 0:
            if self.is_above == 1:
                self.bullet_top.clip_draw(0, 0, 100, 100, self.x, self.y, 35, 70)
            elif self.is_above == 2:
                self.bullet_bot.clip_draw(0, 0, 100, 100, self.x, self.y, 35, 70)
            elif self.direction > 0:
                self.bullet_right.clip_draw(0, 0, 100, 100, self.x, self.y, 70, 35)
            elif self.direction < 0:
                self.bullet_left.clip_draw(0, 0, 100, 100, self.x, self.y, 70, 35)
