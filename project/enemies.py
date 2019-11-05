from pico2d import *
import game_world
import random
from enemy import Enemy


class Appear:

    def __init__(self):
        self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
        self.timer = 0

    def update(self):
        if self.timer <= 0:
            self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
            self.timer = 1000
            soldier = Enemy(self.x, self.y)
            game_world.add_object(soldier, 1)

        if self.timer > 0:
            self.timer -= 1

    def draw(self):
        pass


