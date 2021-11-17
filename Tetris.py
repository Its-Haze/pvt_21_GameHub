import pygame  # importera pygame packet
from sys import exit  # importera function exit from modul sys


def display_score():
    """ visa score av användare"""
    current_time = pygame.time.get_ticks() - start_time # score
    score_surf = test_font.render(f'{current_time}', False, (64, 64, 64)) # score font
    score_rect = score_surf.get_rect(center=(600, 50))
    screen.blit(score_surf, score_rect)


# # # # Aktivera Pygame # # # #

pygame.init()  # initiera pygame biblioteket
screen = pygame.display.set_mode((800, 400))  # Skapa ett Pygame fönster att jobba i
clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes
game_active = True # variabln för att kolla om game ska köra
start_time = 0 # varibel att spara senast tiden
# # # # Surface, Rektanglar & Fonts # # # #

# Sky
sky_surface = pygame.image.load('graphics/Sky.png')  # Laddar in bilden Sky.png

# Ground
ground_surface = pygame.image.load('graphics/ground.png')  # Laddar in bilden ground.png

# Snail
snail_surface = pygame.image.load('graphics/snail/snail1.png')  # Laddar in bilden snail1.png
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

#snail_x_pos = 600  # Startar dens x_position med 600

# Player
player_surf = pygame.image.load('graphics/Player/player_walk_1.png')  # Laddar in bilden player_walk_1.png
player_rect = player_surf.get_rect(midbottom=(100, 300))  # skapar rektangel som man kan styra
player_gravity = 0 # variabln för att kontrolera hur hög player ska hoppa

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
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: # hoppa med click från muss
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20 # hoppa upp 20 från player står
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: # hoppa med mellandslag,
                    player_gravity = -20 #hoppa upp 20 från player står
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # slå på mellanslag för att starta om game
                game_active = True # kör game igen
                snail_rect.left = 800 # initerra igen snigel plats
                start_time = pygame.time.get_ticks() # spara tiden av sista gång

    if game_active:
        screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1

        screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2

        screen.blit(text_surface, text_rectangle)  # Sätter texten på skärmen  - Lager 3
        display_score()
        snail_rect.x -= 4  # uppdaterar snigelns x position med [-4] varje gång while loopen körs
        if snail_rect.right < 0:  # Kollar om snigelns x position är mindre än 0
            snail_rect.left = 800  # sätter dens x position till 800

        screen.blit(snail_surface, snail_rect)  # sätter snigeln på skärmen med positionen av snail_rect
        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: #efter player hoppade och trilla ned, vi kontrolerar om att stå på ground surface
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)  # Sätter spelaren på skärmen med positionen av player_rect

        if snail_rect.colliderect(player_rect):# om player träffar snail
            game_active = False # stop game
    else:
        screen.fill('Yellow') # när game är stopp

    pygame.display.update()  # uppdaterar skärmen [pygame window]
    clock.tick(60)  # hur snabb program kör [60 fps]
