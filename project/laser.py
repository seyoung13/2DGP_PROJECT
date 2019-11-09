from pico2d import *
import game_world
import main_state


class Laser:
    image = None

    def __init__(self, x=0, y=0, direction=-1, is_above=0):
        self.x, self.y = x, y
        self.frame_y = 0
        self.direction = direction
        self.hit = 0
        self.is_above = is_above
        self.timer = 50
        if Laser.image is None:
            Laser.image = load_image('laser.png')

    def update(self):
        # 이동
        self.frame_y = (self.frame_y+1) % 4
        self.timer -= 1

        # 화면 밖으로 넘어감
        if self.timer < 0:
            game_world.remove_object(self)
        # 적을 맞힘
        if main_state.infantry.y - 50 < self.y < main_state.infantry.y + 50:
            main_state.infantry.hp -= 1
            main_state.infantry.hit = 1

    def draw(self):
        self.image.clip_draw(self.x+(self.direction*300), self.frame_y*60, 60, 60, self.x, self.y, 1200, 20)
