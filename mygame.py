import os
import sys
import pygame
import datetime
import pyganim
from random import randint

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

player = None
all_sprites = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
enemies = pygame.sprite.Group()

left = right = False
up = False
hit_second = False
score = 0
ending_flag = False


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def glitch():
    text_font = pygame.font.Font('data/19888.ttf', 40)

    text_image = text_font.render('Управление: WASD - стримерская платформа, '
                                  'Пробел - удар', True, pygame.Color('#9999b0'))
    text_width = text_image.get_width()
    text_height = text_image.get_height()

    text_x = WIDTH - text_width - 20
    text_y = HEIGHT - text_height - 20
    fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(text_image, (text_x, text_y))
    pygame.display.flip()
    pygame.time.wait(randint(1000, 3000))
    fon = pygame.transform.scale(load_image('fon1.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(text_image, (text_x, text_y))
    pygame.display.flip()
    pygame.time.wait(100)
    fon = pygame.transform.scale(load_image('fon_pomehi.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(text_image, (text_x, text_y))
    pygame.display.flip()
    pygame.time.wait(100)
    fon = pygame.transform.scale(load_image('fon2.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(text_image, (text_x, text_y))


def start_screen():
    glitch()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        glitch()

        return


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


animation_fire = [load_image('fire/Fire-Wrath__11.png', -1),
                  load_image('fire/Fire-Wrath__12.png', -1),
                  load_image('fire/Fire-Wrath__13.png', -1),
                  load_image('fire/Fire-Wrath__14.png', -1),
                  load_image('fire/Fire-Wrath__15.png', -1)]

animation_enemy = [load_image('enemy/BeetleMove1.png', -1),
                   load_image('enemy/BeetleMove2.png', -1),
                   load_image('enemy/BeetleMove3.png', -1),
                   load_image('enemy/BeetleMove4.png', -1)]

animation_enemy_bullet = [load_image('enemy_bullet/BeetleMove1.png', -1),
                          load_image('enemy_bullet/BeetleMove2.png', -1),
                          load_image('enemy_bullet/BeetleMove3.png', -1),
                          load_image('enemy_bullet/BeetleMove4.png', -1)]

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

animation_glitch = [load_image('glitch/glitch1.jpg', -1),
                    load_image('glitch/glitch2.jpg', -1),
                    load_image('glitch/glitch3.jpg', -1),
                    load_image('glitch/glitch4.jpg', -1)]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tile_images['wall'][randint(0, 4)]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.start_x = pos_x
        self.start_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
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

    def update(self, left, right, up, platforms, hit):
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
        self.collide(0, self.velocity_y, platforms)
        self.rect.x += self.velocity_x
        self.collide(self.velocity_x, 0, platforms)

    def hit_update(self, hit):
        if hit and self.velocity_x > 0:
            timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=0.3)
            print('signal1')
            return timer_stop
        if hit and self.velocity_x < 0:
            timer_stop = datetime.datetime.utcnow() + datetime.timedelta(seconds=0.3)
            print('signal2')
            return timer_stop
        else:
            self.velocity_hit = 0
            return 0

    def die(self):
        global score
        score = 0
        pygame.time.wait(500)
        for i in all_sprites:
            if not isinstance(i, Platform):
                i.teleportation_start()

    def collide(self, velocity_x, velocity_y, platforms):
        global ending_flag
        for i in platforms:
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
                if (isinstance(i, BlockDie) or isinstance(i, Enemy) or isinstance(i, Enemy_red)
                    or isinstance(i, Enemy_mantis) or isinstance(i, Bullet)) and not hit_second:
                    self.die()
                elif isinstance(i, Ending):
                    ending_flag = True

    def teleportation_start(self):
        self.rect.x = tile_width * self.start_x + 15
        self.rect.y = tile_height * self.start_y + 5


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = tile_images['die_block']
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)
        fire_frames = []
        for i in animation_fire:
            fire_frames.append((i, 100))
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
        self.rect = pygame.Rect(x, y, 50, 50)
        self.start_x = tile_width * x + 15
        self.start_y = tile_height * y + 5
        self.max_left = maxleft
        self.max_up = maxup
        self.velocity_x = left
        self.velocity_y = up
        self.rect = self.image.get_rect().move(self.start_x, self.start_y)

        animation_frames = []
        for i in animation_enemy:
            animation_frames.append((i, 100))
        self.animation_enemy_play = pyganim.PygAnimation(animation_frames)
        self.animation_enemy_play.play()

    def update(self, platforms):

        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_enemy_play.blit(self.image, (0, 0))

        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        self.collide(platforms)

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.velocity_x = -self.velocity_x
        if abs(self.start_y - self.rect.y) > self.max_left:
            self.velocity_y = -self.velocity_y

    def collide(self, platforms):
        global score
        for i in platforms:
            if pygame.sprite.collide_rect(self, hero) and hit_second:
                print('enemy_die')
                score += 1
                print(score)
                self.rect.x = 3000
                self.rect.y = 3000
            elif pygame.sprite.collide_rect(self, i) and self != i:
                self.velocity_x = - self.velocity_x
                self.velocity_y = - self.velocity_y

    def teleportation_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class Enemy_red(pygame.sprite.Sprite):
    def __init__(self, x, y, left, up, maxleft, maxup):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy_bullet/BeetleMove1.png', -1)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.start_x = tile_width * x + 15
        self.start_y = tile_height * y + 5
        self.max_left = maxleft
        self.max_up = maxup
        self.velocity_x = left
        self.velocity_y = up
        self.rect = self.image.get_rect().move(self.start_x, self.start_y)

        animation_frames = []
        for i in animation_enemy_bullet:
            animation_frames.append((i, 100))
        self.animation_enemy_play = pyganim.PygAnimation(animation_frames)
        self.animation_enemy_play.play()
        self.lives = 1000

    def update(self, platforms):

        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_enemy_play.blit(self.image, (0, 0))

        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        self.collide(platforms)

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.velocity_x = -self.velocity_x
        if abs(self.start_y - self.rect.y) > self.max_left:
            self.velocity_y = -self.velocity_y

    def collide(self, platforms):
        global score
        for i in platforms:
            if pygame.sprite.collide_rect(self, hero) and hit_second:
                if self.lives:
                    print('live')
                    self.lives -= 1
                elif self.lives <= 0:
                    score += 2
                    print('enemy_die')
                    self.rect.x = 3000
                    self.rect.y = 3000
            elif pygame.sprite.collide_rect(self, i) and self != i:
                self.velocity_x = - self.velocity_x
                self.velocity_y = - self.velocity_y

    def teleportation_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class Enemy_mantis(pygame.sprite.Sprite):
    def __init__(self, x, y, left, maxleft):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('enemy_mantis/right/MantisMove1.png', -1)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.start_x = tile_width * x + 15
        self.start_y = tile_height * y + 5
        self.max_left = maxleft
        self.velocity_x = left
        self.velocity_y = 0
        self.ground = False
        self.shot_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=randint(3, 6))
        self.rect = self.image.get_rect().move(self.start_x, self.start_y)

        animation_frames = []
        for i in animation_enemy_mantis_left:
            animation_frames.append((i, 100))
        self.animation_enemy_mantis_left_play = pyganim.PygAnimation(animation_frames)
        self.animation_enemy_mantis_left_play.play()

    def shot(self):
        bullet = Bullet(self.rect.x, self.rect.y, randint(-10, 10), randint(-10, 10))
        all_sprites.add(bullet)
        enemies.add(bullet)
        platforms_list.append(bullet)

    def update(self, platforms):
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_enemy_mantis_left_play.blit(self.image, (0, 0))

        if self.ground:
            self.velocity_y += GRAVITY

        if abs(self.start_x - self.rect.x) > self.max_left:
            self.velocity_x = -self.velocity_x

        if datetime.datetime.utcnow() > self.shot_time:
            self.shot()
            self.shot_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=randint(3, 6))

        self.ground = False
        self.rect.y += self.velocity_y
        self.collide(self.velocity_y, platforms)
        self.rect.x += self.velocity_x
        self.collide(0, platforms)

    def collide(self, velocity_y, platforms):
        global score
        if pygame.sprite.collide_rect(self, hero) and hit_second:
            print('enemy_die')
            score += 3
            self.rect.x = 3000
            self.rect.y = 3000
        for i in platforms:
            if velocity_y > 0:
                self.rect.bottom = i.rect.top
                self.ground = True
                self.velocity_y = 0
            elif pygame.sprite.collide_rect(self, i) and self != i:
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
            animation_frames.append((i, 100))
        self.animation_bullet_play = pyganim.PygAnimation(animation_frames)
        self.animation_bullet_play.play()

    def update(self, platforms):
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_bullet_play.blit(self.image, (0, 0))
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.collide(platforms)

    def collide(self, platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i) and self != i and not isinstance(i, Enemy_mantis):
                self.rect.x = 3000
                self.rect.y = 3000
                self.kill()

    def teleportation_start(self):
        self.kill()


class Ending(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('glitch/glitch1.jpg', -1)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height

        animation_frames = []
        for i in animation_glitch:
            animation_frames.append((i, 100))
        self.animation_glitch_play = pyganim.PygAnimation(animation_frames)
        self.animation_glitch_play.play()

    def update(self):
        self.image.fill(pygame.Color(BACKGROUND_COLOR))
        self.animation_glitch_play.blit(self.image, (0, 0))


class Button:
    def __init__(self, x, y):
        self.text_image = pygame.font.Font('data/19888.ttf', 40).render('QUIT', True, pygame.Color('white'))
        self.text_x = WIDTH + x
        self.text_y = HEIGHT + y
        self.rect = pygame.Rect(self.text_x, self.text_y, 50, 50)

    def collide(self, mouse):
        if self.rect.collidepoint(mouse):
            terminate()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                platform = Platform(x, y)
                all_sprites.add(platform)
                platforms_list.append(platform)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '*':
                die_block = BlockDie(x, y)
                all_sprites.add(die_block)
                platforms_list.append(die_block)
                animatedEntities.add(die_block)
            elif level[y][x] == '$':
                enemy = Enemy(x, y, 2, 3, 200, 20)
                all_sprites.add(enemy)
                platforms_list.append(enemy)
                enemies.add(enemy)
            elif level[y][x] == '%':
                enemy = Enemy_red(x, y, 2, 3, 200, 20)
                all_sprites.add(enemy)
                platforms_list.append(enemy)
                enemies.add(enemy)
            elif level[y][x] == '!':
                enemy = Enemy_mantis(x, y, 2, 200)
                all_sprites.add(enemy)
                platforms_list.append(enemy)
                enemies.add(enemy)
            elif level[y][x] == '&':
                ending = Ending(x, y)
                animatedEntities.add(ending)
                platforms_list.append(ending)
    return new_player, x, y


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    a, b, _, _ = target_rect
    _, _, w, h = camera
    a, b = -a + WIDTH / 2, -b + HEIGHT / 2

    a = min(0, a)
    a = max(-(camera.width - WIDTH), a)
    b = max(-(camera.height - HEIGHT), b)
    b = min(0, b)

    return pygame.Rect(a, b, w, h)


tile_images = {'wall': [load_image('box1.png'), load_image('box2.png'), load_image('box3.png'),
                        load_image('box4.png'), load_image('box5.png')],
               'die_block': load_image('fire/Fire-Wrath__11.png', -1)}
player_image = load_image('Knight/afk/noBKG_KnightIdle_strip1.png', -1)
tile_width = tile_height = 50
bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill(pygame.Color(BACKGROUND_COLOR))

start_screen()

hero = Player(55, 55)
platforms_list = []
hero, level_x, level_y = generate_level(load_level('levelex.txt'))
all_sprites.add(hero)
total_level_width = len(load_level('levelex.txt')[0]) * WIDTH
total_level_height = len(load_level('levelex.txt')) * HEIGHT
button = Button(-150, -100)
camera = Camera(camera_configure, total_level_width, total_level_height)
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
            if hit_second:
                None
            else:
                hit_second = True
                st_hit = hero.hit_update(hit_second)
                print('keydown')
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            button.collide(mouse_pos)

    text_font = pygame.font.Font('data/19888.ttf', 40)
    text_image = text_font.render(str(score), True, pygame.Color('white'))
    text_width = text_image.get_width()
    text_x = WIDTH - text_width - 30
    text_y = 30

    enemies.update(platforms_list)
    animatedEntities.update()
    camera.update(hero)
    if hit_second:
        if datetime.datetime.utcnow() > st_hit:
            hit_second = False
            print('stop')
    hero.update(left, right, up, platforms_list, hit_second)

    screen.fill(pygame.Color(0, 0, 0))
    screen.blit(bg, (0, 0))
    for sp in all_sprites:
        screen.blit(sp.image, camera.apply(sp))
    screen.blit(text_image, (text_x, text_y))
    screen.blit(button.text_image, (button.text_x, button.text_y))
    if ending_flag:
        fon = pygame.transform.scale(load_image('fon_ending2.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        pygame.time.wait(randint(1000, 5000))
        fon = pygame.transform.scale(load_image('fon_ending1.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)
        fon = pygame.transform.scale(load_image('fon_ending_pomehi1.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)
        fon = pygame.transform.scale(load_image('fon_ending_pomehi2.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        pygame.time.wait(100)
        fon = pygame.transform.scale(load_image('fon_ending_2.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

terminate()
