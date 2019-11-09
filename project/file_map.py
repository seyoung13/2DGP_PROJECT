from pico2d import *
import game_world
from ground import Ground
from background import Background


class Map:
    ground1 = 0
    ground2 = 0
    background1 = 0

    def __init__(self):
        self.bw, self.bh = 1200, 800
        self.g1x, self.g1y = 400, 30
        self.g1w, self.g1h = 800, 60
        self.g2x, self.g2y = 1000, 60
        self.g2w, self.g2h = 400, 60

    def update(self):
        pass

    def draw(self):
        if Map.background1 == 0:
            background1 = Background(self.bw, self.bh)
            game_world.add_object(background1, 0)
            Map.background1 = 1

        if Map.ground1 == 0:
            ground1 = Ground(self.g1x, self.g1y, self.g1w, self.g1h)
            game_world.add_object(ground1, 0)
            Map.ground1 = 1

        if Map.ground2 == 0:
            ground2 = Ground(self.g2x, self.g2y, self.g2w, self.g2h)
            game_world.add_object(ground2, 0)
            Map.ground2 = 1

