import pygame  # importera pygame packet
from sys import exit  # importera function exit from modul sys
from random import randint


# https://youtu.be/AY9MnQ4x3zk?t=10838

# TODO: check player class
# TODO: fix obstacle class
# TODO: remove all previous code that is no longer needed


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()  # surface - frames
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()  # surface - frames
        self.player_walk = [player_walk_1, player_walk_2]  # lista av de alla frames
        self.player_index = 0  # start index
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()  # surface - jump

        self.image = self.player_walk[self.player_index]  # image = listan med indexed [player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

        
    def player_input(self):
        keys = pygame.key.get_pressed()  # få en lista av alla keys som går att klicka
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # om mellanslaget trycks och spelaren är på y_300
            self.gravity = -17  # om man hoppar så får blir gravity -20
        
        
    def player_move(self):
        # player not walking out of frame
        if self.rect.left < 0:
            self.rect.left = 0  # om spelaren är utanför vänstra sidan av skärmen
        if self.rect.right > 800:
            self.rect.right = 800  # om spelaren är utanför högra sidan av skärmen

        # player walking movement speed
        if moving_right:
            self.rect.x += 4  # hastighet för att gå höger
        if moving_left:
            self.rect.x -= 4  # hastighet för att gå vänster
            
    
    def apply_gravity(self):
        self.gravity += 1  # ökar y axelns värde med 1 hela tiden
        self.rect.y += self.gravity  # sätter y värdet till det som gravity är
        if self.rect.bottom >= 300:  # om rektangelns nedre del är mindre eller lika med 300
            self.rect.bottom = 300  # sätt rektangelns bottom till 300
    
    def animation_state(self):
        """ Play walking animation if player is on floor, or jump animation if not on floor"""
        if self.rect.bottom < 300: # om spelaren inte är på marken
            self.image = self.player_jump
        else:
            if moving_right or moving_left:
                self.player_index += 0.1
                if self.player_index >= len(self.player_walk):
                    self.player_index = 0
                self.image = self.player_walk[int(self.player_index)]
            else:
                self.image = self.player_walk[0]

    def update(self):
        """ Update the methods of the class """
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.player_move()


def display_score():
    """ visa score av användare """
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # hur långt det har gått sen pygame.init()
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))  # objektet av score
    score_rect = score_surf.get_rect(center=(400, 50))  # rektanglen av objektet score
    screen.blit(score_surf, score_rect)  # skriver ut på skärmen varje gång funktionen körs
    return current_time  # returnera värdet av score


def obstacle_movement(obstacle_list):
    """ rör alla mobs och tar bort dem från listan om dem har åkt utanför skärmen """

    if obstacle_list:  # om listan inte är tom
        for obstacle_rect in obstacle_list:  # för varje mob i listan
            obstacle_rect.x -= 5  # hastigheten på alla mobs att röra sig till vänster

            if obstacle_rect.bottom == 300:  # om deras bottom-y värde ligger på 300 är det en snigel
                screen.blit(snail_surf, obstacle_rect)  # skriv ut snigeln på skärmen med dens nuvarande obstacle_rect position
            else:  # om deras bottom/y värde är något annat så är det en fluga
                screen.blit(fly_surf, obstacle_rect)  # skriv ut flugan
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle_rect.x > - 100]  # tar mobs från listan om de åker utanför skärmen

        return obstacle_list  # returnera listan med alla mobs
    else:
        return []  # Tom lista


def collisions(player, obstacle_list):  # Player surf, listan med alla mobs på skärmen
    """ om spelarens rektangel träffar en obstacle så sätts game_active till False, annars True """
    if obstacle_list:  # om listan innehåller ett värde
        for obstacle_rect in obstacle_list:  # för varje separat mob i mob listan
            if player.colliderect(obstacle_rect):  # om spelarens rektangel träffar mob rektanglen
                return False  # returnera False och spara detta värdet i game_active sen
    return True  # returnera True och spara detta värdet i game_active sen


def player_animation(player_surf, player_index):
    """ Play walking animation if player is on floor, or jump animation if not on floor"""

    if player_rect.bottom < 300:  # om nedre rektanglen är på marken
        player_surf = player_jump  # om spelaren inte är på marken så ska player_jump animationen visas

    else:
        if moving_right or moving_left:  # om spelaren rör sig höger eller vänster
            player_index += 0.1  # öka med 0.1
            if player_index >= len(player_walk):  # om indexet är högre/lika med player_walk listan (2)
                player_index = 0  # sätt tillbaka variabeln till 0 om den gått till 2.0
            player_surf = player_walk[int(player_index)]  # bilden för gubben blir en surface från listan med indexet player_index
            # walk animation
        else:
            player_surf = player_walk[0]  # om spelaren inte rör sig så ska bara indexet 0 visas
    return player_surf, player_index


# # # # Aktivera Pygame # # # #
pygame.init()  # initiera pygame biblioteket
pygame.display.set_caption("The insane runner")
WINDOW_SIZE = (800, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)  # Skapa ett Pygame fönster (width=800, Height=400)
clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes
pygame.time.Clock()
game_active = False  # variabeln för att kolla om game ska köra
start_time = 0  # variabel att spara senast tiden

# # # # Surface, Rektanglar & Fonts # # # #

# Font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # loading en font

# Obstacles - kommer innehålla alla sniglar och flugor som har spawnats

obstacle_rect_list = []  # kommer innehålla alla obstacles-rektanglar

# Sky
sky_surface = pygame.image.load('graphics/Sky.png').convert()  # surface - Sky.png

# Ground
ground_surface = pygame.image.load('graphics/ground.png').convert()  # surface - ground.png


# Groups

player = pygame.sprite.GroupSingle()
player.add(Player())





# # # Obstacle Animation # # #
# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # frame - snail1.png
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()  # frame - snail2.png
snail_frames = [snail_frame_1, snail_frame_2]  # lista av frames
snail_index = 0 # start index
snail_surf = snail_frames[snail_index]  # surface = indexet vi är på i listan

# Fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()  # frame - fly1.png
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()  # frame - fly2.png
fly_frames = [fly_frame1, fly_frame2]  # lista av frames
fly_index = 0  # start index
fly_surf = fly_frames[fly_index]  # surface = indexet vi är på i listan
# ---------------------------

# # #  Player & Animation surfaces # # #
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()  # surface - player_walk_1.png
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()  # surface - player_walk_2.png
player_walk = [player_walk_1, player_walk_2]  # lista av alla bilder vi vill animera

player_index = 0  # indexet byter mellan walk_1 och walk_2 så den byter mellan 0 & 1 konstant

player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()  # Laddar in bilden jump.png
player_surf = player_walk[player_index]  # Player_surf ändras hela tiden baserat på vilket index vi ligger i
# ---------------------------
player_rect = player_surf.get_rect(midbottom=(100, 300))  # skapar rektangel som man kan styra

player_gravity = 0  # variabeln för att kontrolera hur hög player ska hoppa

# Sido rörelser för spelaren med piltangenterna
moving_right = False
moving_left = False

# intro screen
player_stand_rotate = 0  # Börjar att visa bilden utan någon rotation
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()  # Surface - player_stand

game_name = test_font.render("Pixel runner", False, (111, 196, 169))  # Text surface - game_name
game_name_rect = game_name.get_rect(center=(400, 50))  # text rect - game_name

game_message = test_font.render("Press space to run", False, (111, 196, 169))  # text surface - game_message
game_message_rect = game_message.get_rect(center=(400, 350))  # text rect - game_message

# Score
score = 0


# # # Obstacle_timer - Custom USEREVENT # # #
# https://coderslegacy.com/python/pygame-userevents/

obstacle_timer = pygame.USEREVENT + 1  # nytt custom event

pygame.time.set_timer(obstacle_timer, 1500)  # skapar en timer som kör obstacle_timer var 1500 milli-sekund

snail_animation_timer = pygame.USEREVENT + 2  # nytt custom event
pygame.time.set_timer(snail_animation_timer, 300)  # kör denna varje 300 millisekund

fly_animation_timer = pygame.USEREVENT + 3  # nytt custom event
pygame.time.set_timer(fly_animation_timer, 200)  # kör denna varje 200 millisekund

# # # # # GAME LOOP # # # # #
while True:
    # Allt inuti denna while loopen uppdateras på skärmen varje sekund

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Om knappen [x] klickas så gör följande:
            pygame.quit()  # Stäng av pygame
            exit()  # Stäng ner hela python filen

        if game_active:
            # if event.type == pygame.MOUSEBUTTONDOWN:  # Klicka med musen
            #     if player_rect.collidepoint(event.pos):  # om player_rect träffas av positionen av musen
            #         player_gravity = -20  # hoppa upp
            if event.type == pygame.KEYDOWN:  # om knappen har tryckts ner
                if event.key == pygame.K_RIGHT: moving_right = True  # right_arrow down
                if event.key == pygame.K_LEFT: moving_left = True  # left_arrow down

                if event.key == pygame.K_SPACE:  # Om mellanslags tangenten har tryckts
                    if player_rect.bottom >= 300:  # hoppa med mellandslag,
                        player_gravity = -17  # hoppa upp 20px från player står

            if event.type == pygame.KEYUP:  # om någon tangent har släppts upp
                if event.key == pygame.K_RIGHT: moving_right = False  # right_arrow down
                if event.key == pygame.K_LEFT: moving_left = False  # left_arrow up

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # slå på mellanslag för att starta om game
                game_active = True  # kör game igen
                start_time = int(pygame.time.get_ticks() / 1000)  # spara tiden av sista gång
        if game_active:
            if event.type == obstacle_timer:  # om obstacle timer har hänt
                if randint(0, 2):  # random nummer mellan 0 - 2
                    # om 1 eller 2 || True
                    # skicka ut en snigel
                    # appenda en ny snigel rektangel med x värde mellan 800 - 1100 och på y värde 300
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(800, 1100), 300)))
                else:
                    # om 0 || False
                    # skicka ut fluga
                    # appenda en ny fluga rektangel med x värde mellan 800 - 1100 och på y värde 210
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(800, 1100), 210)))

            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surf = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]


    if game_active:
        screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1
        screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2
        score = display_score()  # Sätter retur värdet av funktionen till score

        # player
        player.draw(screen)
        player.update()
        
        
        
        
        player_gravity += 1  # ökar y axelns värde med 1 hela tiden
        player_rect.y += player_gravity  # sätter y värdet till det som gravity är
        if player_rect.bottom >= 300:  # efter player hoppade och trilla ned, vi kontrollerar om att stå på ground surface
            player_rect.bottom = 300
        player_surf, player_index = player_animation(player_surf, player_index)  # byter walking / jumping bild på player surf innan den visas på skärmen
        screen.blit(player_surf, player_rect)  # Sätter spelaren på skärmen med positionen av player_rect

        # player not walking out of frame
        if player_rect.left < 0: player_rect.left = 0  # om spelaren är utanför vänstra sidan av skärmen
        if player_rect.right > 800: player_rect.right = 800  # om spelaren är utanför högra sidan av skärmen

        # player walking movement speed
        if moving_right: player_rect[0] += 4  # hastighet för att gå höger
        if moving_left: player_rect[0] -= 4  # hastighet för att gå vänster

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)  # returnerar en ny lista med alla obsticles att visa på skärmen

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)  # returnerar ett bool värde till game_active

    if not game_active:
        screen.fill((94, 129, 162))  # fyll skärmen med färg

        # Player stand
        player_stand_rotate += 2  # Ökar rotationen av bilden
        player_stand_rotozoom = pygame.transform.rotozoom(player_stand, player_stand_rotate, 2)  # tar en surface och roterar & förstorar bilden
        player_stand_rect = player_stand_rotozoom.get_rect(center=(400, 200))
        screen.blit(player_stand_rotozoom, player_stand_rect)  # lägg in player stand i rektangel positionen

        # Återställ variablarna
        obstacle_rect_list.clear()  # töm listan av alla obstacles
        player_rect.midbottom = (80, 300)  # placera spelaren på plats 80, 300
        player_gravity = 0  # resetta spelarens gravity

        # End screen - Score / Message
        score_message = test_font.render(f"Score: {score}", False, (111, 196, 169))  # visar antalet score
        score_message_rect = score_message.get_rect(center=(400, 50))  # rektanglen av score + placering

        if score == 0:  # om score är 0
            screen.blit(game_name, game_name_rect)  # Namnet på spelet
            game_instruction = test_font.render('Press space to play', False, (111, 196, 169))  # meddelande om score är 0
        else:  # om score inte är 0
            screen.blit(score_message, score_message_rect)  # lägg score meddelandet på skärmen
            game_instruction = test_font.render('Press space to play again', False, (111, 196, 169))  # meddelande om score inte är 0

        game_instruction_rect = game_instruction.get_rect(center=(400, 350))
        screen.blit(game_instruction, game_instruction_rect)  # lägg meddelandet att starta om spelet



    pygame.display.update()  # uppdaterar skärmen [pygame window]
    clock.tick(60)  # hur snabb program kör [60 fps]
