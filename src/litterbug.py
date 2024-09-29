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

        # traveling vertically first or is not moving
        else:
            self.image = self.image_bug_right

        self.rect = self.image.get_rect()
        self.rect.topleft = (x * const.TILE_SIZE, y * const.TILE_SIZE)

        self.speed = 4
        self.direction = (x_direction, y_direction)


    def check_collision(self, rect):

        # direction of obstacle
        obstacle = (0 , 0)

        # convert pixel position to tile indices for all four corners of the litterbug's rect
        top_left = (rect.left // const.TILE_SIZE, rect.top // const.TILE_SIZE)
        top_right = (rect.right // const.TILE_SIZE, rect.top // const.TILE_SIZE)
        bottom_left = (rect.left // const.TILE_SIZE, rect.bottom // const.TILE_SIZE)
        bottom_right = (rect.right // const.TILE_SIZE, rect.bottom // const.TILE_SIZE)

        corners = [top_left, top_right, bottom_left, bottom_right]

        # Check each corner for collision with a walls
        for corner in corners:

            (tile_x, tile_y) = corner

            if (0 <= tile_x < const.MAP_WIDTH) and (0 <= tile_y < const.MAP_HEIGHT):

                # collision detected
                if const.PARK_MAP[tile_y][tile_x] == const.OBSTACLE:
                    
                    if corner == top_left:
                        obstacle = tuple(map(lambda i, j: i + j, obstacle, (const.LEFT, const.UP)))

                    elif corner == top_right:
                        obstacle = (map(lambda i, j: i + j, obstacle, (const.RIGHT, const.UP)))

                    elif corner == bottom_left:
                        obstacle = tuple(map(lambda i, j: i + j, obstacle, (const.LEFT, const.DOWN)))

                    elif corner == bottom_right:
                        obstacle = tuple(map(lambda i, j: i + j, obstacle, (const.RIGHT, const.DOWN)))

        # normalize obstacle values
        obstacle = tuple(obstacle)

        if obstacle[0] > 0:
            obstacle = (const.RIGHT, obstacle[1])
        
        elif obstacle[0] < 0:
            obstacle = (const.LEFT, obstacle[1])
        
        if obstacle[1] > 0:
            obstacle = (obstacle[0], const.DOWN)
        
        elif obstacle[1] < 0:
            obstacle = (obstacle[0], const.UP)
                
        return obstacle


    def update(self):

        # calculate new position
        dx, dy = self.direction
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # check for collision
        collision = self.check_collision(new_rect)

        # change direction if there is a collision
        if collision[0] != 0:
            dx = -dx

        if collision[1] != 0:
            dy = -dy

        self.direction = (dx, dy)

        self.rect = self.rect.move(dx * self.speed, dy * self.speed)

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