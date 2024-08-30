import pygame, random

from laser import Laser, Missile, Beam
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from alien import MysteryShip


class Game:

    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lives = 3
        self.run = True
        self.offset = offset
        # create group to hold spaceship
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.total_alien = 0
        self.wave = 1
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.current_mystery_ship = None
        self.score = 0
        self.highscore = 0
        self.boss = 0
        self.load_highscore()
        pygame.mixer.music.load("Sound/suckerpunch.ogg")
        pygame.mixer.music.play(-1)
        self.explosion_sound = pygame.mixer.Sound("Sound/explosion.ogg")

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []

        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)

        return obstacles

    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                # determines type of alien based on row
                if row == 0:
                    if self.wave >= 20 or self.wave % 4 == 0:
                        alien_type = 5
                    else:
                        alien_type = 3
                elif row in (1, 2):
                    if self.wave >= 15 or self.wave % 3 == 0:
                        alien_type = 4
                    else:
                        alien_type = 2
                else:
                    if self.wave >= 25 or self.wave % 5 == 0:
                        alien_type = 6
                    else:
                        alien_type = 1
                self.total_alien += 1
                alien = Alien(alien_type, x + self.offset / 2, y)
                # alien = Alien(alien_type, x, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()

        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            if random_alien.type == 4:
                missile_sprite = Missile(random_alien.rect.center, -2, self.screen_height, "missile")
                self.alien_lasers_group.add(missile_sprite)
            elif random_alien.type == 5:
                beam_sprite = Beam(random_alien.rect.center, -10, self.screen_height, "beam")
                self.alien_lasers_group.add(beam_sprite)
            else:
                laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height, "laser")
                self.alien_lasers_group.add(laser_sprite)
        if self.mystery_ship_group.sprites():
            event_ship = random.choice(self.mystery_ship_group.sprites())
            if self.current_mystery_ship.form == "missile":
                laser_sprite = Laser(event_ship.rect.center, -6, self.screen_height, "laser")
                self.alien_lasers_group.add(laser_sprite)
            elif self.current_mystery_ship.form == "ufo":
                beam_sprite = Beam(event_ship.rect.center, -10, self.screen_height, "beam")
                self.alien_lasers_group.add(beam_sprite)
            # elif self.current_mystery_ship.form == "boss":
            #     missile_sprite = Missile(event_ship.rect.center, -2, self.screen_height, "missile")
            #     self.alien_lasers_group.add(missile_sprite)

    def create_mystery_ship(self, form):
        # Create a new mystery ship
        mystery_ship = MysteryShip(self.screen_width, self.offset, form)
        # Add the mystery ship to the group
        self.mystery_ship_group.add(mystery_ship)
        self.current_mystery_ship = mystery_ship
        print("Created Mystery Ship")

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            # add high-score to text file
            # w = write
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            # r = read
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        # if no high-score is found then we set high-score to 0
        except FileNotFoundError:
            self.highscore = 0

    def check_for_collisions(self):
        # Spaceship
        if self.spaceship_group.sprite.lasers_group:

            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                # awards the player 100 points if alien is hit
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, False)
                if aliens_hit:
                    for alien in aliens_hit:
                        alien.take_damage(1)
                        if alien.HP <= 0:
                            alien.kill()
                            self.explosion_sound.play()
                            self.score += alien.type * 100
                            self.check_for_highscore()
                            self.total_alien -= 1
                            print(self.total_alien, " aliens left!")
                        laser_sprite.kill()
                # if pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True):
                #     laser_sprite.kill()
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, False):
                    if self.current_mystery_ship:
                        # Take damage
                        self.current_mystery_ship.take_damage(1)
                        # Check if HP is less than or equal to 0
                        if self.current_mystery_ship.HP <= 0:
                            # If HP is 0 or less, kill the MysteryShip
                            if self.current_mystery_ship.form == "missile":
                                self.score += 5000
                            elif self.current_mystery_ship.form == "ufo":
                                self.score += 10000
                            elif self.current_mystery_ship.form == "boss":
                                self.score += 50000
                            else:
                                self.score += 1000
                            if 0 <= self.lives < 3:
                                self.lives += 1
                            self.explosion_sound.play()
                            self.check_for_highscore()
                            self.current_mystery_ship.kill()
                            print("Mystery Ship killed!")
                    laser_sprite.kill()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, False):
                        laser_sprite.kill()

        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    print("Spaceship Hit!")
                    self.lives -= 1
                    if self.lives < 0:
                        self.game_over()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.pow -= 1
                        if laser_sprite.pow <= 0:
                            laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
                    if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                        print("Spaceship Hit!")
                        self.lives -= 1
                        if self.lives < 0:
                            self.game_over()

        if self.total_alien <= 0 and self.run == True:
            self.wave += 1
            print("Wave Cleared!", " Moving to Wave ", self.wave)
            self.score += (1000 * self.wave)
            if 0 <= self.lives < 3:
                self.lives += 1
            if self.wave % 3 == 0:
                self.obstacles = self.create_obstacles()
            self.create_aliens()

    def game_over(self):
        print("Game Over!")
        self.wave = 1
        self.total_alien = 0
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0
