import pygame  # importera pygame packet
from sys import exit  # importera function exit from modul sys
from random import randint, choice
from high_score import high_score

# https://youtu.be/AY9MnQ4x3zk?t=13381
from input_box import InputBox


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [pygame.image.load(f'Runner_folder/graphics/player/player_walk_{i}.png').convert_alpha() for i in range(1, 3)]  # lista av de alla frames
        self.player_index = 0  # start index
        self.player_jump = pygame.image.load('Runner_folder/graphics/player/jump.png').convert_alpha()  # surface - jump

        self.image = self.player_walk[self.player_index]  # image = listan med indexed [player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.game_active = True
        self.moving = False  # om piltangenterna klickas så blir denna True, annars False

    def player_move(self):
        if self.game_active:  # om game active är True
            keys = pygame.key.get_pressed()  # få en lista av alla keys som går att klicka
            if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # om mellanslaget trycks och spelaren är på y_300
                self.gravity = -17  # hoppa med -17 pixlar från marken
            # player not walking out of frame
            if self.rect.left < 0:  # om gubben är för nära vänstra kanten av skärmen
                self.rect.left = 0  # få den att stanna på vänstra sidan
            if self.rect.right > 800:  # om gubben är för nära högra kanten av skärmen
                self.rect.right = 800  # få den att stanna på högra sidan

            self.moving = False  # sätt den till false varje gång vi kör uppdaterar player_move

            # player walking movement speed
            if keys[pygame.K_RIGHT]:  # om högra piltangenten klickas
                self.rect.x += 6  # hastighet för att gå höger
                self.moving = True

            if keys[pygame.K_LEFT]:  # om vänstra piltangenten klickas
                self.rect.x -= 6  # hastighet för att gå vänster
                self.moving = True

    def apply_gravity(self):
        self.gravity += 1  # ökar y axelns värde med 1 hela tiden
        self.rect.y += self.gravity  # sätter y värdet till det som gravity är
        if self.rect.bottom >= 300:  # om rektangelns nedre del är mindre eller lika med 300
            self.rect.bottom = 300  # sätt rektangelns bottom till 300

    def animation_state(self):
        """ Play walking animation if player is on floor, or jump animation if not on floor"""
        if self.rect.bottom < 300:  # om spelaren inte är på marken
            self.image = self.player_jump  # sätt image till player_jump
        else:
            if self.moving:  # om spelaren går antingen höger eller vänster
                self.player_index += 0.1  # öka indexed med 0.1
                if self.player_index >= len(self.player_walk):  # om indexed är större än listans längd
                    self.player_index = 0  # sätt tillbaka indexet till 0
                self.image = self.player_walk[int(self.player_index)]  # sätt image till int(indexed) av listan
            else:
                self.image = self.player_walk[0]  # om spelaren inte rör sig

    def player_x_pos(self):
        return self.rect.x

    def update(self):
        """ Update the methods of the class """
        self.player_move()  # Update player_move
        self.apply_gravity()  # Update apply_gravity
        self.animation_state()  # Update animation state


class Obstacle(pygame.sprite.Sprite):  # Skapa en obstacle klass
    def __init__(self, type, player_pos_x):  # initiera klassen och lägg in en sträng vad obstacle heter
        super().__init__()  # initiera pygame.sprite.Sprite
        self.type = type
        self.player_pos_x = player_pos_x
        if self.type == "fly":  # om obstacle är fly
            self.frames = [pygame.image.load(f"Runner_folder/graphics/Fly/Fly{i}.png").convert_alpha() for i in range(1, 3)]
            y_pos = 210  # start positionen - Höjden på obstacle
            x_pos = randint(800, 1100)

        elif self.type == "snail":  # om obstacle är snail
            self.frames = [pygame.image.load(f"Runner_folder/graphics/Snail/snail{i}.png").convert_alpha() for i in range(1, 3)]
            y_pos = 300  # start positionen - Höjden på obstacle
            x_pos = randint(800, 1100)

        elif self.type == "dragon": # om obstacle är dragon
            unscaled_frames = [pygame.image.load(f"Runner_folder/graphics/dragon/Walk{i}.png").convert_alpha() for i in range(1, 6)]
            # skapa en list comprehension som skalar ner alla bildernas storlek med 1,5
            self.frames = [pygame.transform.scale(i, (int(i.get_width() // 1.5), int(i.get_height() // 1.5))) for i in unscaled_frames]
            y_pos = 300  # start positionen - Höjden på obstacle
            x_pos = randint(800, 1100)

        elif self.type == "cat":
            unscaled_cats = [pygame.image.load(f"Runner_folder/graphics/cat/cat_{i}.png").convert_alpha() for i in range(1, 4)]
            # list comprehension som minskar storleken på alla frames
            self.frames = [pygame.transform.scale(i, (int(i.get_width() // 1.2), int(i.get_height() // 1.2))) for i in unscaled_cats]
            y_pos = 300
            x_pos = randint(800, 1100)

        elif self.type == "stone":
            unscaled_stones = [pygame.image.load("Runner_folder/graphics/stone/stone.png").convert_alpha() for i in range(1, 3)]
            self.frames = [pygame.transform.scale(i, (int(i.get_width() // 2), int(i.get_height() // 2))) for i in unscaled_stones]
            y_pos = -20
            # x_pos = nuvarande x position av spelaren och spawna stenen ovanför spelaren
            x_pos = self.player_pos_x + 30

        self.animation_index = 0  # vilket index     som bilden vi är på ska visa
        self.image = self.frames[self.animation_index]  # image = listan av alla bilder med vilket index vi vill visa upp
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))  # rektangeln har ett random x värde och ett y värde

    def animation_state(self):  # metod för att öka indexet så bilden ändras
        self.animation_index += 0.1  # öka hela tiden med 0.1
        if self.animation_index >= len(self.frames):  # kolla om indexet är större eller lika med listans storlek
            self.animation_index = 0  # sätt den tillbaka till 0
        self.image = self.frames[int(self.animation_index)]  # sätt bilden till vad indexet är inuti frames listan

    def update(self):  # sprite.Sprite update metod
        self.animation_state()  # vilken animation vi ska visa
        if self.type != "stone":
            self.rect.x -= 7  # flytta obstacle -7 pixlar
        elif self.type == "stone":
            self.rect.y += 3
        self.destroy()  # kolla om vi är utanför skärmen - DESTROY

    def destroy(self):  # sprite.Sprite destroy metod
        if self.type != "stone":
            if self.rect.x <= -100:  # om obstacle är för långt utanför skärmen
                self.kill()  # ta bort den från obstacle gruppen
        elif self.type == "stone":
            if self.rect.y >= (300 - self.image.get_height()):
                self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self, angle):  # initiera klassen och lägg in en sträng vad obstacle heter
        super().__init__()  # initiera pygame.sprite.Sprite
        self.angle = angle
        #  list comprehension, ladda in alla 8 Frames av fåglarna i deras original storlek
        unscaled_birds = [pygame.image.load(f"Runner_folder/graphics/birds/bird_{i}.png").convert_alpha() for i in range(1, 9)]
        y_pos = 75
        down_scale = 6  # dela höjden / längden på surface med 6
        if self.angle == "Right":
            self.frames = [pygame.transform.scale(i, (int(i.get_width() // down_scale), int(i.get_height() // down_scale))) for i in unscaled_birds]
            x_pos = 900

        elif self.angle == "Left":
            left_unscaled_bird = [pygame.transform.flip(i, True, False) for i in unscaled_birds]
            self.frames = [pygame.transform.scale(i, (int(i.get_width() // down_scale), int(i.get_height() // down_scale))) for i in left_unscaled_bird]
            x_pos = -100
        self.animation_index = 0  # vilket index som bilden vi är på ska visa
        self.image = self.frames[self.animation_index]  # image = listan av alla bilder med vilket index vi vill visa upp
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))  # rektangeln har ett random x värde och ett y värde

    def animation_state(self):  # metod för att öka indexet så bilden ändras 
        self.animation_index += 0.1  # öka hela tiden med 0.1
        if self.animation_index >= len(self.frames):  # kolla om indexet är större eller lika med listans storlek
            self.animation_index = 0  # sätt den tillbaka till 0
        self.image = self.frames[int(self.animation_index)]  # sätt bilden till vad indexet är inuti frames listan

    def update(self):  # sprite.Sprite update metod
        self.animation_state()  # vilken animation vi ska visa
        if self.angle == "Right":
            self.rect.x -= 4  # flytta obstacle -4 pixlar
        elif self.angle == "Left":
            self.rect.x += 4  # fly
        self.destroy()  # kolla om vi är utanför skärmen - DESTROY

    def destroy(self):  # sprite.Sprite destroy metod
        if self.angle == "Right":
            if self.rect.x <= -100:  # om obstacle är för långt utanför skärmen
                self.kill()  # ta bort den från obstacle gruppen
        elif self.angle == "Left":
            if self.rect.x >= 900:
                self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coin_animation_1 = pygame.image.load('Runner_folder/graphics/coins/coin1.png').convert_alpha()
        coin_animation_2 = pygame.image.load('Runner_folder/graphics/coins/coin2.png').convert_alpha()

        self.coin_frames = [coin_animation_1, coin_animation_2]
        self.coin_index = 0
        self.image = self.coin_frames[self.coin_index]
        self.rect = self.image.get_rect(midbottom=(randint(50, 750), 0))

    def animation_coin(self):
        self.coin_index += 0.1
        if self.coin_index > len(self.coin_frames):
            self.coin_index = 0
        self.image = self.coin_frames[int(self.coin_index)]

    def update(self):
        self.animation_coin()
        self.rect.y += 5
        self.destroy()

    def destroy(self):
        if self.rect.y > 250:
            self.kill()


def display_score(start_time, test_font, screen):
    """ visa score av användare """
    current_time = int(pygame.time.get_ticks() / 1000) - start_time  # hur långt det har gått sen pygame.init()
    score_surf = test_font.render(f'Score: {current_time}', False, (255, 255, 102))  # objektet av score
    score_rect = score_surf.get_rect(center=(400, 50))  # rektanglen av objektet score
    screen.blit(score_surf, score_rect)  # skriver ut på skärmen varje gång funktionen körs
    return current_time  # returnera värdet av score


def display_coins(screen, test_font, coins):
    """ visa antal coins av användare"""
    coins_surf = test_font.render(f'Coins: {coins}', False, (255, 255, 102))  # score font
    coins_rect = coins_surf.get_rect(center=(100, 50))
    screen.blit(coins_surf, coins_rect)


def collision_sprite(player, obstacle_group, screen, score, bird_group, coins, player_, user_id):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        # player_.__init__()
        player_.rect.x = 80
        # player.empty()
        # player.add(player_)
        obstacle_group.empty()
        bird_group.empty()
        high_score('runner', screen, user_id, (score, coins), False)
        return False
    else:
        return True


def collision_with_coin_sprite(player, coin_group, bg_sound_coin):
    if pygame.sprite.spritecollide(player.sprite, coin_group, False):
        coin_group.empty()
        bg_sound_coin.play(0)
        return True
    return False


def play_runner():
    from game_hub import start_game_hub
    # # # # Aktivera Pygame # # # #
    pygame.init()  # initiera pygame biblioteket
    pygame.display.set_caption("The insane runner")
    WINDOW_SIZE = (800, 400)
    screen = pygame.display.set_mode(WINDOW_SIZE)  # Skapa ett Pygame fönster (width=800, Height=400)
    clock = pygame.time.Clock()  # Skapar en klocka från att pygame.init() kördes
    pygame.time.Clock()
    game_active = False  # variabeln för att kolla om game ska köra
    start_time = 0  # variabel att spara senast tiden

    # Sound
    bg_sound_game = pygame.mixer.Sound('Runner_folder/audio/music.mp3')
    bg_sound_lobby = pygame.mixer.Sound('Runner_folder/audio/lobby.wav')
    bg_sound_death = pygame.mixer.Sound('Runner_folder/audio/death.mp3')
    bg_sound_coin = pygame.mixer.Sound('Runner_folder/audio/coin.wav')
    bg_sound_game.set_volume(0.1)
    bg_sound_lobby.set_volume(0.05)
    bg_sound_death.set_volume(0.1)
    bg_sound_coin.set_volume(0.1)
    bg_sound_lobby.play(-1)

    coins = 0

    # # # # Surface, Rektanglar & Fonts # # # #

    # Font
    test_font = pygame.font.Font('Runner_folder/font/Pixeltype.ttf', 50)  # loading en font

    # Obstacles - kommer innehålla alla sniglar och flugor som har spawnats

    # Sky
    sky_surface = pygame.image.load('Runner_folder/graphics/Sky.png').convert()  # surface - Sky.png

    # Ground
    ground_surface = pygame.image.load('Runner_folder/graphics/ground.png').convert()  # surface - ground.png

    # Background Forest
    background_list = [pygame.image.load('Runner_folder/graphics/background/Cartoon_Forest_BG_01.png').convert_alpha(),
                       pygame.image.load('Runner_folder/graphics/background/Cartoon_Forest_BG_02.png').convert_alpha(),
                       pygame.image.load('Runner_folder/graphics/background/Cartoon_Forest_BG_03.png').convert_alpha(),
                       pygame.image.load('Runner_folder/graphics/background/Cartoon_Forest_BG_04.png').convert_alpha()]

    forest_surface = background_list[randint(0, len(background_list) - 1)]  # Laddar in bilden Forest1.png

    # Groups
    player_ = Player()
    player = pygame.sprite.GroupSingle()
    player.add(player_)

    obstacle_group = pygame.sprite.Group()

    coin_group = pygame.sprite.Group()

    bird_group = pygame.sprite.Group()

    # intro screen
    player_stand_rotate = 0  # Börjar att visa bilden utan någon rotation
    player_stand = pygame.image.load("Runner_folder/graphics/Player/player_stand.png").convert_alpha()  # Surface - player_stand

    game_name = test_font.render("Pixel runner", False, (111, 196, 169))  # Text surface - game_name
    game_name_rect = game_name.get_rect(center=(400, 50))  # text rect - game_name

    go_back_btn = pygame.image.load('Runner_folder/graphics/end_screen/home_button.png').convert_alpha()
    downscaled_go_back_btn = pygame.transform.scale(go_back_btn, ((go_back_btn.get_width() // 4), (go_back_btn.get_height() // 4)))
    go_back_surf_rect = downscaled_go_back_btn.get_rect(bottomleft=(20, 380))

    leaderboard_surf = pygame.image.load('Runner_folder/graphics/end_screen/button_small_leaderboard.png').convert_alpha()  # Surface - leaderboard
    leaderboard_surf_rect = leaderboard_surf.get_rect(topright=(780, 20))

    # Score
    score = 0
    test_timer = 0

    # # # Obstacle_timer - Custom USEREVENT # # #
    # https://coderslegacy.com/python/pygame-userevents/

    obstacle_timer = pygame.USEREVENT + 1  # nytt custom event

    pygame.time.set_timer(obstacle_timer, 1600)  # skapar en timer som kör obstacle_timer var 1500 milli-sekund

    snail_animation_timer = pygame.USEREVENT + 2  # nytt custom event
    pygame.time.set_timer(snail_animation_timer, 300)  # kör denna varje 300 millisekund

    fly_animation_timer = pygame.USEREVENT + 3  # nytt custom event
    pygame.time.set_timer(fly_animation_timer, 200)  # kör denna varje 200 millisekund

    coin_timer = pygame.USEREVENT + 4  # Vi skapar en timer för att välja hur ofta bilden på coin skall bytas ut - detta skapar en animering
    pygame.time.set_timer(coin_timer, 4000)

    bird_timer = pygame.USEREVENT + 5
    pygame.time.set_timer(bird_timer, 6000)

    input_box = InputBox(100, 100, 140, 32, (64, 64, 64), (96, 96, 96))
    user_id = ''
    done = False
    is_first_time = True
    game_over = False

    # # # # # GAME LOOP # # # # #
    while True:
        player_rect_x_pos = player_.player_x_pos()
        # Allt inuti denna while loopen uppdateras på skärmen varje sekund
        if is_first_time:
            text_register = test_font.render("Username", True, 'Black')
            screen.blit(text_register, [100, 60])
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:  # Klicka med musen
                        if leaderboard_surf_rect.collidepoint(
                                event.pos):  # om player_rect träffas av positionen av musen
                            print("clicked the leaderboard!")
                            high_score('runner', screen, user_id, (score, coins), True)
                        if go_back_surf_rect.collidepoint(event.pos):
                            bg_sound_lobby.stop()
                            start_game_hub()

                    user_id = input_box.handle_event(event)
                    screen.fill((94, 129, 162))
                    screen.blit(text_register, [100, 60])
                    input_box.update()
                    input_box.draw(screen)
                    if user_id:
                        user_id = str(user_id).lower().strip()
                        done = True
                # leaderboard button
                screen.blit(leaderboard_surf, leaderboard_surf_rect)

                # Go back to game hub button
                screen.blit(downscaled_go_back_btn, go_back_surf_rect)
                pygame.display.flip()
            is_first_time = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Om knappen [x] klickas så gör följande:
                pygame.quit()  # Stäng av pygame
                exit()  # Stäng ner hela python filen

            if game_active:
                if event.type == obstacle_timer:  # om obstacle timer har hänt
                    obstacle_group.add(Obstacle(choice(["fly", "snail", "dragon", "cat", "stone", "stone", "stone"]), player_rect_x_pos))
                if event.type == bird_timer:
                    bird_group.add(Bird(choice(["Left", "Right"])))

                if event.type == coin_timer:
                    coin_group.add(Coin())

                if event.type == pygame.KEYDOWN:  # om knappen har tryckts ner
                    if event.key == pygame.K_ESCAPE:
                        print("ESC")
                        bg_sound_lobby.stop()
                        start_game_hub()

            if not game_active:

                if event.type == pygame.MOUSEBUTTONDOWN:  # Klicka med musen
                    if leaderboard_surf_rect.collidepoint(event.pos):  # om player_rect träffas av positionen av musen
                        print("clicked the leaderboard!")
                        high_score('runner', screen, user_id, (score, coins), True)
                    if go_back_surf_rect.collidepoint(event.pos):
                        bg_sound_lobby.stop()
                        start_game_hub()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # slå på mellanslag för att starta om game
                        game_active = True  # kör game igen
                        start_time = int(pygame.time.get_ticks() / 1000)  # spara tiden av sista gång
                        #test_timer = int(pygame.time.get_ticks() / 1000)
                        coins = coins - coins
                    if event.key == pygame.K_ESCAPE:
                        bg_sound_lobby.stop()
                        start_game_hub()

        if game_active:

            screen.blit(sky_surface, (0, 0))  # sätter himlen på skärmen  - Lager 1
            screen.blit(forest_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))  # sätter marken på skärmen  - Lager 2

            score = display_score(start_time, test_font, screen)  # Sätter retur värdet av funktionen till score

            # player group single
            player.draw(screen)
            player.update()

            # Obstacle Group
            obstacle_group.draw(screen)
            obstacle_group.update()

            # Coin Group
            coin_group.draw(screen)
            coin_group.update()
            # Bird Group
            bird_group.draw(screen)
            bird_group.update()

            if collision_with_coin_sprite(player, coin_group, bg_sound_coin):
                # bg_sound_coin.play(0)
                coins += 1

            display_coins(screen, test_font, coins)

            # Collision
            game_active = collision_sprite(player, obstacle_group, screen, score, bird_group, coins, player_, user_id)

        if not game_active:
            player_rect_x_pos = player_.player_x_pos()
            screen.fill((94, 129, 162))  # fyll skärmen med färg


            # leaderboard button
            screen.blit(leaderboard_surf, leaderboard_surf_rect)

            # Go back to game hub button
            screen.blit(downscaled_go_back_btn, go_back_surf_rect)

            # Player stand
            player_stand_rotate += 2  # Ökar rotationen av bilden
            player_stand_rotozoom = pygame.transform.rotozoom(player_stand, player_stand_rotate, 2)  # tar en surface och roterar & förstorar bilden
            player_stand_rect = player_stand_rotozoom.get_rect(center=(400, 200))
            screen.blit(player_stand_rotozoom, player_stand_rect)  # lägg in player stand i rektangel positionen
            forest_surface = background_list[randint(0, len(background_list) - 1)]


            # coins score:
            if coins != 0:
                display_coins(screen, test_font, coins)

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


if __name__ == '__main__':
    play_runner()
