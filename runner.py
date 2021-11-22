import pygame  # importera pygame packet
from random import randint
from sys import exit  # importera function exit from modul sys


def display_score():
    """ visa score av användare"""
    current_time = (pygame.time.get_ticks() - start_time) // 1000  # score
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))  # score font
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def display_pre_score(score):
    pre_score_surf = test_font.render(f'Score: {score}', False, 'Grey')
    pre_score_rect = pre_score_surf.get_rect(center=(400, 50))
    screen.blit(pre_score_surf, pre_score_rect)


def obstacle_movement(obstacle_list: list):
    if obstacle_list:  # Om listan inte är tom
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5  # Flyttar varje obstacle 5 pixlar till vänster
            if obstacle_rect.bottom == 300:  # Om obstacle är 300 så vet vi att det är en snigel
                screen.blit(snail_surface, obstacle_rect)  # blit snail_surface
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if
                         obstacle.x > -100]  # Sparar bara obstacles om deras x värde är större än minus 100
        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    """ return False om player träffar obstacle, annars  return True"""
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle): # om player träffa obstacle
                return False
    return True


def player_animation(pl_surf, index):
    if player_rect.bottom < 300:
        pl_surf = player_jump
    else:
        index += 0.1
        if index > len(player_walk):
            index = 0
        pl_surf = player_walk[int(index)]
    return pl_surf, index

# # # # Aktivera Pygame # # # #

pygame.init()  # initiera pygame biblioteket
screen = pygame.display.set_mode((800, 400))  # Skapa ett Pygame fönster att jobba i
clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes
game_active = False  # variabln för att kolla om game ska köra
start_time = 0  # varibel att spara senast tiden
# # # # Surface, Rektanglar & Fonts # # # #

# Timers för event
obstacle_timer = pygame.USEREVENT + 1  # Vi skapar en timer genom att använda pygame's USEREVENT.
# Vi plussar på 1 för att inte använda pygames reserverade ID för USEREVENT.
pygame.time.set_timer(obstacle_timer, 1500)  # Vi bestämmer hur ofta pygame ska köra vårat event (1.5 sekunder)

snail_timer = pygame.USEREVENT + 2  # Vi skapar en timer för att välja hur ofta bilden på snigeln skall bytas ut - detta skapar en animering
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3 # Vi skapar en timer för att animera flugan
pygame.time.set_timer(fly_timer, 200)


# Obstacles
obstacles_list = []  # Vi skapar listan som våra obstacles kommer ligga i

# Sky
sky_surface = pygame.image.load('graphics/Sky.png')  # Laddar in bilden Sky.png

# Ground
ground_surface = pygame.image.load('graphics/ground.png')  # Laddar in bilden ground.png

# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # loading en font

# Snail
snail_animation_1 = pygame.image.load('graphics/snail/snail1.png')  # Laddar in bilden snail1.png
snail_animation_2 = pygame.image.load('graphics/snail/snail2.png')  # Laddar in bilden snail1.png
snail_index = 0
snail_animation = [snail_animation_1, snail_animation_2]
snail_surface = snail_animation[snail_index]

# Fly
fly_animation_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_animation_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_index = 0
fly_animation = [fly_animation_1, fly_animation_2]
fly_surf = fly_animation[fly_index]

# Player
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_index = 0
player_walk = [player_walk1, player_walk2]

player_surf = player_walk[player_index]  # Laddar in bilden player_walk_1.png
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

            if event.type == obstacle_timer:
                print('Våran obstacle timer funkar!')
                if randint(0, 1):
                    obstacles_list.append(snail_surface.get_rect(midbottom=(randint(800, 1100), 300)))  # Lägger till en snigel i listan av obstacles
                else:
                    obstacles_list.append(fly_surf.get_rect(midbottom=(randint(800, 1100), 210)))

            if event.type == snail_timer:
                if snail_index == 0:  # Varannan gång blittar vi första snigelnbilden, varannan gång den andra
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_animation[snail_index]

            if event.type == fly_timer:
                if fly_index == 0:  # Varannan gång blittar vi första flugbilden, varannan gång den andra
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_animation[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # slå på mellanslag för att starta om game
                game_active = True  # kör game igen
                start_time = pygame.time.get_ticks()  # spara tiden av sista gång

    if game_active:
        screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1

        screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2

        score = display_score()
        obstacles_list = obstacle_movement(obstacles_list) # anropa function obstacle_movement
        game_active = collision(player_rect, obstacles_list) # anropa function collision
        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:  # efter player hoppade och trilla ned, vi kontrolerar om att stå på ground surface
            player_rect.bottom = 300
        player_surf, player_index = player_animation(player_surf, player_index)
        screen.blit(player_surf, player_rect)  # Sätter spelaren på skärmen med positionen av player_rect

    if not game_active:
        screen.fill((94, 129, 162))

        if score == 0:  # Visar speltitel om score är noll
            screen.blit(text_surface, text_rectangle)
            instructions_surf = test_font.render('Press space to play', False, 'Black')
        else:  # Om spelaren har spelat en omgång, visa score istället
            display_pre_score(score)
            instructions_surf = test_font.render('Press space to play again', False, 'Black')
        instructions_rect = instructions_surf.get_rect(center=(400, 350))

        player_rotate -= 4

        _player_stand = pygame.transform.rotozoom(player_stand, player_rotate,
                                                  2)  # Tar en bild och gör den större eller rotera den.
        player_stand_rect = _player_stand.get_rect(center=(400, 200))
        screen.blit(_player_stand, player_stand_rect)
        screen.blit(instructions_surf, instructions_rect)
        obstacles_list.clear()  # Tömmer listan när spelaren har förlorat

    pygame.display.update()  # uppdaterar skärmen [pygame window]
    clock.tick(60)  # hur snabb program kör [60 fps]
