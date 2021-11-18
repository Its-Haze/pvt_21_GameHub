import pygame  # importera pygame packet
from sys import exit  # importera function exit from modul sys


def display_score():
    """ visa score av användare"""
    current_time = (pygame.time.get_ticks() - start_time)//1000  # score
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))  # score font
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def display_pre_score(score):
    pre_score_surf = test_font.render(f'Score: {score}', False, 'Grey')
    pre_score_rect = pre_score_surf.get_rect(center=(400, 50))
    screen.blit(pre_score_surf, pre_score_rect)


# # # # Aktivera Pygame # # # #

pygame.init()  # initiera pygame biblioteket
screen = pygame.display.set_mode((800, 400))  # Skapa ett Pygame fönster att jobba i
clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes
game_active = False  # variabln för att kolla om game ska köra
start_time = 0  # varibel att spara senast tiden
# # # # Surface, Rektanglar & Fonts # # # #

# Sky
sky_surface = pygame.image.load('graphics/Sky.png')  # Laddar in bilden Sky.png

# Ground
ground_surface = pygame.image.load('graphics/ground.png')  # Laddar in bilden ground.png

# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # loading en font

# Snail
snail_surface = pygame.image.load('graphics/snail/snail1.png')  # Laddar in bilden snail1.png
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

# snail_x_pos = 600  # Startar dens x_position med 600

# Player
player_surf = pygame.image.load('graphics/Player/player_walk_1.png')  # Laddar in bilden player_walk_1.png
player_rect = player_surf.get_rect(midbottom=(100, 300))  # skapar rektangel som man kan styra
player_gravity = 0  # variabln för att kontrolera hur hög player ska hoppa
player_rotate = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()





# Vi skapar en rektangel och centrerar den.

# Texter
text_surface = test_font.render('Austranaut runner', False, 'Black')  # Skapar text ["text", bool, "färg"]
text_rectangle = text_surface.get_rect(midtop=(400, 50))  # Skapar rektangel som man kan styra
score = 0
while True:
    # Allt inuti denna while loopen uppdateras på skärmen varje sekund

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Om knappen [x] klickas så hör följande:
            pygame.quit()  # Stäng av pygame
            exit()  # Stäng ner hela python filen
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:  # hoppa med click från muss
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20  # hoppa upp 20 från player står
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:  # hoppa med mellandslag,
                    player_gravity = -20  # hoppa upp 20 från player står
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # slå på mellanslag för att starta om game
                game_active = True  # kör game igen
                snail_rect.left = 800  # initerra igen snigel plats
                start_time = pygame.time.get_ticks()  # spara tiden av sista gång

    if game_active:
        screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1

        screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2

        score = display_score()
        snail_rect.x -= 4  # uppdaterar snigelns x position med [-4] varje gång while loopen körs
        if snail_rect.right < 0:  # Kollar om snigelns x position är mindre än 0
            snail_rect.left = 800  # sätter dens x position till 800

        screen.blit(snail_surface, snail_rect)  # sätter snigeln på skärmen med positionen av snail_rect
        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:  # efter player hoppade och trilla ned, vi kontrolerar om att stå på ground surface
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)  # Sätter spelaren på skärmen med positionen av player_rect

        if snail_rect.colliderect(player_rect):  # om player träffar snail
            game_active = False  # stop game
    if not game_active:
        screen.fill((94, 129, 162))

        if score == 0:  # Visar speltitel om score är noll
            screen.blit(text_surface, text_rectangle)
            instructions_surf = test_font.render('Press space to play', False, 'Black')
        else:  # Om spelaren har spelat en omgång, visa score istället
            display_pre_score(score)
            instructions_surf = test_font.render('Press space to play again', False, 'Black')
        instructions_rect = instructions_surf.get_rect(center=(400, 350))


        # player_rotate -= 4

        _player_stand = pygame.transform.rotozoom(player_stand, player_rotate,2)  # Tar en bild och gör den större eller rotera den.
        player_stand_rect = _player_stand.get_rect(center=(400, 200))
        screen.blit(_player_stand, player_stand_rect)
        screen.blit(instructions_surf, instructions_rect)

    pygame.display.update()  # uppdaterar skärmen [pygame window]
    clock.tick(60)  # hur snabb program kör [60 fps]
