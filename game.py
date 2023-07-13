import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

tsX = 0
tsY = 0
testSurface = pygame.Surface((100, 200))
testSurface.fill("Red")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    screen.blit(testSurface,(tsX,tsY))

    pygame.display.update()
    clock.tick(60)