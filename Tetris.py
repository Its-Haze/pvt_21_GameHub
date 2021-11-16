import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_surface = test_font.render('Tetris', False, 'Black')
text_rectangle = text_surface.get_rect(midtop=(400, 50))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, text_rectangle)
    pygame.display.update()
    clock.tick(60)

