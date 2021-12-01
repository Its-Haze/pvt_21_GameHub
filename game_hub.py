import pygame
from sys import exit
from instructions_screen import show_intro_screen


class Image:
    """ Image class"""
    def __init__(self, image_url, pos):
        self.image_surface = pygame.image.load(image_url).convert_alpha()
        self.image_rect = self.image_surface.get_rect(midtop=pos)

    def draw(self, _screen):
        """display an image in pygame screen"""
        _screen.blit(self.image_surface, self.image_rect)


class Text:
    """ Text class"""
    def __init__(self, text, pos, color, size):
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont('Comic Sans MS', size)
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_rect = self.text_surface.get_rect(midtop=pos)

    def draw(self, _screen):
        """ Display text on pygame screen"""
        _screen.blit(self.text_surface, self.text_rect)

    def update_text(self, text):
        """Update text"""
        self.text_surface = self.font.render(text, False, self.color)

    def update_color(self, color):
        """Update color"""
        self.text_surface = self.font.render(self.text, False, color)


class Game:
    """Class game"""
    text: Text
    image: Image

    def __init__(self, text, image):
        self.text = text
        self.image = image


def start_game_hub():
    """ Game hub function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    # Implementering av scrollning
    intermediate_surf = pygame.surface.Surface((800, 800))
    scroll_y = 0

    clock = pygame.time.Clock()
    running = True

    pygame.font.init()  # Behövs för att initiera fonts

    menu_text = Text('Game hub', (400, 50), 'Black', 40)
    runner_text = Text('Runner', (220, 130), 'Black', 40)
    tetris_text = Text('Tetris', (580, 130), 'Black', 40)

    background_sky = pygame.image.load('Runner_folder/graphics/background/backgroundsky.png')

    list_of_games = []
    runner = Game(runner_text, Image('Runner_folder/graphics/medium_runner.png', (220, 200)))
    tetris = Game(tetris_text, Image('Tetris_folder/medium_tetris.png', (580, 200)))
    list_of_games.append(runner)
    list_of_games.append(tetris)

    bg_sound_hub = pygame.mixer.Sound('audio/hub.mp3')
    bg_sound_hub.set_volume(0.2)
    bg_sound_hub.play()

    while running:
        intermediate_surf.blit(background_sky, (0, 0))
        # Change screen to the current game
        menu_text.draw(intermediate_surf)
        for game in list_of_games:
            game.text.draw(intermediate_surf)
            game.image.draw(intermediate_surf)

        # When user click "runner", play "runner"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if runner.image.image_rect.collidepoint(event.pos):
                    print('Klickade på runner')
                    bg_sound_hub.stop()
                    show_intro_screen("runner")
                if tetris.image.image_rect.collidepoint(event.pos):
                    print('Klickade på tetris')
                    bg_sound_hub.stop()
                    show_intro_screen("tetris")

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    scroll_y = min(scroll_y + 25, 0)
                elif event.y == -1:
                    scroll_y = max(scroll_y - 25, -400)
        screen.blit(intermediate_surf, (0, scroll_y))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    start_game_hub()
