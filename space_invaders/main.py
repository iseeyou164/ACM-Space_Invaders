import pygame
import sys
import random
from game import Game

pygame.init()

# SCREEN_WIDTH = 750
# SCREEN_HEIGHT = 700

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50
# Add it the offset to screen
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
# add the color that you want to use here
YELLOW = (243, 216, 63)
GREY = (29, 29, 27)

# Create our font
font = pygame.font.Font("Font/monogram.ttf", 40)
# Surface to display our text
wave_surface = font.render("WAVE 1", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("Score", False, YELLOW)
highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)

# give title to screen
pygame.display.set_caption("Python Space Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)
mystery_ship = pygame.USEREVENT + 1
pygame.time.set_timer(mystery_ship, random.randint(4000, 8000))

# keeps running until game is closed
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
        if event.type == mystery_ship and game.run and not game.mystery_ship_group:
            if game.wave >= 30 and game.wave % 3 == 0:
                game.create_mystery_ship("missile")
                pygame.time.set_timer(mystery_ship, random.randint(10000, 14000))
            elif game.wave >= 10 and game.wave % 5 == 0:
                game.create_mystery_ship("ufo")
                pygame.time.set_timer(mystery_ship, random.randint(10000, 14000))
            else:
                game.create_mystery_ship("mystery")
                pygame.time.set_timer(mystery_ship, random.randint(4000, 8000))

            # print(pygame.time)

    # updating
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game.run == False:
        game.reset()

    # change background color
    screen.fill(GREY)

    # Drawing Section (inside the game loop)
    # frame outline
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    # border line to add are spaceship lives at the bottom
    screen.fill(GREY)
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 30)

    if game.run:
        screen.blit(wave_surface, (570, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))

    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50

    # display score
    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))

    # display high-score
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (625, 40, 50, 50))

    fw = "LEVEL: " + str(game.wave)
    formatted_wave = fw.zfill(3)
    wave_surface = font.render(formatted_wave, False, YELLOW)

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)

    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pygame.display.update()

    clock.tick(60)
