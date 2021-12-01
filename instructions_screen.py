import pygame
from sys import exit
from eriks_runner import play_runner
from tetris import play_tetris
from Space_Invaders_Game.main import play_space_invaders
import ctypes  # An included library with Python install.


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def show_intro_screen(game_name):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
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

    bg_sound_hub = pygame.mixer.Sound('audio/hub.mp3')
    bg_sound_hub.set_volume(0.2)
    bg_sound_hub.play()

    while running:
        from hubtest1 import start_game_hub

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    if game_name == "runner":
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_runner()
                    elif game_name == "tetris":
                        print(f'Klickade på {game_name}')
                        bg_sound_hub.stop()
                        play_tetris()
                if guide_rect.collidepoint(event.pos):
                    if game_name == "runner":
                        print("klickade på runner guide knappen")
                    elif game_name == "tetris":
                        print("klickade på tetris guide knappen")

                        Mbox("Tetris regler",
                             "Tetris bygger på block som är uppbyggda av fyra rutor. Det finns sju möjliga, sammanhängande figurer som består av fyra rutor vardera. De kallas ofta för 'I', 'T', 'O', 'L', 'J', 'S' och 'Z', efter deras former. "
                             + "Dessa block släpps mer eller mindre slumpvis ner från övre delen av ett spelfält . Medan de faller ner kan de styras i sidled, samt vridas. "
                             + "När ett block landar på botten av spelfältet, eller på ett annat block, stannar det och nästa block släpps ner. "
                             + "När ett block har landat så att en eller flera vågräta rader var som helst i höjdleden är helt täckta med rutor försvinner de raderna, och raderna ovanför flyttas ner. "
                             + "Spelaren får poäng, vanligen mer ju fler rader som försvinner samtidigt. Som mest kan fyra rader försvinna genom att ett 'I'-block placeras vertikalt",
                             0)

                if back_rect.collidepoint(event.pos):
                    print("klickade på back knappen")
                    bg_sound_hub.stop()
                    start_game_hub()

        if running:
            screen.fill("black")

            # Rotation
            # True
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

            # Change screen to the current game

            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    show_intro_screen("runner")
