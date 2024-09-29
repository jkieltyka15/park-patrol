import pygame
import os

# local libraries
import constants as const
import utility as util

# sprite assets
SPRITE_LITTER_BUG_L = os.path.join(const.ASSET_DIR, "litterbug_left.png")
SPRITE_LITTER_BUG_R = os.path.join(const.ASSET_DIR, "litterbug_right.png")

# player class
class Litterbug(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image_player_left = pygame.image.load(SPRITE_LITTER_BUG_L)
        self.image_player_right = pygame.image.load(SPRITE_LITTER_BUG_R)

        self.image = self.image_player_right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)

        self.speed = 4


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

        # make litterbug sprite face direction of travel
        if dx == const.LEFT:
            self.image = self.image_player_left

        elif dx == const.RIGHT:
            self.image = self.image_player_right