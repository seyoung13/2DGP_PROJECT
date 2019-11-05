from pico2d import *
import game_world
import main_state


class Pistol:
    image = None
    max_pistol = 1

    def __init__(self, x=0, y=0, direction=-1):
        self.x, self.y = x, y
        self.direction = direction
        self.hit = 0
        if Pistol.image is None:
            Pistol.image = load_image('pistol_bullet.png')

    def update(self):
        # 이동
        self.x += self.direction * 5

        # 화면 밖으로 넘어감
        if self.x < 0 or self.x > 1200:
            Pistol.max_pistol -= 1
            game_world.remove_object(self)
        # 적을 맞힘
        elif main_state.inRect(main_state.enemy.x - 10, main_state.enemy.y + 50,
                               main_state.enemy.x + 10, main_state.enemy.y - 50, self.x, self.y):
            Pistol.max_pistol -= 1
            main_state.enemy.hp -= 1
            main_state.enemy.hit = 1
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, 20, 20)
