from pico2d import *
import game_world
import main_state


class Infantry:
    image = None
    image_hit = None

    def __init__(self, x=0, y=0, hp=0):
        self.x, self.y = x, y
        self.hp = hp
        self.hit = 0
        self.face_direction = 1
        if Infantry.image is None:
            Infantry.image = load_image('animation_sheet.png')
        if Infantry.image_hit is None:
            Infantry.image_hit = load_image('animation_sheet_hit.png')
        self.timer = 200

    def update(self):
        # 이동
        self.x += 0.5 * self.face_direction
        # 판정
        if self.hp <= 0:
            game_world.remove_object(self)

        if self.hit > 0:
            self.hit -= 0.25

        if self.timer > 0:
            self.timer -= 1

        if self.timer <= 0:
            self.face_direction *= -1
            self.timer = 200

        self.x = clamp(25, self.x, 1200 - 25)

    def draw(self):
        if self.hit == 0:
            self.image.clip_draw(0, 100 * 2, 100, 100, self.x, self.y)
        else:
            self.image_hit.clip_draw(0, 100 * 2, 100, 100, self.x, self.y)
