import pygame
import os

# local libraries
import constants as const

# sprite assets
SPRITE_LITTER_BUG_L = os.path.join(const.ASSET_DIR, "litterbug_left.png")
SPRITE_LITTER_BUG_R = os.path.join(const.ASSET_DIR, "litterbug_right.png")

# player class
class Litterbug(pygame.sprite.Sprite):

    def __init__(self, x, y, x_direction, y_direction):

        super().__init__()

        self.image_bug_left = pygame.image.load(SPRITE_LITTER_BUG_L)
        self.image_bug_right = pygame.image.load(SPRITE_LITTER_BUG_R)

        # traveling left first
        if x_direction == const.LEFT:
            self.image = self.image_bug_left

        # traveling right first
        elif x_direction == const.RIGHT:
            self.image = self.image_bug_right

        # traveling vertically first
        else:
            self.image = self.image_bug_right

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)

        self.speed = 4
        direction = (x_direction, y_direction)


    def check_collision(self, rect):

        # convert pixel position to tile indices for all four corners of the player's rect
        corners = [
            (rect.left // const.TILE_SIZE, rect.top // const.TILE_SIZE),        # top-left
            (rect.right // const.TILE_SIZE, rect.top // const.TILE_SIZE),       # top-right
            (rect.left // const.TILE_SIZE, rect.bottom // const.TILE_SIZE),     # bottom-left
            (rect.right // const.TILE_SIZE, rect.bottom // const.TILE_SIZE),    # bottom-right
        ]

        # Check each corner for collision with a walls
        for corner in corners:

            (tile_x, tile_y) = corner

            if (0 <= tile_x < const.MAP_WIDTH) and (0 <= tile_y < const.MAP_HEIGHT):

                # collision detected
                if const.PARK_MAP[tile_y][tile_x] == const.OBSTACLE:
                    return True
                
        return False


    def move(self, dx, dy):

        # calculate new position
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # check for collision
        if not self.check_collision(new_rect):
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
            self.image = self.image_bug_left

        elif dx == const.RIGHT:
            self.image = self.image_bug_right