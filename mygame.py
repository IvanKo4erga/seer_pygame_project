import pygame
import datetime
import pyganim
from random import randint
from loads import load_level, terminate, load_image

pygame.init()

FPS = 30
WIDTH = 1920
HEIGHT = 1080
STEP = 10
JUMP = 14
GRAVITY = 0.35
HIT = 20
BACKGROUND_COLOR = '#78788f'
ANIMATION_DELAY = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
fires = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bg = pygame.Surface((WIDTH, HEIGHT))

player = None
left = right = False
up = False
hit_second = False
invuln = False
score = 0
ending_flag = False

animation_fire = [load_image('fire/Fire-Wrath__11.png', -1),
                  load_image('fire/Fire-Wrath__12.png', -1),
                  load_image('fire/Fire-Wrath__13.png', -1),
                  load_image('fire/Fire-Wrath__14.png', -1),
                  load_image('fire/Fire-Wrath__15.png', -1)]

animation_enemy = [load_image('enemy/BeetleMove1.png', -1),
                   load_image('enemy/BeetleMove2.png', -1),
                   load_image('enemy/BeetleMove3.png', -1),
                   load_image('enemy/BeetleMove4.png', -1)]

animation_enemy_mantis_left = [load_image('enemy_mantis/left/MantisMove1.png', -1),
                               load_image('enemy_mantis/left/MantisMove2.png', -1),
                               load_image('enemy_mantis/left/MantisMove3.png', -1),
                               load_image('enemy_mantis/left/MantisMove4.png', -1)]

animation_bullet = [load_image('bullet/AcidBlob1.png', -1),
                    load_image('bullet/AcidBlob2.png', -1),
                    load_image('bullet/AcidBlob3.png', -1),
                    load_image('bullet/AcidBlob4.png', -1)]

animation_hero_afk = [load_image('Knight/afk/noBKG_KnightIdle_strip1.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip2.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip3.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip4.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip5.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip6.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip7.png', -1),
                      load_image('Knight/afk/noBKG_KnightIdle_strip8.png', -1)]

animation_hero_right = [load_image('Knight/run/right/noBKG_KnightRun_strip_right1.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right2.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right3.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right4.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right5.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right6.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right7.png', -1),
                        load_image('Knight/run/right/noBKG_KnightRun_strip_right8.png', -1), ]

animation_hero_left = [load_image('Knight/run/left/noBKG_KnightRun_strip_left1.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left2.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left3.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left4.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left5.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left6.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left7.png', -1),
                       load_image('Knight/run/left/noBKG_KnightRun_strip_left8.png', -1), ]

animation_hero_jump_right = [load_image('Knight/noBKG_KnightJumpAndFall_right.png', -1),
                             load_image('Knight/noBKG_KnightJumpAndFall_right.png', -1)]
animation_hero_jump_left = [load_image('Knight/noBKG_KnightJumpAndFall_left.png', -1),
                            load_image('Knight/noBKG_KnightJumpAndFall_left.png', -1)]

# animation_glitch = [load_image('glitch/glitch1.jpg', -1),
#                     load_image('glitch/glitch2.jpg', -1),
#                     load_image('glitch/glitch3.jpg', -1),
#                     load_image('glitch/glitch4.jpg', -1)]

tile_images = {'wall': [load_image('box1.png'), load_image('box2.png'), load_image('box3.png'),
                        load_image('box4.png'), load_image('box5.png')],
               'fire': load_image('fire/Fire-Wrath__11.png', -1)}
player_image = load_image('Knight/afk/noBKG_KnightIdle_strip1.png', -1)

TILE_W = TILE_H = 50

all_sprites_list = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                platform = Platform(x, y)
                all_sprites.add(platform)
                all_sprites_list.append(platform)
            elif level[y][x] == '@':
                new_player = Player(x, y)
                all_sprites.add(new_player)
            elif level[y][x] == '*':
                fire = Fire(x, y)
                all_sprites.add(fire)
                all_sprites_list.append(fire)
                fires.add(fire)
            elif level[y][x] == '$':
                enemy = Enemy(x, y, 2, 3, 200, 20)
                all_sprites.add(enemy)
                all_sprites_list.append(enemy)
                enemies.add(enemy)
            elif level[y][x] == '!':
                enemy = Enemy_mantis(x, y, 2, 200)
                all_sprites.add(enemy)
                all_sprites_list.append(enemy)
                enemies.add(enemy)
            elif level[y][x] == '&':
                ending = Ending(x, y)
                all_sprites.add(ending)
                # fires.add(ending)
                all_sprites_list.append(ending)
    return new_player, x, y


def camera_configure(camera, target_rect):
    x, y, _, _ = target_rect
    _, _, w, h = camera
    screen_center_x, screen_center_y = -(x - (WIDTH / 2)), -(y - (HEIGHT / 2))
    x1 = -(camera.width - WIDTH) - 190
    y1 = -(camera.height - HEIGHT) - 108

    if screen_center_x > 190:
        screen_center_x = 190
    if screen_center_y > 108:
        screen_center_y = 108
    if screen_center_x < x1:
        screen_center_x = x1
    if screen_center_y < y1:
        screen_center_y = y1

    return pygame.Rect(screen_center_x, screen_center_y, w, h)


def start_s():
    text_font = pygame.font.Font('data/19888.ttf', 30)

    text_image = text_font.render('Управление: (стримерская платформа) WASD — клавиши передвижения , ', True,
                                  pygame.Color('#9999b0'))
    text3_image = text_font.render('Пробел — рывок-удар', True, pygame.Color('#9999b0'))
    text2_image = text_font.render('Нажмите любую кнопку, чтобы начать', True, pygame.Color('#9999b0'))
    text_width = text_image.get_width()
    text_height = text_image.get_height()
    text2_width = text2_image.get_width()
    text2_height = text2_image.get_height()
    text3_width = text3_image.get_width()
    text3_height = text3_image.get_height()

    text_x = WIDTH - text_width - 300
    text_y = HEIGHT - text_height - 500
    text2_x = WIDTH - text2_width - 300
    text2_y = HEIGHT - text2_height - 300
    text3_x = WIDTH - text3_width - 300
    text3_y = HEIGHT - text3_height - 400

    screen.blit(text_image, (text_x, text_y))
    screen.blit(text2_image, (text2_x, text2_y))
    screen.blit(text3_image, (text3_x, text3_y))
    pygame.display.flip()
    # pygame.time.wait(1000)
    # fon = pygame.transform.scale(load_image('fon1.png'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # screen.blit(text_image, (text_x, text_y))
    # pygame.display.flip()
    # pygame.time.wait(100)
    # fon = pygame.transform.scale(load_image('fon_pomehi.png'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # screen.blit(text_image, (text_x, text_y))
    # pygame.display.flip()
    # pygame.time.wait(100)
    # fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # screen.blit(text_image, (text_x, text_y))


def start_screen():
    start_s()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        start_s()


# class Tile(pygame.sprite.Sprite):
#     def __init__(self, tile_type, pos_x, pos_y):
#         super().__init__(all_sprites)
#         self.image = tile_images[tile_type]
#         self.rect = self.image.get_rect().move(
#             TILE_W * pos_x, TILE_H * pos_y)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tile_images['wall'][randint(0, 4)]
        self.rect = self.image.get_rect().move(
            TILE_W * pos_x, TILE_H * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)  # Добавление нового спрайта в группу всех спрайтов
        self.start_x = pos_x
        self.start_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            TILE_W * pos_x + 15, TILE_H * pos_y + 5)
        self.velocity_y = 0
        self.velocity_x = 0
        self.velocity_hit = 0
        self.ground = False

        animation_frames = []
        for i in animation_hero_afk:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_afk = pyganim.PygAnimation(animation_frames)
        self.animation_afk.play()

        animation_frames = []
        for i in animation_hero_right:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_right = pyganim.PygAnimation(animation_frames)
        self.animation_right.play()

        animation_frames = []
        for i in animation_hero_left:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_left = pyganim.PygAnimation(animation_frames)
        self.animation_left.play()

        animation_frames = []
        for i in animation_hero_jump_left:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_hero_jump_left_play = pyganim.PygAnimation(animation_frames)
        self.animation_hero_jump_left_play.play()

        animation_frames = []
        for i in animation_hero_jump_right:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_hero_jump_right_play = pyganim.PygAnimation(animation_frames)
        self.animation_hero_jump_right_play.play()

    def update(self, left, right, up, collided, hit):
        if left:
            if hit:
                self.velocity_x = -HIT
            else:
                self.velocity_x = -STEP
                if up:
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_hero_jump_left_play.blit(self.image, (0, 0))
                else:
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_left.blit(self.image, (0, 0))
        if right:
            if hit:
                self.velocity_x = HIT
            else:
                self.velocity_x = STEP
                if up:
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_hero_jump_right_play.blit(self.image, (0, 0))
                else:
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_right.blit(self.image, (0, 0))
        if up:
            if self.ground:
                self.velocity_y = -JUMP

        if not self.ground:
            self.velocity_y += GRAVITY

        if not (left or right):
            self.image.fill(pygame.Color(BACKGROUND_COLOR))
            self.animation_afk.blit(self.image, (0, 0))

        self.ground = False
        self.rect.y += self.velocity_y
        self.collide(0, self.velocity_y, collided)
        self.rect.x += self.velocity_x
        self.collide(self.velocity_x, 0, collided)

    def hit_update(self, hit):
        if hit and self.velocity_x > 0:
            timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=0.3)
            timer_invuln = timer_stop + datetime.timedelta(seconds=1)
            # print('signal1')
            return timer_stop, timer_invuln
        if hit and self.velocity_x < 0:
            timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=0.3)
            timer_invuln = timer_stop + datetime.timedelta(seconds=1)
            # print('signal2')
            return timer_stop, timer_invuln
        else:
            self.velocity_hit = 0
            return 0

    def die(self):
        global score
        score = 0
        pygame.time.wait(500)
        for i in all_sprites:
            if not (isinstance(i, Platform) or isinstance(i, Ending)):
                i.teleportation_start()

    def collide(self, velocity_x, velocity_y, collided):
        global ending_flag
        for i in collided:
            if pygame.sprite.collide_rect(self, i):
                if velocity_x > 0:
                    self.rect.right = i.rect.left
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_afk.blit(self.image, (0, 0))
                if velocity_x < 0:
                    self.rect.left = i.rect.right
                    self.image.fill(pygame.Color(BACKGROUND_COLOR))
                    self.animation_afk.blit(self.image, (0, 0))
                if velocity_y > 0:
                    self.rect.bottom = i.rect.top
                    self.ground = True
                    self.velocity_y = 0
                if velocity_y < 0:
                    self.rect.top = i.rect.bottom
                    self.velocity_y = 0
                if (isinstance(i, Fire) or isinstance(i, Enemy)
                    or isinstance(i, Enemy_mantis) or isinstance(i, Bullet)) and not invuln:
                    self.die()
                elif isinstance(i, Ending):
                    ending_flag = True

    def teleportation_start(self):
        self.rect.x = TILE_W * self.start_x
        self.rect.y = TILE_H * self.start_y


class Fire(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = tile_images['fire']
        self.rect = self.image.get_rect().move(TILE_W * x, TILE_H * y)
        fire_frames = []
        for i in animation_fire:
            fire_frames.append((i, ANIMATION_DELAY))
        self.animation_fire_play = pyganim.PygAnimation(fire_frames)
        self.animation_fire_play.play()
        self.animation_fire_play.blit(self.image, (0, 0))

    def update(self):
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_fire_play.blit(self.image, (0, 0))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, left, up, maxleft, maxup):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy/BeetleMove1.png', -1)
        self.start_x = TILE_W * x + 15
        self.start_y = TILE_H * y + 5
        self.max_left = maxleft
        self.max_up = maxup
        self.velocity_x = left
        self.velocity_y = up
        self.rect = self.image.get_rect().move(self.start_x, self.start_y)

        animation_frames = []
        for i in animation_enemy:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_enemy_play = pyganim.PygAnimation(animation_frames)
        self.animation_enemy_play.play()

    def update(self, collided):

        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_enemy_play.blit(self.image, (0, 0))

        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        self.collide(collided)

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.velocity_x = -self.velocity_x
        if abs(self.start_y - self.rect.y) > self.max_left:
            self.velocity_y = -self.velocity_y

    def collide(self, collided):
        global score
        for i in collided:
            if pygame.sprite.collide_rect(self, hero) and hit_second:
                score += 1
                self.rect.x = 3000
                self.rect.y = 3000
            elif pygame.sprite.collide_rect(self, i) and self != i and not isinstance(i, Bullet):
                self.velocity_x = - self.velocity_x
                self.velocity_y = - self.velocity_y

    def teleportation_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class Enemy_mantis(pygame.sprite.Sprite):
    def __init__(self, x, y, left, maxleft):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy_mantis/right/MantisMove1.png', -1)
        # self.rect = pygame.Rect(x, y, 50, 50)
        self.start_x = TILE_W * x + 15
        self.start_y = TILE_H * y + 5
        self.max_left = maxleft
        self.velocity_x = left
        self.velocity_y = 0
        self.ground = False
        self.shot_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=randint(3, 6))
        self.rect = self.image.get_rect().move(self.start_x, self.start_y)

        animation_frames = []
        for i in animation_enemy_mantis_left:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_enemy_mantis_left_play = pyganim.PygAnimation(animation_frames)
        self.animation_enemy_mantis_left_play.play()

    def shot(self):
        bullet = Bullet(self.rect.x, self.rect.y, randint(-10, 10), randint(-10, 10))
        all_sprites.add(bullet)
        enemies.add(bullet)
        all_sprites_list.append(bullet)

    def update(self, collided):
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_enemy_mantis_left_play.blit(self.image, (0, 0))

        if self.ground:
            self.velocity_y += GRAVITY

        if datetime.datetime.utcnow() > self.shot_time:
            self.shot()
            self.shot_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=randint(3, 6))

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.velocity_x = -self.velocity_x

        self.ground = False
        self.rect.y += self.velocity_y
        self.collide(self.velocity_y, collided)
        self.rect.x += self.velocity_x
        self.collide(0, collided)

    def collide(self, velocity_y, collided):
        global score
        if pygame.sprite.collide_rect(self, hero) and hit_second:
            self.rect.x = 3000
            self.rect.y = 3000
            # print('enemy_die')
            score += 3

        for i in collided:
            if velocity_y > 0:
                self.rect.bottom = i.rect.top
                self.ground = True
                self.velocity_y = 0
            elif pygame.sprite.collide_rect(self, i) and self != i and not isinstance(i, Bullet):
                self.velocity_x = - self.velocity_x

    def teleportation_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('bullet/AcidBlob1.png', -1)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.rect.x = x
        self.rect.y = y

        animation_frames = []
        for i in animation_bullet:
            animation_frames.append((i, ANIMATION_DELAY))
        self.animation_bullet_play = pyganim.PygAnimation(animation_frames)
        self.animation_bullet_play.play()

    def update(self, collided):
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_bullet_play.blit(self.image, (0, 0))
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.collide(collided)

    def collide(self, collided):
        for i in collided:
            if pygame.sprite.collide_rect(self, i) and self != i and not isinstance(i, Enemy_mantis):
                self.kill()

    def teleportation_start(self):
        self.kill()


class Ending(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('exit.png', -1)
        self.rect = self.image.get_rect().move(
            TILE_W * x, TILE_H * y)

        # animation_frames = []
        # for i in animation_exit:
        #     animation_frames.append((i, 100))
        # self.animation_exit_play = pyganim.PygAnimation(animation_frames)
        # self.animation_exit_play.play()

    # def update(self):
    #     self.image.fill(pygame.Color(BACKGROUND_COLOR))
    #     self.animation_exit_play.blit(self.image, (0, 0))


class Button:
    def __init__(self, x, y):
        self.text_image = pygame.font.Font('data/19888.ttf', 40).render('QUIT', True, pygame.Color('white'))
        self.text_x = WIDTH + x
        self.text_y = HEIGHT + y
        self.rect = pygame.Rect(self.text_x, self.text_y, 50, 50)

    def collide(self, mouse):
        if self.rect.collidepoint(mouse):
            terminate()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


hero = Player(55, 55)


def main():
    global hero, all_sprites_list, hit_second, left, right, up, invuln
    bg.fill(pygame.Color(BACKGROUND_COLOR))
    loaded_lvl = load_level('levelex.txt')
    start_screen()
    hero, level_x, level_y = generate_level(loaded_lvl)
    LVL_WIDTH = len(loaded_lvl[0]) * TILE_W
    LVL_HEIGHT = len(loaded_lvl) * TILE_H
    button = Button(-300, -300)
    camera = Camera(camera_configure, LVL_WIDTH, LVL_HEIGHT)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                right = True
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                left = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                up = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not hit_second:
                    hit_second = True
                    invuln = True
                    st_hit = hero.hit_update(hit_second)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button.collide(mouse_pos)
        text_font = pygame.font.Font('data/19888.ttf', 40)
        text_image = text_font.render('Your score: ' + str(score), True, pygame.Color('white'))
        text_width = text_image.get_width()
        text_x = WIDTH - text_width - 200
        text_y = HEIGHT - 200
        enemies.update(all_sprites_list)
        fires.update()
        camera.update(hero)
        if hit_second:
            if datetime.datetime.utcnow() > st_hit[0]:
                hit_second = False
        if invuln:
            if datetime.datetime.utcnow() > st_hit[1]:
                invuln = False
        hero.update(left, right, up, all_sprites_list, hit_second)
        screen.fill(pygame.Color(0, 0, 0))
        screen.blit(bg, (0, 0))
        for sp in all_sprites:
            screen.blit(sp.image, camera.apply(sp))
        screen.blit(text_image, (text_x, text_y))
        screen.blit(button.text_image, (button.text_x, button.text_y))
        if ending_flag:
            ending_image = pygame.transform.scale(load_image('ending1.png'), (300, 100))
            ending_image.set_alpha(8)
            text_ending_font = pygame.font.Font('data/19888.ttf', 100)
            text_ending_image = text_ending_font.render('You escaped', True, pygame.Color('white'))
            screen.blit(bg, (0, 0))
            screen.blit(text_image, (text_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))))
            screen.blit(text_ending_image, (text_ending_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))))
            screen.blit(ending_image, (ending_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False

        pygame.display.flip()

        clock.tick(FPS)

    terminate()


if __name__ == "__main__":
    main()
