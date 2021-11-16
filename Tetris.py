import pygame  # importera pygame packet
from sys import exit  # importera function exit from modul sys


# # # # Aktivera Pygame # # # #

pygame.init()  # initiera pygame biblioteket
screen = pygame.display.set_mode((800, 400))  # Skapa ett Pygame fönster att jobba i
clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes

# # # # Surface, Rektanglar & Fonts # # # #

# Sky
sky_surface = pygame.image.load('graphics/Sky.png')  # Laddar in bilden Sky.png

# Ground
ground_surface = pygame.image.load('graphics/ground.png')  # Laddar in bilden ground.png

# Snail
snail_surface = pygame.image.load('graphics/snail/snail1.png')  # Laddar in bilden snail1.png
snail_x_pos = 600  # Startar dens x_position med 600

# Player
player_surf = pygame.image.load('graphics/Player/player_walk_1.png')   # Laddar in bilden player_walk_1.png
player_rect = player_surf.get_rect(midbottom=(100, 300))  # skapar rektangel som man kan styra

# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # loading en font

# Texter
text_surface = test_font.render('Tetris', False, 'Black')  # Skapar text ["text", bool, "färg"]
text_rectangle = text_surface.get_rect(midtop=(400, 50))  # Skapar rektangel som man kan styra


while True:
    # Allt inuti denna while loopen uppdateras på skärmen varje sekund

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Om knappen [x] klickas så hör följande:
            pygame.quit()  # Stäng av pygame
            exit()  # Stäng ner hela python filen

    screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1

    screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2

    screen.blit(text_surface, text_rectangle)  # Sätter texten på skärmen  - Lager 3

    snail_x_pos -= 4  # uppdaterar snigelns x position med [-4] varje gång while loopen körs
    if snail_x_pos < 0:  # Kollar om snigelns x position är mindre än 0
        snail_x_pos = 800  # sätter dens x position till 800

    snail_rect = snail_surface.get_rect(midbottom=(snail_x_pos, 300))  # uppdaterar snigelns rektangel

    screen.blit(snail_surface, snail_rect)  # sätter snigeln på skärmen med positionen av snail_rect

    screen.blit(player_surf, player_rect)  # Sätter spelaren på skärmen med positionen av player_rect

    pygame.display.update()  # uppdaterar skärmen [pygame window]
    clock.tick(60)  # hur snabb program kör [60 fps]
