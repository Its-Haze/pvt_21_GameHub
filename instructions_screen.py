import pygame
from random import choice
from sys import exit
from eriks_runner import play_runner
from tetris import play_tetris
from snake import play_snake
from space_invaders import play_space_invaders
import ctypes  # An included library with Python install.


class Player(pygame.sprite.Sprite):
    def __init__(self, angle):  # initiera klassen och lägg in en sträng vad obstacle heter
        super().__init__()  # initiera pygame.sprite.Sprite
        self.angle = angle
        #  list comprehension, ladda in alla 8 Frames av fåglarna i deras original storlek
        player_walking_frames = [pygame.image.load(f'Runner_folder/graphics/player/player_walk_{i}.png').convert_alpha()
                                 for i in range(1, 3)]
        y_pos = 600
        x_pos = 0
        self.up_scale = 1.1
        if self.angle == "Left":
            self.frames = [pygame.transform.scale(i, (int(i.get_width() * self.up_scale),
                                                      int(i.get_height() * self.up_scale)))
                           for i in player_walking_frames]
            x_pos = -10

        elif self.angle == "Right":
            left_unscaled_player = [pygame.transform.flip(i, True, False) for i in player_walking_frames]
            self.frames = [pygame.transform.scale(i, (int(i.get_width() * self.up_scale),
                                                      int(i.get_height() * self.up_scale)))
                           for i in left_unscaled_player]
            x_pos = 810
        self.animation_index = 0  # vilket index som bilden vi är på ska visa
        self.image = self.frames[self.animation_index]  # image= listan av alla bilder med vilket index vi vill visa upp
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))  # rektangeln har ett random x värde och ett y värde

    def animation_state(self):  # metod för att öka indexet så bilden ändras
        """Animerar alla frames i listan self.frames och sätter nuvarande frame som self.image"""
        self.animation_index += 0.1  # öka hela tiden med 0.1
        if self.animation_index >= len(self.frames):  # kolla om indexet är större eller lika med listans storlek
            self.animation_index = 0  # sätt den tillbaka till 0
        self.image = self.frames[int(self.animation_index)]  # sätt bilden till vad indexet är inuti frames listan

    def update(self):  # sprite.Sprite update metod
        """uppdaterar hela tiden i game loopen"""
        self.animation_state()  # vilken animation vi ska visa
        if self.angle == "Right":
            self.rect.x -= 6  # flytta obstacle -5 pixlar
        elif self.angle == "Left":
            self.rect.x += 6  # fly
        self.destroy()  # kolla om vi är utanför skärmen - DESTROY

    def destroy(self):  # sprite.Sprite destroy metod
        """ tar bort alla instanser av klassen om spelarens x axel har nått utanför skärmen"""
        if self.angle == "Right":
            if self.rect.x <= -100:  # om obstacle är för långt utanför skärmen
                self.kill()  # ta bort den från obstacle gruppen
        elif self.angle == "Left":
            if self.rect.x >= 900:
                self.kill()


def mbox(title, text, style):
    """returnerar en messagebox"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def show_intro_screen(game_name):
    """Funktionen som startar intro screen från game_hub filen"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"{game_name} - menu")
    surf_rotation = 0
    surf_scale = 2

    surf_rotation_bool = True

    clock = pygame.time.Clock()
    running = True

    pygame.font.init()  # Behövs för att initiera fonts

    play_surface = pygame.image.load(
        'Instructions_folder/menu_buttons/start_button_text.png').convert_alpha()  # surface - Sky.png
    play_rect = play_surface.get_rect(midtop=(400, 120))

    guide_surface = pygame.image.load(
        "Instructions_folder/menu_buttons/guide_button_text.png").convert_alpha()
    guide_rect = guide_surface.get_rect(midtop=(400, 260))

    back_surface = pygame.image.load(
        "Instructions_folder/menu_buttons/back_button_text.png").convert_alpha()
    back_rect = back_surface.get_rect(midtop=(400, 400))

    # Guide Pictures
    runner_guide_surface = pygame.image.load("Runner_folder/graphics/runner_guide_2.png").convert_alpha()
    runner_guide_rect = runner_guide_surface.get_rect(topleft=(0, 0))

    tetris_guide_surface = pygame.image.load("Tetris_folder/tetris_guide.png").convert_alpha()
    tetris_guide_rect = tetris_guide_surface.get_rect(topleft=(0, 0))

    tetris_about_surface = pygame.image.load("Tetris_folder/what_is_tetris.png").convert_alpha()
    tetris_about_rect = tetris_about_surface.get_rect(bottomleft=(25, 575))

    snake_guide_surface = pygame.image.load("Snake_folder/snake_guide.png").convert_alpha()
    snake_guide_rect = tetris_guide_surface.get_rect(topleft=(0, 0))

    space_invaders_guide_surface = pygame.image.load("Space_Invaders_folder/res/space_invaders_guide.png") \
        .convert_alpha()
    space_invaders_guide_rect = space_invaders_guide_surface.get_rect(topleft=(0, 0))

    user_press_guide = False

    bg_sound_hub = pygame.mixer.Sound('audio/hub.mp3')
    bg_sound_hub.set_volume(0.1)
    bg_sound_hub.play(-1)

    player_group = pygame.sprite.Group()
    player_walk_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_walk_timer, 1600)

    while running:
        from game_hub import start_game_hub

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    user_press_guide = False

            if event.type == player_walk_timer:
                player_group.add(Player(choice(["Left", "Right"])))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Play Knappen
                if play_rect.collidepoint(event.pos):
                    if game_name == "runner" and not user_press_guide:
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_runner()
                    elif game_name == "tetris" and not user_press_guide:
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_tetris()
                    elif game_name == "snake":
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_snake()
                    elif game_name == "space invaders":
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_space_invaders()

                # Guide knappen
                if guide_rect.collidepoint(event.pos):

                    if game_name == "runner" and not user_press_guide:
                        print("klickade på runner guide knappen")
                        user_press_guide = True

                    elif game_name == "tetris" and not user_press_guide:
                        print("klickade på tetris guide knappen")
                        user_press_guide = True

                    elif game_name == "snake" and not user_press_guide:
                        print("klickade på snake guide knappen")
                        user_press_guide = True

                    elif game_name == "space invaders" and not user_press_guide:
                        print("klickade på space invaders guide knappen")
                        user_press_guide = True

                # Tetris [What is tetris] knappen
                if tetris_about_rect.collidepoint(event.pos):
                    if game_name == "tetris" and not user_press_guide:
                        mbox("Tetris regler",
                             "Tetris bygger på block som är uppbyggda av fyra rutor. Det finns sju möjliga, "
                             "sammanhängande figurer som består av fyra rutor vardera. "
                             "De kallas ofta för 'I', 'T', 'O', 'L', 'J', 'S' och 'Z', efter deras former. "
                             + "Dessa block släpps mer eller mindre slumpvis ner från övre delen av ett spelfält. "
                               "Medan de faller ner kan de styras i sidled, samt vridas. "
                             + "När ett block landar på botten av spelfältet, "
                               "eller på ett annat block, stannar det och nästa block släpps ner. "
                             + "När ett block har landat så att en eller flera vågräta rader var som helst i "
                               "höjdleden är helt täckta med rutor försvinner de raderna, "
                               "och raderna ovanför flyttas ner. "
                             + "Spelaren får poäng, vanligen mer ju fler rader som försvinner samtidigt. "
                               "Som mest kan fyra rader försvinna genom att ett 'I'-block placeras vertikalt",
                             0)
                # Tillbaka Knappen
                if back_rect.collidepoint(event.pos):
                    if not user_press_guide:
                        print("klickade på back knappen")
                        bg_sound_hub.stop()
                        start_game_hub()

        if running:
            screen.fill("black")
            if user_press_guide and game_name == "runner":
                screen.blit(runner_guide_surface, runner_guide_rect)
            elif user_press_guide and game_name == "tetris":
                screen.blit(tetris_guide_surface, tetris_guide_rect)
            elif user_press_guide and game_name == "snake":
                screen.blit(snake_guide_surface, snake_guide_rect)
            elif user_press_guide and game_name == "space invaders":
                screen.blit(space_invaders_guide_surface, space_invaders_guide_rect)

            else:
                # Rotation
                # True
                if game_name == "runner":
                    player_group.draw(screen)
                    player_group.update()

                if surf_rotation_bool:
                    surf_rotation -= 1
                    surf_scale -= 0.01

                if surf_rotation == -20:
                    surf_rotation_bool = False
                # False
                if not surf_rotation_bool:
                    surf_rotation += 1
                    surf_scale += 0.01

                if surf_rotation == 20:
                    surf_rotation_bool = True

                font = pygame.font.Font("Instructions_folder/font/FFFFORWA.TTF", 10)
                title_text = font.render(f"{game_name}", False, "white")
                title_rotozoom_text = pygame.transform.rotozoom(
                    title_text, surf_rotation, surf_scale)
                title_rect = title_rotozoom_text.get_rect(midtop=(400, 20))

                screen.blit(title_rotozoom_text, title_rect)
                screen.blit(play_surface, play_rect)
                screen.blit(guide_surface, guide_rect)
                screen.blit(back_surface, back_rect)
                if game_name == "tetris":
                    screen.blit(tetris_about_surface, tetris_about_rect)

                # Change screen to the current game

            pygame.display.update()
            clock.tick(60)

# if __name__ == '__main__':
#     show_intro_screen()
