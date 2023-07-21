import pygame
import random
from sys import exit


# Display Score
def display_score():
    current_time = int((int(pygame.time.get_ticks())) / 1000)
    score_surface = font.render(f'{current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center=(640, 80))
    screen.blit(score_surface, score_rect)


# Main
window_height = 720
window_width = 1280
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()
game_active = True
game_start = False
font = pygame.font.Font('rainyhearts.ttf', 72)
font_small = pygame.font.Font('rainyhearts.ttf', 30)

# Background
background = pygame.image.load('Graphics/Main/Environment/bg_grasslands.png').convert()
background = pygame.transform.scale(background, (1280, 720))
ground = pygame.image.load('Graphics/Main/Environment/Ground.png')

# Enemies
slime_surface = pygame.image.load('Graphics/Main/Enemies/Slime/slimeGreen.png').convert_alpha()
slime_rect = slime_surface.get_rect(midbottom=(1200, 580))

# Player
player_surface = pygame.image.load('Graphics/Main/Player/alienPink_walk1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(150, 580))
player_gravity = 0

# Start Screen
title = font.render('PLATFORMER', False, (16, 167, 209))
title_rect = title.get_rect(center=(640, 100))
player_idle = pygame.image.load('Graphics/Main/Player/alienPink.png').convert_alpha()
player_idle = pygame.transform.scale2x(player_idle)
player_idle_rect = player_idle.get_rect(center=(640, 360))
press_space = font.render('Press SPACE To Start', False, 'White')
press_space_rect = press_space.get_rect(center=(640, 600))

# Game Over
game_over = font.render('Game Over', False, 'White')
game_over_rect = game_over.get_rect(center=(640, 360))

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 580 and game_start:
                player_gravity = -20
            if event.key == pygame.K_SPACE and not game_start:
                game_start = True

    if game_active:
        if not game_start:
            screen.fill((227, 216, 16))
            screen.blit(player_idle, player_idle_rect)
            screen.blit(title, title_rect)
            screen.blit(press_space, press_space_rect)

        if game_start:
            screen.blit(background, (0, 0))
            screen.blit(ground, (0, 580))
            display_score()
            slime_rect.x -= 4
            if slime_rect.left < -50: slime_rect.x = 1300
            screen.blit(slime_surface, slime_rect)

            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 580:
                player_rect.bottom = 580

            screen.blit(player_surface, player_rect)

            if slime_rect.colliderect(player_rect):
                game_active = False

    else:
        screen.fill('Black')
        screen.blit(game_over, game_over_rect)

    pygame.display.update()
    clock.tick(60)
