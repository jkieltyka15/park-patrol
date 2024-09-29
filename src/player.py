import pygame
import os

# local libraries
import constants as const
import utility as util

# sprite assets
SPRITE_RANGER_RACHEL = os.path.join(const.ASSET_DIR, "ranger-rachel.png")

# player class
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.image.load(SPRITE_RANGER_RACHEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)
        self.speed = 8


    def move(self, dx, dy):

        # calculate new position
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # check for collision
        if not util.check_collision(new_rect):
            self.rect = new_rect
        
        # prevent moving off-screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.right > const.MAP_WIDTH * const.TILE_SIZE:
            self.rect.right = const.MAP_WIDTH * const.TILE_SIZE

        if self.rect.bottom > const.MAP_HEIGHT * const.TILE_SIZE:
            self.rect.bottom = const.MAP_HEIGHT * const.TILE_SIZE