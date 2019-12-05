from pico2d import *
import game_world
import main_state


class Infantry:
    image = None
    image_hit = None

    def __init__(self, x=0, y=0, hp=0):
        self.x, self.y = x, y
        self.w, self.h = 20, 100
        self.cx, self.cy = 0, 0
        self.hp = hp
        self.sick = 0
        self.face_direction = 1
        self.timer = 200
        os.chdir('image')
        if Infantry.image is None:
            Infantry.image = load_image('animation_sheet.png')
        if Infantry.image_hit is None:
            Infantry.image_hit = load_image('animation_sheet_hit.png')
        os.chdir('..\\')

    def update(self):
        # 이동
        self.x += 0.5 * self.face_direction
        # 판정
        if self.hp <= 0:
            game_world.remove_object(self)

        if self.sick > 0:
            self.sick -= 0.25

        if self.timer > 0:
            self.timer -= 1

        if self.timer <= 0:
            self.face_direction *= -1
            self.timer = 200

        self.x = clamp(25, self.x, 1200 - 25)

    def draw(self):
        self.cx, self.cy = self.x - self.bg.window_left, self.y - self.bg.window_bot
        if self.sick == 0:
            self.image.clip_draw(0, 100 * 2, 100, 100, self.cx, self.cy)
        else:
            self.image_hit.clip_draw(0, 100 * 2, 100, 100, self.cx, self.cy)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.cx - self.w / 2, self.cy - self.h / 2, \
               self.cx + self.w / 2, self.cy + self.h / 2

    def damaged(self, damage):
        self.hp -= damage
        self.sick = 1

    def set_background(self, bg):
        self.bg = bg
