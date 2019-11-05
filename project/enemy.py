from pico2d import *
import random
import main_state


class Enemy:
    image = None
    image_hit = None

    def __init__(self):
        self.x, self.y = random.randint(100, 1100), random.randint(70, 180)
        self.hp = 5
        self.hit = 0
        self.direction, self.face_direction = 0, 1
        self.jumping, self.jump_y, self.jump_count = 0, 0, 0
        self.frame = 0
        if Enemy.image is None:
            Enemy.image = load_image('animation_sheet.png')
        if Enemy.image_hit is None:
            Enemy.image_hit = load_image('animation_sheet_hit.png')
        self.bullet_x, self.bullet_y = 0, 0

    def update(self):
        self.frame = (self.frame + 1) % 8
        # 이동

        # 판정
        if self.hp <= 0:
            self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
            self.hp = 5

        if self.hit > 0:
            self.hit -= 0.25

    def draw(self):
        if self.hit == 0:
            self.image.clip_draw(0, 100 * 2, 100, 100, self.x, self.y + self.jump_y)
        else:
            self.image_hit.clip_draw(0, 100 * 2, 100, 100, self.x, self.y + self.jump_y)

        self.x = clamp(25, self.x, 1200 - 25)
