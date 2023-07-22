import pygame
import random
from sys import exit


# Display Score
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000)
    score_surface = font.render(f'{current_time}', False, 'Black')
    score_rect = score_surface.get_rect(center=(640, 80))
    screen.blit(score_surface, score_rect)
    return current_time


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 580:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 4

            if enemy_rect.bottom == 580:
                screen.blit(slime_surface, enemy_rect)
            else:
                screen.blit(bat_surface, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > 0]

        return enemy_list
    else:
        return []


def collision(player, enemy_list):
    if enemy_list:
        for enemy in enemy_list:
            if player.colliderect(enemy):
                return False
    return True


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
start_time = 0

# Background
background = pygame.image.load('Graphics/Main/Environment/bg_grasslands.png').convert()
background = pygame.transform.scale(background, (1280, 720))
ground = pygame.image.load('Graphics/Main/Environment/Ground.png')

# Enemy Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 900)

slime_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(slime_animation_timer, 500)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer, 300)

# Enemies
slime_frame_1 = pygame.image.load('Graphics/Main/Enemies/Slime/slimeGreen.png').convert_alpha()
slime_frame_2 = pygame.image.load('Graphics/Main/Enemies/Slime/slimeGreen_walk.png').convert_alpha()
slime_frames = [slime_frame_1, slime_frame_2]
slime_frame_index = 0
slime_surface = slime_frames[slime_frame_index]

bat_frame_1 = pygame.image.load('Graphics/Main/Enemies/Bat/bat.png').convert_alpha()
bat_frame_2 = pygame.image.load('Graphics/Main/Enemies/Bat/bat_fly.png').convert_alpha()
bat_frames = [bat_frame_1, bat_frame_2]
bat_frame_index = 0
bat_surface = bat_frames[bat_frame_index]

enemy_rect_list = []

# Player
player_walk_1 = pygame.image.load('Graphics/Main/Player/alienPink_walk1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics/Main/Player/alienPink_walk2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load('Graphics/Main/Player/alienPink_jump.png').convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(200, 580))
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
score = 0
score_surf = font_small.render(f'Your Score: {score}', False, 'White')
score_surf_rect = score_surf.get_rect(center=(640, 450))
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

        if event.type == enemy_timer and game_active and game_start:
            if random.randint(0, 2):
                enemy_rect_list.append(slime_surface.get_rect(bottomright=(random.randint(1300, 1400), 580)))
            else:
                enemy_rect_list.append(bat_surface.get_rect(midbottom=(random.randint(1300, 1400), 400)))

        if event.type == slime_animation_timer:
            if slime_frame_index == 0:
                slime_frame_index = 1
            else:
                slime_frame_index = 0
            slime_surface = slime_frames[slime_frame_index]

        if event.type == bat_animation_timer:
            if bat_frame_index == 0:
                bat_frame_index = 1
            else:
                bat_frame_index = 0
            bat_surface = bat_frames[bat_frame_index]

    if game_active:
        if not game_start:
            screen.fill((227, 216, 16))
            screen.blit(player_idle, player_idle_rect)
            screen.blit(title, title_rect)
            screen.blit(press_space, press_space_rect)

        if game_start:

            player_animation()
            game_active = collision(player_rect, enemy_rect_list)
            screen.blit(background, (0, 0))
            screen.blit(ground, (0, 580))
            display_score()
            enemy_movement(enemy_rect_list)
            score = display_score()
            score_surf = font_small.render(f'Your Score: {score}', False, 'White')

            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 580:
                player_rect.bottom = 580

            enemy_rect_list = enemy_movement(enemy_rect_list)

            screen.blit(player_surf, player_rect)

    else:
        enemy_rect_list.clear()
        screen.fill('Black')
        screen.blit(game_over, game_over_rect)
        screen.blit(score_surf, score_surf_rect)

    pygame.display.update()
    clock.tick(60)
