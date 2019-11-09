from pico2d import *
import game_world
import random
import file_player
from file_infantry import Infantry


class Spawn:

    def __init__(self):
        self.x, self.y = 0, 0
        self.timer = 500

    def update(self):
        if self.timer > 0:
            self.timer -= 1

        if self.timer == 1:
            self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
            self.spawn_enemy()

        if self.timer == 0:
            self.timer = 500

    def spawn_enemy(self):
        soldier1 = Infantry(self.x, self.y, 5)
        game_world.add_object(soldier1, 1)

    def draw(self):
        pass


