import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height, type):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height
        self.type = type
        self.pow = 1

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            # print("Killed")
            self.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height, type):
        super().__init__()
        self.image = pygame.Surface((8, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height
        self.type = type
        self.pow = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            # print("Killed")
            self.kill()


class Beam(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height, type):
        super().__init__()
        self.image = pygame.Surface((3, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.screen_height = screen_height
        self.type = type
        self.pow = 1

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 0:
            # print("Killed")
            self.kill()

# cont. in slide 21/28!
