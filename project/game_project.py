from pico2d import *
import random


class Grass:
    def __init__(self):
        self.x, self.y = None, None
        self.w, self.h = None, None
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(self.x, self.y, self.w, self.h)


class Background:
    def __init__(self):
        self.image = load_image('KPU_GROUND_FULL.png')

    def draw(self):
        self.image.draw(WinWidth / 2, WinHeight / 2, WinWidth, WinHeight)


class Player:
    def __init__(self):
        self.x, self.y = random.randint(0, 400), 90
        self.ground = None
        self.direction, self.face_direction = 0, 1
        self.jumping, self.jump_y, self.jump_count = 0, 0, 0
        self.frame = 0
        self.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        # 이동
        self.x += 0.1 * self.direction
        for i in range(2):
            if grass[i].x - grass[i].w/2 < self.x < grass[i].x + grass[i].w/2:
                self.ground = grass[i].y + grass[i].h
                if self.jumping == 0:
                    self.y = grass[i].y + grass[i].h
        # 점프
        if self.jumping == 1 and self.jump_count <= 20:
            self.jump_count += 0.1
        if self.jump_count >= 20 or self.y < self.ground:
            self.jumping = 0
            self.jump_count = 0
        self.jump_y = -(self.jump_count ** 2) + (20 * self.jump_count)

    def draw(self):
        if self.direction == 0:
            if self.face_direction > 0:
                self.image.clip_draw(0, 100 * 3, 100, 100, self.x, self.y + self.jump_y)
            elif self.face_direction < 0:
                self.image.clip_draw(0, 100 * 2, 100, 100, self.x, self.y + self.jump_y)
        elif self.direction > 0:
            self.image.clip_draw(self.frame * 100, 100 * 1, 100, 100, self.x, self.y + self.jump_y)
        elif self.direction < 0:
            self.image.clip_draw(self.frame * 100, 100 * 0, 100, 100, self.x, self.y + self.jump_y)
        self.x = clamp(25, self.x, 1200 - 25)
        self.x += self.direction * 1.5


class Pistol:
    def __init__(self):
        self.x, self.y = 0, 0
        self.direction = 0
        self.remain = 0
        self.image = load_image('bullet.png')

    def update(self):
        if self.remain == 0:
            self.x, self.y = player.x, player.y + player.jump_y
            self.direction = player.face_direction
        elif self.remain > 0:
            self.x += self.direction * 5
            self.remain -= 0.5
        # 판정
        if infantry.hp > 0 and self.remain > 0 and \
                infantry.x - 10 < self.x < infantry.x + 10 and infantry.y - 50 < self.y < infantry.y + 50:
            infantry.hp -= 1
            self.remain = 0

    def draw(self):
        self.image.clip_draw(0, 0, 60, 60, self.x, self.y, 30, 30)


class Enemy:
    def __init__(self):
        self.x, self.y = random.randint(600, 1100), 150
        self.hp = 5
        self.direction, self.face_direction = 0, 1
        self.jumping, self.jump_y, self.jump_count = 0, 0, 0
        self.frame = 0
        self.image = load_image('animation_sheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        # 이동
        self.x += 0.1 * self.direction
        for i in range(2):
            if grass[i].x - grass[i].w/2 < self.x < grass[i].x + grass[i].w/2:
                self.y = grass[i].y+grass[i].h
        # 점프
        if self.jumping == 1 and self.jump_count <= 20:
            self.jump_count += 0.1
        if self.jump_count >= 20:
            self.jumping = 0
            self.jump_count = 0
        self.jump_y = -(self.jump_count ** 2) + (20 * self.jump_count)
        # 판정
        if self.hp <= 0:
            self.x = random.randint(600, 1100)
            self.y = random.randint(50, 150)
            self.hp = 5

    def draw(self):
        if self.direction == 0:
            if self.face_direction > 0:
                self.image.clip_draw(0, 100 * 3, 100, 100, self.x, self.y + self.jump_y)
            elif self.face_direction < 0:
                self.image.clip_draw(0, 100 * 2, 100, 100, self.x, self.y + self.jump_y)
        elif self.direction > 0:
            self.image.clip_draw(self.frame * 100, 100 * 1, 100, 100, self.x, self.y + self.jump_y)
        elif self.direction < 0:
            self.image.clip_draw(self.frame * 100, 100 * 0, 100, 100, self.x, self.y + self.jump_y)
        self.x = clamp(25, self.x, 1200 - 25)
        self.x += self.direction * 1.5


def BulletLimit(arr, size, num):
    for i in range(size):
        if arr[i].remain == 0:
            arr[i].remain = num
            return
    return


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            # 이동
            if event.key == SDLK_RIGHT:
                player.direction += 1
                player.face_direction = 1
            elif event.key == SDLK_LEFT:
                player.direction -= 1
                player.face_direction = -1
            # 공격
            elif event.key == SDLK_a:
                BulletLimit(pistol, pistol_max, 200)
            # 점프
            elif event.key == SDLK_s and player.jumping == 0:
                player.jumping = 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.direction -= 1
            elif event.key == SDLK_LEFT:
                player.direction += 1


WinWidth, WinHeight = 1200, 800
running = True

open_canvas(WinWidth, WinHeight)
grass = [Grass() for i in range(2)]

grass[0].x, grass[0].y, grass[0].w, grass[0].h = 400, 30, 800, 60
grass[1].x, grass[1].y, grass[1].w, grass[1].h = 1000, 90, 400, 60
background = Background()

player = Player()
pistol_max = 4
pistol = [Pistol() for i in range(pistol_max)]
infantry = Enemy()

while running:
    clear_canvas()
    handle_events()

    background.draw()
    for i in range(2):
        grass[i].draw()
    player.draw()
    if infantry.hp > 0:
        infantry.draw()

    for i in range(pistol_max):
        if pistol[i].remain != 0:
            pistol[i].draw()

    player.update()
    infantry.update()

    for i in range(pistol_max):
        pistol[i].update()

    update_canvas()

close_canvas()
