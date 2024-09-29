import pygame
import os

# local libraries
import constants as const

# sprite assets
SPRITE_RANGER_RACHEL_L = os.path.join(const.ASSET_DIR, "ranger-rachel_left.png")
SPRITE_RANGER_RACHEL_R = os.path.join(const.ASSET_DIR, "ranger-rachel_right.png")

# player class
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        self.image_player_left = pygame.image.load(SPRITE_RANGER_RACHEL_L)
        self.image_player_right = pygame.image.load(SPRITE_RANGER_RACHEL_R)

        self.image = self.image_player_right
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)

        self.speed = 8


    def check_collision(self, rect):

        # convert pixel position to tile indices for all four corners of the player's rect
        corners = [
            (rect.left // const.TILE_SIZE, rect.top // const.TILE_SIZE),        # top-left
            (rect.right // const.TILE_SIZE, rect.top // const.TILE_SIZE),       # top-right
            (rect.left // const.TILE_SIZE, rect.bottom // const.TILE_SIZE),     # bottom-left
            (rect.right // const.TILE_SIZE, rect.bottom // const.TILE_SIZE),    # bottom-right
        ]

        # check each corner for collision with obstacle
        for corner in corners:

            (tile_x, tile_y) = corner

            if (0 <= tile_x < const.MAP_WIDTH) and (0 <= tile_y < const.MAP_HEIGHT):

                # collision detected with map obstacle
                if const.PARK_MAP[tile_y][tile_x] == const.OBSTACLE:
                    return True
        
        # add all obstacles to list
        obstacles = []
        obstacles = obstacles + const.LITTERBUGS

        # check if collision with all obstacles
        for obstacle in obstacles:

            # collision detected
            if rect.colliderect(obstacle.rect):
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

        # make player sprite face direction of travel
        if dx == const.LEFT:
            self.image = self.image_player_left

        elif dx == const.RIGHT:
            self.image = self.image_player_right
