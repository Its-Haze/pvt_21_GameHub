import pygame   # https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
import random
from sys import exit

# alla färg av figur


class Figure:
    x = 0  # figur x position
    y = 0  # figur y position
    # definera alla type and rotation of figur och spara i en list
    # alla figur ligger in fyrakantan 4*4
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # lika I
        [[4, 5, 9, 10], [2, 6, 5, 9]], #
        [[6, 7, 9, 10], [1, 5, 6, 10]], # lika Z
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # lika J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # lika L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # lika T
        [[1, 2, 5, 6]],# lika O
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
        self.type = random.randint(0, len(self.figures) - 1) # valjer random figur from figures listan
        self.color = random.randint(1, len(self.colors) - 1) # väljer random färg from colors listan
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation] # välja en figur

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type]) #rotation


class Tetris:
    level: float # controlera hur snabb figur ska flytta ner
    score: int
    state: str
    field: list
    height: int
    width: int
    x: int
    y: int
    zoom = 20 # hur stor av fyrakantan in kraftnät
    figure = None

    def __init__(self, height, width):
        """ Skapa en teris """
        self.height = height #hög av Teris skäm
        self.width = width # lengd av Teris skäm
        self.field = [] # list för att kolla om hur fingurer har fyller på skäm
        self.score = 0 # spare påäng
        self.state = "start" # status
        self.x = 100
        self.y = 60
        self.level = 1.5

        # skapa alla värde av field lika med 0
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        """ Skapa en new figur"""
        self.figure = Figure(3, 0)

    def intersects(self):
        """ kolla om figur får röra sig """
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    # kolla om position av figur går ut Teris skäm eller finns något figure har redan ligger på Teris skäm
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        """ Ta bort alla lines som har filler upp av figur"""
        lines = 0 # rakna hur många råder ska ta bort
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0: # kolla om field[i][j] int har fyllt
                    zeros += 1
            if zeros == 0: #om hel råden är fylld, då tar det bort råden
                lines += 1
                # ta det bort raden
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2 # räkna score = lines^2

    def go_space(self):
        """ figur ska flytta sig ner till om det går när användare tryck på mellanslag"""
        while not self.intersects(): # loop till det går
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
        if self.intersects(): # om alla markerad är det fullt
            self.state = "gameover"

    def go_side(self, dx):
        """ Figure flytter till vänster (dx negative) eller höger (positive) beror på hur dx blir
            dx blir +1 eller -1 så figur flytta dx*zoom
        """
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects(): # om det får inte flytta figur får x postion lika innan flytt
            self.figure.x = old_x

    def rotate(self):
        """rotera figure"""
        old_rotation = self.figure.rotation # spara rotation innan flytt
        self.figure.rotate() # rotera figure
        if self.intersects(): # om det blir genomskärs, rotera inte
            self.figure.rotation = old_rotation

def play_tetris():
    from hubtest1 import start_game_hub
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

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    size = (400, 500) # stolek av skäm (not Teris skäm)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")

    # Loop until the user clicks the close button.
    running = True
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10) # skapa en Teris skäm med hight = 20, width = 10
    counter = 0

    pressing_down = False

    while running:
        if game.figure is None: # om det finns ingen figur (börja play)
            game.new_figure() # skapa en ny figur
        counter += 1
        if counter > 100000:
            counter = 0
        # om användare trycker på k_down eller det gå ner automat förlja counters värde
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: # k_up för att rotera
                    game.rotate()
                if event.key == pygame.K_DOWN: # k_down för att gå ner (markera pressing_down = True
                    pressing_down = True
                if event.key == pygame.K_LEFT: # k_left för att gå till vänster
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT: # k_right för att gå till höger
                    game.go_side(1)
                if event.key == pygame.K_SPACE: # k_space för att gå längst ner
                    game.go_space()
                if event.key == pygame.K_ESCAPE: # k_esc för att spela om
                    start_game_hub()
                if event.key == pygame.K_r:
                    game.__init__(20, 10)

        if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN: # om användare släpa k_down så markera pressing_down = False
                    pressing_down = False

        screen.fill(WHITE) # fill färg för hela skäm
        # rita kraftnät och rita alla figur som har redan körd
        for i in range(game.height):
            for j in range(game.width):
                # rita kraftnät med färg Gray och börja på position Teris skäm
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    # rita alla figurer som har redan ligger nedan: type rect(screen, färg, x, y, width, hight)
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
        # rita en figure
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        #rita alla delar av figur: type rect(screen, färg, x, y, width, hight)
                        pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.zoom * (j + game.figure.x) + 1,
                                        game.y + game.zoom * (i + game.figure.y) + 1,
                                        game.zoom - 2, game.zoom - 2])
        # skapa alla text för att visa
        font = pygame.font.SysFont('comicsans', 25, True, False) # font för text
        font1 = pygame.font.SysFont('comicsans', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)  #
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press R", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        if game.state == "gameover":
            # rita text på Teris skäm
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    play_tetris()
