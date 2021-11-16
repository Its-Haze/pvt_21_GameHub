import pygame  # importera pygame packet
from sys import exit  # importera funtion exit from modul sys

pygame.init()  # initsera pygame
screen = pygame.display.set_mode((800, 400))  # rita en pygame fönster
clock = pygame.time.Clock()  # raknar pygame init

sky_surface = pygame.image.load('graphics/Sky.png')  # loading en fil som bild
ground_surface = pygame.image.load('graphics/ground.png')

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # loading en font
test_font1 = pygame.font.get_default_font()

text_surface = test_font.render('Tetris', False, 'Black')
text_rectangle = text_surface.get_rect(midtop=(400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png')
snail_x_pos = 600


player_surf = pygame.image.load('graphics/Player/player_walk_1.png')
player_rect = player_surf.get_rect(midbottom=(100, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, text_rectangle)
    snail_x_pos -= 4
    if snail_x_pos < 0:
        snail_x_pos = 800

    snail_rect = snail_surface.get_rect(midbottom=(snail_x_pos, 300))
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surf, player_rect)
    pygame.display.update()
    clock.tick(60)  # hur snabb program kör
