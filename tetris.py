
import pygame  # https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
import random
from sys import exit
from high_score import high_score

# alla färg av figur
from input_box import InputBox


class Figure:
    """Class Figure"""
    x = 0  # figur x position
    y = 0  # figur y position
    # definera alla type and rotation of figur och spara i en list
    # alla figur ligger in fyrakantan 4*4
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # lika I
        [[4, 5, 9, 10], [2, 6, 5, 9]],  #
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # lika Z
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # lika J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # lika L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # lika T
        [[1, 2, 5, 6]],  # lika O
    ]

    def __init__(self, x, y):
        """initera en figur"""
        self.x = x
        self.y = y
        self.colors = [
            (0, 0, 0),
            (120, 37, 179),
            (100, 179, 179),
            (80, 34, 22),
            (80, 134, 22),
            (180, 34, 22),
            (180, 34, 122),
        ]
        self.type = random.randint(0, len(self.figures) - 1)  # valjer random figur from figures listan
        self.color = random.randint(1, len(self.colors) - 1)  # väljer random färg from colors listan
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]  # välja en figur

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])  # rotation


class Tetris:
    level: float  # controlera hur snabb figur ska flytta ner
    score: int
    active: bool
    field: list
    height: int
    width: int
    x: int
    y: int
    zoom: int  # hur stor av fyrakantan  in kraftnät och figur ska bli.
    figure: Figure
    block_list: list

    def __init__(self, height, width):
        self.figure = Figure(5, 0)
        """ Skapa en teris """
        self.height = height  # hög av Teris skäm
        self.width = width  # lengd av Teris skäm
        self.field = []  # list för att kolla om hur fingurer har fyller på skäm
        self.score = 0  # spare påäng
        self.active = True  # status
        self.x = 60
        self.y = 38
        self.level = 1.5
        self.zoom = 20
        self.game_over = False
        self.bg_sound_rotate = pygame.mixer.Sound('Tetris_folder/audio/rotate.mp3')
        self.bg_sound_drop = pygame.mixer.Sound('Tetris_folder/audio/drop.mp3')
        self.bg_sound_line = pygame.mixer.Sound('Tetris_folder/audio/line.mp3')
        self.bg_sound_rotate.set_volume(0.2)
        self.bg_sound_line.set_volume(0.2)
        self.bg_sound_drop.set_volume(0.2)
        self.block_list = [Figure(5, 0)]

        # skapa alla värde av field lika med 0
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        """ Skapa en new figur"""
        self.block_list.append(Figure(5, 0))
        self.figure = self.block_list.pop(0)

    def intersects(self):
        """ kolla om figur får röra sig """
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    # kolla om figur får flytta sig, vänser, höger, upper och nedan
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        """ Ta bort alla lines som har filler upp av figur"""
        lines = 0  # rakna hur många råder ska ta bort
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:  # kolla om field[i][j] int har fyllt
                    zeros += 1
            if zeros == 0:  # om hel råden är fylld, då tar det bort råden
                self.bg_sound_line.play(0)
                lines += 1
                # ta det bort raden
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2  # räkna score = lines^2

    def go_space(self):
        """ figur ska flytta sig ner till om det går när användare tryck på mellanslag"""
        self.bg_sound_drop.play(0)
        while not self.intersects():  # loop till det går
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        """ figur ska flytta sig ner en pixel*zoom"""
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        """ Markera field där alla figur är fyllda"""
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():  # om alla markerad är det fullt
            self.active = False
            self.game_over = True

    def go_side(self, dx):
        """ Figure flytter till vänster (dx negative) eller höger (positive) beror på hur dx blir
            dx blir +1 eller -1 så figur flytta dx*zoom
        """
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():  # om det får inte flytta figur får x postion lika innan flytt
            self.figure.x = old_x

    def rotate(self):
        """rotera figure"""
        self.bg_sound_rotate.play(0)
        old_rotation = self.figure.rotation  # spara rotation innan flytt
        self.figure.rotate()  # rotera figure
        if self.intersects():  # om det blir genomskärs, rotera inte
            self.figure.rotation = old_rotation


def game_over(screen):
    """Show Game over screen"""
    # rita text på Teris skäm
    font1 = pygame.font.SysFont('comicsans', 65, True, False)
    font2 = pygame.font.SysFont('comicsans', 25, True, False)
    text_game_over = font1.render("Game Over", True, (255, 0, 0))
    text_game_over1 = font2.render("Press R to restart", True, 'Black')
    screen.blit(text_game_over, [35, 180])
    screen.blit(text_game_over1, [90, 265])


def draw_freeze_figures(colors, game, screen):
    """ Rita kraftnät och rita alla figur som har redan körd"""
    for i in range(game.height):
        for j in range(game.width):
            # rita kraftnät med färg Gray och börja på position Teris skäm
            pygame.draw.rect(screen, (204, 102, 0),
                             [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                # rita alla figurer som har redan ligger nedan: type rect(screen, färg, x, y, width, hight)
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                  game.zoom - 1])


def draw_next_figure(colors, game,  _screen):
    """Rita nästa figur"""
    font = pygame.font.SysFont('comicsans', 20)
    label = font.render('Next Shape', False, 'Black')
    label_rect = label.get_rect(center=(320, 85))
    _screen.blit(label, label_rect)

    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in game.block_list[0].image():
                pygame.draw.rect(_screen, colors[game.block_list[0].color],
                                 [game.x + 110 + game.zoom * (j + game.block_list[0].x) + 1,
                                  game.y + 90 + game.zoom * (i + game.block_list[0].y) + 1,
                                  game.zoom - 2, game.zoom - 2])


def draw_figure(colors, game, screen):
    """Rita en figure"""
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    # rita alla delar av figur: type rect(screen, färg, x, y, width, hight)
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])


def play_tetris():
    from hubtest1 import start_game_hub, Image, Text
    """ Function run tetris game"""
    colors = [
        (0, 0, 0),
        (120, 37, 179),
        (100, 179, 179),
        (80, 34, 22),
        (80, 134, 22),
        (180, 34, 22),
        (180, 34, 122),
    ]
    # Initialize the game engine
    pygame.init()

    size = (400, 500)  # stolek av skäm (not Teris skäm)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")
    is_first_time = True
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(21, 10)  # skapa en Teris skäm med hight = 20, width = 10
    counter = 0

    pressing_down = False

    bg_sound_background = pygame.mixer.Sound('Tetris_folder/audio/background.mp3')
    bg_sound_gameover = pygame.mixer.Sound('Tetris_folder/audio/over.mp3')
    bg_sound_gameover.set_volume(0.2)
    bg_sound_background.set_volume(0.2)
    bg_sound_background.play()
    input_box = InputBox(100, 100, 140, 32, (153, 76, 0), (204, 102, 0))
    user_id = ''
    done = False

    while True:

        game.game_over = False
        screen.fill('White')  # fill färg för hela skäm
        back_ground_img = Image('Tetris_folder/background.jpg', (200, 0))
        back_ground_img.draw(screen)
        menu_surface = pygame.image.load('Tetris_folder/menu.png').convert_alpha()
        menu_rect = menu_surface.get_rect(topleft=(10, 5))

        if is_first_time:
            font1 = pygame.font.SysFont('comicsans', 25, False, False)
            text_register = font1.render("Username", True, (204, 102, 0))
            font2 = pygame.font.SysFont('comicsans', 15, False, False)
            text_error = font2.render("Please input name", True, (102, 51, 0))
            screen.blit(text_register, [100, 60])
            while not done:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        screen.blit(text_error, [100, 150])
                        pygame.quit()
                        exit()

                    user_id = input_box.handle_event(event)
                    back_ground_img = Image('Tetris_folder/background.jpg', (200, 0))
                    back_ground_img.draw(screen)
                    screen.blit(menu_surface, menu_rect)
                    screen.blit(text_register, [100, 60])
                    input_box.update()
                    input_box.draw(screen)
                    if user_id:
                        user_id = str(user_id).lower().strip()
                        done = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu_rect.collidepoint(event.pos):
                            bg_sound_background.stop()
                            start_game_hub()

                pygame.display.flip()
            is_first_time = False

        back_ground_img.draw(screen)
        screen.blit(menu_surface, menu_rect)
        high_score_image = Image('Tetris_folder/high_score.png', (370, 10))
        high_score_image.draw(screen)
        if game.figure is None:  # om det finns ingen figur (börja play)
            game.new_figure()  # skapa en ny figur
        counter += 1
        if counter > 100000:
            counter = 0
        # om användare trycker på k_down eller det gå ner automat förlja counters värde
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.active:
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game.active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # k_up för att rotera
                        game.rotate()
                    if event.key == pygame.K_DOWN:  # k_down för att gå ner (markera pressing_down = True
                        pressing_down = True
                    if event.key == pygame.K_LEFT:  # k_left för att gå till vänster
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:  # k_right för att gå till höger
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:  # k_space för att gå längst ner
                        game.go_space()
                    if event.key == pygame.K_ESCAPE:  # k_esc för att spela om
                        bg_sound_background.stop()
                        start_game_hub()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:  # om användare släpa k_down så markera pressing_down = False
                        pressing_down = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if high_score_image.image_rect.collidepoint(event.pos):
                        high_score('tetris', screen, user_id, (game.score, 0), True)

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.__init__(21, 14)
                        bg_sound_background.play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if high_score_image.image_rect.collidepoint(event.pos):
                        high_score('tetris', screen, user_id, (game.score, 0), True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    bg_sound_background.stop()
                    start_game_hub()

        draw_freeze_figures(colors, game, screen)
        draw_figure(colors, game, screen)
        draw_next_figure(colors, game, screen)
        # skapa alla text för att visa
        score = Text(f'Score: {game.score}', (200, 0), 'Yellow', 25)
        score.draw(screen)

        if not game.active:
            is_first_time = False
            game_over(screen)
            if game.game_over:
                bg_sound_gameover.play(0)
                high_score('tetris', screen, user_id, (game.score, 0), False)
                bg_sound_background.stop()

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    play_tetris()
