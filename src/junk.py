import pygame
import os

# local libraries
import constants as const

# sprite assets
SPRITE_JUNK = os.path.join(const.ASSET_DIR, "junk.png")

# junk class
class Junk(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.image.load(SPRITE_JUNK)

        # scale images
        scale = 0.2
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() * scale, self.image.get_height() * scale))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)
