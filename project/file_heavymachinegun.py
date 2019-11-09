from pico2d import *
import game_world
import main_state
import game_framework


PIXEL_PER_METER = (10.0 / 0.3)
MUZZLE_VELOCITY_KMPH = 200.0  # Km / Hour
MUZZLE_VELOCITY_MPM = (MUZZLE_VELOCITY_KMPH * 1000.0 / 60.0)
MUZZLE_VELOCITY_MPS = (MUZZLE_VELOCITY_MPM / 60.0)
MUZZLE_VELOCITY_PPS = (MUZZLE_VELOCITY_MPS * PIXEL_PER_METER)


class HeavyMachineGun:
    bullet = None

    def __init__(self, x=0, y=0, direction=-1, delay=0, is_above=0):
        self.x, self.y = x, y
        self.direction = direction
        self.hit = 0
        self.delay = delay
        self.is_above = is_above
        if HeavyMachineGun.bullet is None:
            HeavyMachineGun.bullet = load_image('machine_gun_bullet.png')

    def update(self):
        # 이동
        if self.delay > 0:
            self.delay -= 1

        if self.delay == 0:
            if self.is_above == 0:
                self.x += self.direction * MUZZLE_VELOCITY_PPS * game_framework.frame_time
            elif self.is_above == 1:
                self.y += MUZZLE_VELOCITY_PPS * game_framework.frame_time
            else:
                self.y -= MUZZLE_VELOCITY_PPS * game_framework.frame_time

        # 화면 밖으로 넘어감
        if self.x < 0 or self.x > 1200 or self.y < 0 or self.y > 800:
            game_world.remove_object(self)
        # 적을 맞힘
        elif main_state.InRect(main_state.infantry.x - 10, main_state.infantry.y + 50,
                               main_state.infantry.x + 10, main_state.infantry.y - 50, self.x, self.y):
            main_state.infantry.hp -= 1
            main_state.infantry.hit = 1
            game_world.remove_object(self)

    def draw(self):
        if self.delay == 0:
            if self.is_above == 1:
                self.bullet.clip_composite_draw(0, 0, 100, 100, -math.pi / 2, 'h', self.x, self.y, 70, 35)
            elif self.is_above == 2:
                self.bullet.clip_composite_draw(0, 0, 100, 100, math.pi / 2, 'h', self.x, self.y, 70, 35)
            elif self.direction > 0:
                self.bullet.clip_composite_draw(0, 0, 100, 100, math.pi, 'h', self.x, self.y, 70, 35)
            elif self.direction < 0:
                self.bullet.clip_composite_draw(0, 0, 100, 100, 0, 'h', self.x, self.y, 70, 35)
