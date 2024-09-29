import pygame
import os

# local libraries
import constants as const

# sprite assets
SPRITE_POND = os.path.join(const.ASSET_DIR, "pond.png")

# lake class
class Pond(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image = pygame.image.load(SPRITE_POND)

        # scale images
        scale = 2.4
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() * scale, self.image.get_height() * scale))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)
