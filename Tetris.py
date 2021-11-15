import pygame
from sys import exit



pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
test_surface = pygame.Surface((100, 200))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    screen.fill('WHITE')
    screen.blit(test_surface, (700, 200))
    pygame.display.update()
    clock.tick(60)

