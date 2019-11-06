from pico2d import *
import game_world
import random
import player
from enemy import Enemy


class Spawn:

    def __init__(self):
        self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
        self.timer = 0
        self.enemy = None

    def update(self):
        if self.timer <= 0:
            self.x, self.y = random.randint(100, 1100), random.randint(70, 150)
            self.spawn_enemy()
            self.timer = 1000

        if self.timer > 0:
            self.timer -= 1

    def spawn_enemy(self):
        soldier = Enemy(self.x, self.y)
        game_world.add_objects(soldier, 1)

    def draw(self):
        pass


