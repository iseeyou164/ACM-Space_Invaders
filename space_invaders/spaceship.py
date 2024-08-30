import pygame
from laser import Laser


# create class (which will be child of Sprite class)
class Spaceship(pygame.sprite.Sprite):

    # create init to initializes spaceship object
    def __init__(self, screen_width, screen_height, offset):
        # inherits all attributes and methods of sprite class
        # calls constructor of parent sprite class
        super().__init__()

        # attributes for screen size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        # load image file of file directory for visual appearance of ship
        self.image = pygame.image.load("Graphics/spaceship.png")

        # create default rectangular region (rect object) for position of spaceship
        # takes argument for the position of the spaceship (middle bottom of screen)
        # self.rect = self.image.get_rect(midbottom=(self.screen_width / 2, self.screen_height))
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2, self.screen_height))

        # speed attribute to control speed of object movement
        self.speed = 6

        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300

        # load sounds
        self.laser_sound = pygame.mixer.Sound("Sound/laser.ogg")

    # create method for user input
    def get_user_input(self):
        # get list of all keys that are pressed
        keys = pygame.key.get_pressed()

        # check if Left or Right arrow keys are pressed
        if keys[pygame.K_RIGHT]:
            # change x-axis value of rect to make it move right
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            # change x-axis value of rect to make it move left
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height, "laser")
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            # call sound play method
            self.laser_sound.play()

    # create update method to be called for every frame and update each frame
    def update(self):
        # update user input method
        self.get_user_input()
        # update constrain movement method
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    # create method to constrain movement of spaceship when it goes left to right
    def constrain_movement(self):

        # checks if the spaceship moved passed the boundaries (too far to the right)
        if self.rect.right > self.screen_width:
            # reposition inside window
            self.rect.right = self.screen_width
        # checks if the spaceship is passed the boundaries on the left side
        if self.rect.left < 0:
            # reposition inside window
            self.rect.left = 0

        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def reset(self):
        self.rect = self.image.get_rect(midbottom=((self.screen_width + self.offset) / 2, self.screen_height))
        # delete all the lasers the spaceship has fired
        self.lasers_group.empty()
