import pygame
import os

# local libraries
import constants as const

# sprite assets
SPRITE_TREE_GOOD = os.path.join(const.ASSET_DIR, "tree.png")
SPRITE_TREE_STUMP = os.path.join(const.ASSET_DIR, "tree_stump.png")
SPRITE_TREE_FIRE = os.path.join(const.ASSET_DIR, "tree_fire.png")

# tree class
class Tree(pygame.sprite.Sprite):

    def __init__(self, start_state, x, y):

        super().__init__()

        self.image_tree_good = pygame.image.load(SPRITE_TREE_GOOD)
        self.image_tree_stump = pygame.image.load(SPRITE_TREE_STUMP)
        self.image_tree_fire = pygame.image.load(SPRITE_TREE_FIRE)

        # scale images
        scale_good = 0.6
        self.image_tree_good = pygame.transform.scale(self.image_tree_good,
                                                      (self.image_tree_good.get_width() * scale_good,
                                                       self.image_tree_good.get_height() * scale_good))

        scale_stump = 0.1
        self.image_tree_stump = pygame.transform.scale(self.image_tree_stump,
                                                      (self.image_tree_stump.get_width() * scale_stump,
                                                       self.image_tree_stump.get_height() * scale_stump))
        
        scale_fire = 0.6
        self.image_tree_fire = pygame.transform.scale(self.image_tree_fire,
                                                      (self.image_tree_fire.get_width() * scale_fire,
                                                       self.image_tree_fire.get_height() * scale_fire))

        # determine tree start state
        if start_state == const.TREE_STUMP:
            self.image = self.image_tree_stump

        elif start_state == const.TREE_ON_FIRE:
            self.image = self.image_tree_fire

        else:
            self.image = self.image_tree_good

        self.state = start_state

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)


    def change_state(self, new_state):

        if new_state == const.TREE_STUMP:
            self.image = self.image_tree_stump

        elif new_state == const.TREE_ON_FIRE:
            self.image = self.image_tree_fire

        elif new_state == const.TREE_GOOD:
            self.image = self.image_tree_good