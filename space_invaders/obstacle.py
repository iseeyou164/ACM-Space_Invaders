import pygame


# create sprite class (yellow 3x3 pixel)
# combine multiple blocks (like this one) to create obstacle shape

class Block(pygame.sprite.Sprite):
    # create method (constructor)
    # make sure to add x & y

    def __init__(self, x, y):
        super().__init__()

        # since we inherit from sprite class
        # we need image and rect attribute

        # create surface for yellow box (3x3 pixels)
        # .Surface takes a tuple for how many pixels

        self.image = pygame.Surface((3, 3))

        # give square color (yellow)
        self.image.fill((243, 216, 63))

        # create rectangle (rect) for yellow block
        # position block on screen through specific x & y cords
        self.rect = self.image.get_rect(topleft=(x, y))


# create our grid (2d array) to create obstacle shape
# [row][column]
# 0 = empty block
# 1 = yellow block
# 13 sub-lists (rows) and 23 numbers (columns) in each list
grid = [
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
]


# create obstacle class (container for multiple blocks
class Obstacle():
    def __init__(self, x, y):
        self.blocks_group = pygame.sprite.Group()

        for row in range(len(grid)):

            for column in range(len(grid[0])):

                if grid[row][column] == 1:
                    # gives x cord based on column number
                    # since each block is 3x3 we multiply each column by 3
                    pos_x = x + column * 3

                    # gives y cord based on row number
                    # multiply each row by 3 since each block is 3x3 pixels
                    pos_y = y + row * 3

                    # create new block
                    # block class need x & y value to determine where to draw it
                    block = Block(pos_x, pos_y)

                    # add block that was created to the group
                    self.blocks_group.add(block)
