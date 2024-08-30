import pygame
import random
import game


# 4/16/24: left off at workshop 5 slide 21/43

class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        # type of alien to make image path to
        path = f"Graphics/alien_{type}.png"
        if type == 6:
            self.HP = 3
        else:
            self.HP = 1
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def take_damage(self, damage):
        self.HP -= damage

    def update(self, direction):
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, offset, form):
        super().__init__()

        self.offset = offset

        self.screen_width = screen_width

        self.form = form

        path = f"Graphics/{form}.png"

        self.image = pygame.image.load(path)

        if form == "mystery":
            self.HP = 3
        elif form == "missile":
            self.HP = 5
        elif form == "ufo":
            self.HP = 7
        elif form == "boss":
            self.HP = 50

        x = random.choice([self.offset / 2, screen_width + self.offset - self.image.get_width()])

        if x == self.offset / 2:
            self.speed = 1
        else:
            self.speed = -1

        self.rect = self.image.get_rect(topleft=(x, 40))

    def take_damage(self, damage):
        self.HP -= damage
        print("Mystery Ship has ", self.HP, " HP left!")

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.screen_width:
            self.kill()
        elif self.rect.left < 0:
            self.kill()
