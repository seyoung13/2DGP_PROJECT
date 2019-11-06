from pico2d import *
import game_world
import main_state
from pistol import Pistol
from machinegun import Machine_gun
from grenade import Grenade
import random

# Boy Event
# enum 이랑 비슷 0, 1, 2, 3
RIGHT_KEY_DOWN, LEFT_KEY_DOWN, RIGHT_KEY_UP, LEFT_KEY_UP, UP_KEY_DOWN, UP_KEY_UP, DOWN_KEY_DOWN, DOWN_KEY_UP, \
    A_KEY_DOWN, S_KEY_DOWN, D_KEY_DOWN, Q_KEY_DOWN, E_KEY_DOWN = range(13)

PISTOL, MACHINE_GUN, LASER = range(3)
FACING_LEFT, FACING_RIGHT, FACING_TOP = range(3)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_KEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_KEY_UP,
    (SDL_KEYUP, SDLK_UP): UP_KEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_KEY_UP,
    (SDL_KEYDOWN, SDLK_a): A_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_s): S_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_d): D_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_q): Q_KEY_DOWN,
    (SDL_KEYDOWN, SDLK_e): E_KEY_DOWN
}


# Boy States
class IdleState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1
            player.frame = (player.frame + 1) % 8
            player.fy = 0

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0
            player.fy = 2

        player.sit_y = 0
        player.is_above = False

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(0, 100 * (player.fy + 1), 100, 100, player.x, player.y + player.jump_y)
        elif player.direction < 0:
            player.image.clip_draw(0, 100 * player.fy, 100, 100, player.x, player.y + player.jump_y)


class RunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += 2 * player.velocity
        player.x = clamp(25, player.x, 1200 - 25)

        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0

        player.sit_y = 0
        player.is_above = False

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(player.frame * 100, 100 * 1, 100, 100, player.x, player.y + player.jump_y)
        elif player.direction < 0:
            player.image.clip_draw(player.frame * 100, 100 * 0, 100, 100, player.x, player.y + player.jump_y)


class SitState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1
            player.frame = (player.frame + 1) % 8
            player.fy = 0

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0
            player.fy = 2

        player.sit_y = -30
        player.is_above = False

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(0, 100 * (player.fy + 1), 100, 50, player.x, player.y + player.jump_y + player.sit_y)
        elif player.direction < 0:
            player.image.clip_draw(0, 100 * player.fy, 100, 50, player.x, player.y + player.jump_y + player.sit_y)


class CrawlState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.velocity
        player.x = clamp(25, player.x, 1200 - 25)

        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0

        player.sit_y = -30
        player.is_above = False

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(player.frame * 100, 100 * 1, 100, 50, player.x, player.y + player.jump_y +
                                   player.sit_y)
        elif player.direction < 0:
            player.image.clip_draw(player.frame * 100, 100 * 0, 100, 50, player.x, player.y + player.jump_y +
                                   player.sit_y)


class LookAboveState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1
            player.frame = (player.frame + 1) % 8
            player.fy = 0

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0
            player.fy = 2

        player.sit_y = 0
        player.is_above = True

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(0, 100 * (player.fy + 1), 50, 100, player.x, player.y + player.jump_y)
        elif player.direction < 0:
            player.image.clip_draw(0, 100 * player.fy, 50, 100, player.x, player.y + player.jump_y)


class LookAboveRunState:
    @staticmethod
    def enter(player, event):
        if event == RIGHT_KEY_DOWN:
            player.velocity += 1
            player.direction = 1
        elif event == LEFT_KEY_DOWN:
            player.velocity -= 1
            player.direction = -1
        elif event == RIGHT_KEY_UP:
            player.velocity -= 1
        elif event == LEFT_KEY_UP:
            player.velocity += 1

    @staticmethod
    def exit(player, event):
        if event == A_KEY_DOWN:
            player.shoot()
        if event == S_KEY_DOWN and player.jumping == 0:
            player.jumping = 1
        if event == D_KEY_DOWN:
            player.throw()
        if event == Q_KEY_DOWN:
            player.weapon = PISTOL
        if event == E_KEY_DOWN:
            player.weapon = MACHINE_GUN

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += 2 * player.velocity
        player.x = clamp(25, player.x, 1200 - 25)

        player.jump_y = -(player.jump_count ** 2) + (20 * player.jump_count)
        if player.jumping == 1 and player.jump_count < 20:
            player.jump_count += 0.1

        if player.jump_count > 20:
            player.jumping = 0
            player.jump_count = 0

        player.sit_y = 0
        player.is_above = True

    @staticmethod
    def draw(player):
        if player.direction > 0:
            player.image.clip_draw(player.frame * 100, 100 * 1, 50, 100, player.x, player.y + player.jump_y)
        elif player.direction < 0:
            player.image.clip_draw(player.frame * 100, 100 * 0, 50, 100, player.x, player.y + player.jump_y)


next_state_table = {
    IdleState: {RIGHT_KEY_DOWN: RunState, RIGHT_KEY_UP: RunState,
                LEFT_KEY_DOWN: RunState, LEFT_KEY_UP: RunState,
                DOWN_KEY_DOWN: SitState, DOWN_KEY_UP: SitState,
                UP_KEY_DOWN: LookAboveState, UP_KEY_UP: LookAboveState,
                A_KEY_DOWN: IdleState, S_KEY_DOWN: IdleState, D_KEY_DOWN: IdleState,
                Q_KEY_DOWN: IdleState, E_KEY_DOWN: IdleState},

    RunState: {RIGHT_KEY_DOWN: IdleState, RIGHT_KEY_UP: IdleState,
               LEFT_KEY_DOWN: IdleState, LEFT_KEY_UP: IdleState,
               DOWN_KEY_DOWN: CrawlState, DOWN_KEY_UP: CrawlState,
               UP_KEY_DOWN: LookAboveRunState, UP_KEY_UP: LookAboveRunState,
               A_KEY_DOWN: RunState, S_KEY_DOWN: RunState, D_KEY_DOWN: RunState,
               Q_KEY_DOWN: RunState, E_KEY_DOWN: RunState},

    SitState: {RIGHT_KEY_DOWN: CrawlState, RIGHT_KEY_UP: CrawlState,
               LEFT_KEY_DOWN: CrawlState, LEFT_KEY_UP: CrawlState,
               DOWN_KEY_DOWN: IdleState, DOWN_KEY_UP: IdleState,
               UP_KEY_DOWN: IdleState, UP_KEY_UP: IdleState,
               A_KEY_DOWN: SitState, S_KEY_DOWN: SitState, D_KEY_DOWN: SitState,
               Q_KEY_DOWN: SitState, E_KEY_DOWN: SitState},

    CrawlState: {RIGHT_KEY_DOWN: SitState, RIGHT_KEY_UP: SitState,
                 LEFT_KEY_DOWN: SitState, LEFT_KEY_UP: SitState,
                 DOWN_KEY_DOWN: RunState, DOWN_KEY_UP: RunState,
                 UP_KEY_DOWN: RunState, UP_KEY_UP: RunState,
                 A_KEY_DOWN: CrawlState, S_KEY_DOWN: CrawlState, D_KEY_DOWN: CrawlState,
                 Q_KEY_DOWN: CrawlState, E_KEY_DOWN: CrawlState},

    LookAboveState: {RIGHT_KEY_DOWN: LookAboveRunState, RIGHT_KEY_UP: LookAboveRunState,
                     LEFT_KEY_DOWN: LookAboveRunState, LEFT_KEY_UP: LookAboveRunState,
                     DOWN_KEY_DOWN: IdleState, DOWN_KEY_UP: IdleState,
                     UP_KEY_DOWN: IdleState, UP_KEY_UP: IdleState,
                     A_KEY_DOWN: LookAboveState, S_KEY_DOWN: LookAboveState, D_KEY_DOWN: LookAboveState,
                     Q_KEY_DOWN: LookAboveState, E_KEY_DOWN: LookAboveState},

    LookAboveRunState: {RIGHT_KEY_DOWN: LookAboveState, RIGHT_KEY_UP: LookAboveState,
                        LEFT_KEY_DOWN: LookAboveState, LEFT_KEY_UP: LookAboveState,
                        DOWN_KEY_DOWN: RunState, DOWN_KEY_UP: RunState,
                        UP_KEY_DOWN: RunState, UP_KEY_UP: RunState,
                        A_KEY_DOWN: LookAboveRunState, S_KEY_DOWN: LookAboveRunState, D_KEY_DOWN: LookAboveRunState,
                        Q_KEY_DOWN: LookAboveRunState, E_KEY_DOWN: LookAboveRunState}
}


class Player:

    def __init__(self):
        self.x, self.y = 200, 90
        self.image = load_image('animation_sheet.png')
        self.frame = 0
        self.fy = 2
        self.direction = 1
        self.velocity = 0
        self.jumping, self.jump_y, self.jump_count, self.sit_y = 0, 0, 0, 0
        self.weapon = PISTOL
        self.shoot_delay = 0
        self.is_above = False

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        self.shoot_delay -= 1

    def draw(self):
        self.cur_state.draw(self)

    def shoot(self):
        if self.weapon == PISTOL:
            if Pistol.max_pistol < 4:
                bullet = Pistol(self.x, self.y + self.jump_y + self.sit_y + 10, self.direction,
                                self.is_above)
                game_world.add_object(bullet, 1)
                Pistol.max_pistol += 1
        elif self.weapon == MACHINE_GUN and self.shoot_delay < 0:
            if not self.is_above:
                bullet = [Machine_gun(self.x, self.y+self.jump_y+random.randint(-10, 10) + 10 +
                                      self.sit_y, self.direction, i*20, self.is_above) for i in range(4)]
            else:
                bullet = [Machine_gun(self.x+random.randint(-10, 10), self.y + self.jump_y + 50 +
                                      self.sit_y, self.direction, i * 20, self.is_above) for i in range(4)]
            for i in range(4):
                game_world.add_object(bullet[i], 1)
            self.shoot_delay = 55

    def throw(self):
        if Grenade.max_grenade < 2:
            grenade = Grenade(self.x, self.y + self.jump_y, self.direction, self.velocity)
            game_world.add_object(grenade, 1)
            Grenade.max_grenade += 1

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
