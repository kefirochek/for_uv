import pygame
import sqlite3
import os
import sys
from random import randint
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
size = WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
count = 0
level_global = 0
name_global = ''


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

        # сдвинуть объект obj на смещение камеры

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

        # позиционировать камеру на объекте target

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    # чтоб выйти
    pygame.quit()
    sys.exit()


def draw_timer(screen, time_left, lvl=None):
    font = pygame.font.Font(None, 36)
    if lvl:
        if time_left > 15:
            end_screen(5, 'scary')
        text = font.render("У тебя 15 секунд! "
                           + str(time_left // 60)[:-2] + ':' +
                           str(time_left % 60)[:2],
                           True, (255, 0, 0))
    else:
        if int(time_left) / 59 > 1:
            text = font.render("Time left: " + str(time_left // 60)[:-2]
                               + ':' + str(time_left % 60)[:2], True,
                               (0, 0, 0))
        else:
            text = font.render("Time left: " + '00:' +
                               str(time_left)[:str(time_left).count('.') + 1],
                               True, (0, 0, 0))
    screen.blit(text, (0, 0))


def chet(screen, n):
    global count
    font = pygame.font.Font(None, 30)
    count += len(n)
    text = font.render("Грибочков: " + str(count) + '/5',
                       True, (52, 201, 36))
    screen.blit(text, (850, 470))


def avtoris_sql(name):
    con = sqlite3.connect('platform_fox.db')
    cur = con.cursor()
    proveril_est_li = cur.execute(f'''SELECT * from play
                WHERE user = "{name}"''').fetchall()
    if name != 'Неизвестный':
        if proveril_est_li:
            return (proveril_est_li[0][0], proveril_est_li[0][1], proveril_est_li[0][2],
                    proveril_est_li[0][3], proveril_est_li[0][4], proveril_est_li[0][5])
        else:
            res = cur.execute(f'''INSERT INTO play VALUES ('{name}', {0}, {0}, {0}, {0}, {0})''')
            con.commit()
            con.close()
            return name, 0, 0, 0, 0, 0
    return name


def update_sql(level):
    global name_global
    con = sqlite3.connect('platform_fox.db')
    cur = con.cursor()
    lv = f'level_{level}'
    res = cur.execute(f'''UPDATE play SET '{lv}' = {1} 
                                WHERE user = '{name_global}' AND user <> "Неизвестный"''')
    con.commit()
    con.close()


def upoad_start_screen(name):
    # name lvl1, lvl2, lvl3, lvl4, lvl5
    all_dann = avtoris_sql(name)
    start_screen(all_dann[0], all_dann[1], all_dann[2], all_dann[3], all_dann[4], all_dann[5])


def start_screen(ttt='Неизвестный', l1=None,
                 l2=None, l3=None, l4=None, l5=None):
    global level_global
    global name_global
    name_global = ttt
    pygame.init()
    proiden_ne_proiden = []
    conteiner = [l1, l2, l3, l4, l5]
    # if l1 or l2 or l3 or l4 or l5:
    if ttt != 'Неизвестный':
        for i in conteiner:
            if i == 1:
                proiden_ne_proiden.append('пройден')
            else:
                proiden_ne_proiden.append('не пройден')
        intro_text = [f"ВЫБЕРИ УРОВЕНЬ, {ttt}",
                      '',
                      'Тут свой ник <3', '', '',
                      f'1 уровень {proiden_ne_proiden[0]}',
                      f'2 уровень {proiden_ne_proiden[1]}',
                      f'3 уровень {proiden_ne_proiden[2]}',
                      f'4 уровень {proiden_ne_proiden[3]}',
                      f'5 уровень {proiden_ne_proiden[4]}']
    else:
        intro_text = [f"ВЫБЕРИ УРОВЕНЬ, {ttt}",
                      '',
                      'Тут свой ник <3', '', '']

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(10, 160, 100, 50)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    fon = pygame.transform.scale(load_image('i.webp'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Times New Romance', 50)
    text_coord = 25
    text_coord_2 = 450
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    button = Button(
        screen, 780, 50,
        200, 50, text='1',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(104, 205, 50),  # Colour of button when not being interacted with
        hoverColour=(31, 64, 55),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )

    button2 = Button(
        screen, 780, 120,
        200, 50, text='2',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(131, 204, 203),  # Colour of button when not being interacted with
        hoverColour=(31, 64, 55),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )
    button3 = Button(
        screen, 780, 190,
        200, 50, text='3',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(226, 128, 144),  # Colour of button when not being interacted with
        hoverColour=(31, 64, 55),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )
    button4 = Button(
        screen, 780, 260,
        200, 50, text='4',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(123, 104, 238),  # Colour of button when not being interacted with
        hoverColour=(31, 64, 55),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )
    button5 = Button(
        screen, 780, 330,
        200, 50, text='5',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(89, 53, 21),  # Colour of button when not being interacted with
        hoverColour=(31, 64, 55),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )
    button_ok = Button(
        screen, 120, 160,
        50, 50, text='ok',
        fontSize=50,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(pygame.Color('chartreuse4')),  # Colour of button when not being interacted with
        hoverColour=(pygame.Color('lightskyblue3')),  # Colour of button when being hovered over
        pressedColour=(pygame.Color('lightskyblue3')),  # Colour of button when being clicked
        radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
    )

    if proiden_ne_proiden.count('пройден') == 5:
        button209 = Button(
            screen, 780, 420,
            200, 50, text='209',
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(135, 169, 107),  # Colour of button when not being interacted with
            hoverColour=(209, 180, 123),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
        )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 780 < pygame.mouse.get_pos()[0] < 980 and 50 < pygame.mouse.get_pos()[1] < 100:
                    level_global = 1
                    return '1lvl'
                elif 780 < pygame.mouse.get_pos()[0] < 980 and 120 < pygame.mouse.get_pos()[1] < 170:
                    level_global = 2
                    return '2lvl'
                elif 780 < pygame.mouse.get_pos()[0] < 980 and 190 < pygame.mouse.get_pos()[1] < 240:
                    level_global = 3
                    return '3lvl'
                elif 780 < pygame.mouse.get_pos()[0] < 980 and 260 < pygame.mouse.get_pos()[1] < 310:
                    level_global = 4
                    return '4lvl'
                elif 780 < pygame.mouse.get_pos()[0] < 980 and 330 < pygame.mouse.get_pos()[1] < 380:
                    level_global = 5
                    return '5lvl'
                elif 780 < pygame.mouse.get_pos()[0] < 980 and 420 < pygame.mouse.get_pos()[1] < 470:
                    level_global = 5
                    return '209lvl'
                elif 120 < pygame.mouse.get_pos()[0] < 170 and 160 < pygame.mouse.get_pos()[1] < 210:
                    upoad_start_screen(user_text)

        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)


def end_screen(count_grib, lvl=None):
    global level_global
    f = True
    if lvl == 'scary':
        intro_text = ["DEAD"]
        button = Button(
            screen, 650, 350,
            300, 100, text='выйти',
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=('red'),  # Colour of button when not being interacted with
            hoverColour=(31, 64, 55),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
        )
        fon = pygame.transform.scale(load_image('4lvl_sc.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 100)
        text_coord = 0
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 650 < pygame.mouse.get_pos()[0] < 950 and 350 < pygame.mouse.get_pos()[1] < 450:
                        terminate()
            pygame_widgets.update(pygame.event.get())  # Call once every loop to allow widgets to render and listen
            pygame.display.update()
            pygame.display.flip()
            clock.tick(30)
    if count_grib != 5:
        f = False
    if f:
        update_sql(level_global)
        intro_text = ["КОНЕЦ ИГРЫ",
                      'Умничка:3']
        button = Button(
            screen, 650, 350,
            300, 100, text='выйти',
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(107, 156, 184),  # Colour of button when not being interacted with
            hoverColour=(31, 64, 55),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
        )
        fon = pygame.transform.scale(load_image('i2.png'), (WIDTH, HEIGHT))
    else:
        intro_text = ["КОНЕЦ ИГРЫ",
                      f'Собрано {count_grib} из 5 грибочков',
                      'ты не молодец!!!']
        button = Button(
            screen, 650, 350,
            300, 100, text='выйти',
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(107, 156, 184),  # Colour of button when not being interacted with
            hoverColour=(31, 64, 55),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=0  # Radius of border corners (leave empty for not curved)  # Function to call when clicked on
        )
        fon = pygame.transform.scale(load_image('fon_end2.jpg'), (WIDTH, HEIGHT))
    # занести в таблицк
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(253, 217, 181))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 650 < pygame.mouse.get_pos()[0] < 950 and 350 < pygame.mouse.get_pos()[1] < 450:
                    terminate()
        pygame_widgets.update(pygame.event.get())  # Call once every loop to allow widgets to render and listen
        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)


class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self):
        super().__init__()
        self.image = load_image('gg.png')
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.count_grib = 0

    def update(self):
        # В этой функции мы передвигаем игрока
        # Сперва устанавливаем для него гравитацию
        self.calc_grav()
        self.rect.x += self.change_x

        # Следим ударяем ли мы какой-то другой объект, платформы, например
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        lais_kill = pygame.sprite.spritecollide(self, self.level.lais_sprite, True)
        if lais_kill:
            end_screen(self.count_grib)
        mushhhh_kill = pygame.sprite.spritecollide(self, self.level.mushroom, True)
        if mushhhh_kill:
            self.count_grib += 1
            chet(screen, [len(mushhhh_kill)])
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self,
                                                        self.level.platform_list, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.change_y = -16

    # Передвижение игрока
    def go_left(self):
        self.change_x = -9  # Двигаем игрока по Х
        if (self.right):
            self.flip()
            self.right = False

    def go_right(self):
        self.change_x = 9
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        self.change_x = 0

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('w22.png')
        self.rect = self.image.get_rect()


class Win(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('kitti.png')
        self.rect = self.image.get_rect()


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = load_image('mmm.png')
        self.rect = self.image.get_rect()


def name_fon(name_file):
    name_file = name_file + '.txt'
    filename = "data/" + name_file
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class Level(object):
    def __init__(self, player, info):
        self.fon = load_image(info[0])
        self.platform_list = pygame.sprite.Group()
        self.lais_sprite = pygame.sprite.Group()
        self.mushroom = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.lais_sprite.update()
        self.mushroom.update()

    def draw(self, screen):
        screen.blit(self.fon, (0, 0))
        self.platform_list.draw(screen)
        self.lais_sprite.draw(screen)
        self.mushroom.draw(screen)


class Level_0X(Level):
    def __init__(self, player, info):
        # Вызываем родительский конструктор
        Level.__init__(self, player, info)
        level = []
        list_mush = []
        max_x, min_y = 0, 100000
        for i in range(2, len(info)):
            first, second = int(info[i].split(';')[0]), int(info[i].split(';')[1])
            level.append([0, 0, int(first), int(second)])
            if first > max_x or second < min_y:
                max_x, min_y = first, second
        lais = Win(0, 0)
        lais.rect.x = int(max_x)
        lais.rect.y = int(min_y - 50)
        lais.player = self.player
        self.lais_sprite.add(lais)
        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # грибочки
        for i in range(5):
            xxx = randint(1, 990)
            yyy = randint(30, 480)
            list_mush.append([0, 0, xxx, yyy])
        for mush in list_mush:
            grib = Mushroom(mush[0], mush[1])
            grib.rect.x = mush[2]
            grib.rect.y = mush[3]
            grib.player = self.player
            self.mushroom.add(grib)


def main():
    a = start_screen()
    info = name_fon(a)
    pygame.init()
    size = [WIDTH, HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("платформер про лису???")
    player = Player()
    level_list = []
    level_list.append(Level_0X(player, info))
    # Устанавливаем текущий уровень
    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 250
    running = True
    player.rect.y = HEIGHT - player.rect.height
    active_sprite_list.add(player)
    pygame.mixer.init()
    pygame.mixer.music.load('data/' + info[1])
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    camera = Camera()
    start_ticks = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if a == '4lvl':
            draw_timer(screen, seconds, 'scary')
            pygame.mixer.music.set_volume(1)
        else:
            draw_timer(screen, seconds)
        chet(screen, [])
        pygame.display.update()
        camera.update(player)
        active_sprite_list.update()
        current_level.update()
        # Если игрок приблизится к правой стороне, то дальше его не двигаем
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        # Если игрок приблизится к левой стороне, то дальше его не двигаем
        if player.rect.left < 0:
            player.rect.left = 0
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(30)
        pygame.display.flip()
    terminate()


name = '__main__'
if name == '__main__':
    main()
