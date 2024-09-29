import pygame
import random
import os

# local libraries
import constants as const
import junk

# sprite assets
SPRITE_FIREANT_L = os.path.join(const.ASSET_DIR, "fire-ant_left.png")
SPRITE_FIREANT_R = os.path.join(const.ASSET_DIR, "fire-ant_right.png")

# fireant class
class Fireant(pygame.sprite.Sprite):

    def __init__(self, x, y, x_direction, y_direction):

        super().__init__()

        self.image_bug_left = pygame.image.load(SPRITE_FIREANT_L)
        self.image_bug_right = pygame.image.load(SPRITE_FIREANT_R)

        # scale images
        scale = 0.2

        self.image_bug_left = pygame.transform.scale(self.image_bug_left,
                                                      (self.image_bug_left.get_width() * scale,
                                                       self.image_bug_left.get_height() * scale))
        
        self.image_bug_right = pygame.transform.scale(self.image_bug_right,
                                                      (self.image_bug_right.get_width() * scale,
                                                       self.image_bug_right.get_height() * scale))

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

        self.speed = 10
        self.direction = (x_direction, y_direction)


    def torch_tree(self, rect):

        # check if tree is is being contacted
        forest = const.TREES
        for veggie in forest:

            # tree is within reach
            if rect.colliderect(veggie):

                # tree can be torched
                if (veggie.get_state() == const.TREE_GOOD):
                    
                    veggie.set_state(const.TREE_ON_FIRE)


    def check_collision(self, rect):

        # direction of collision
        collision = (0, 0)

        # convert pixel position to tile indices for all four corners of the litterbug's rect
        top_left = (rect.left // const.TILE_SIZE, rect.top // const.TILE_SIZE)
        top_right = (rect.right // const.TILE_SIZE, rect.top // const.TILE_SIZE)
        bottom_left = (rect.left // const.TILE_SIZE, rect.bottom // const.TILE_SIZE)
        bottom_right = (rect.right // const.TILE_SIZE, rect.bottom // const.TILE_SIZE)

        corners = [top_left, top_right, bottom_left, bottom_right]

        # check each corner for collision with collision
        for corner in corners:

            (tile_x, tile_y) = corner

            if (0 <= tile_x < const.MAP_WIDTH) and (0 <= tile_y < const.MAP_HEIGHT):

                # collision detected with map collision
                if const.PARK_MAP[tile_y][tile_x] == const.OBSTACLE:
                    
                    if corner == top_left:
                        collision = tuple(map(lambda i, j: i + j, collision, (const.LEFT, const.UP)))

                    elif corner == top_right:
                        collision = (map(lambda i, j: i + j, collision, (const.RIGHT, const.UP)))

                    elif corner == bottom_left:
                        collision = tuple(map(lambda i, j: i + j, collision, (const.LEFT, const.DOWN)))

                    elif corner == bottom_right:
                        collision = tuple(map(lambda i, j: i + j, collision, (const.RIGHT, const.DOWN)))

        # add all obstacles to list
        obstacles = []

        obstacles.append(const.POND)
        obstacles = obstacles + const.TREES

        obstacles = obstacles + const.LITTERBUGS

        obstacles = obstacles + const.FIREANTS
        obstacles.remove(self)

        # check all obstacles for collisions
        for obstacle in obstacles:

            # collision detected with obstacle
            if rect.colliderect(obstacle.rect):

                if obstacle is const.RANGER_RACHEL and const.INVENTORY_WATER > 0:
                    continue

                # horizontal collision
                if obstacle.rect.right >= rect.left:
                    collision = tuple(map(lambda i, j: i + j, collision, (const.LEFT, 0)))

                elif obstacle.rect.left <= rect.right:
                    collision = tuple(map(lambda i, j: i + j, collision, (const.RIGHT, 0)))

                # vertical collision
                if obstacle.rect.bottom >= rect.top:
                    collision = tuple(map(lambda i, j: i + j, collision, (0, const.UP)))

                elif obstacle.rect.top <= rect.bottom:
                    collision = tuple(map(lambda i, j: i + j, collision, (0, const.DOWN)))

        # normalize collision values
        collision = tuple(collision)

        if collision[0] > 0:
            collision = (const.RIGHT, collision[1])
        
        elif collision[0] < 0:
            collision = (const.LEFT, collision[1])
        
        if collision[1] > 0:
            collision = (collision[0], const.DOWN)
        
        elif collision[1] < 0:
            collision = (collision[0], const.UP)
                
        return collision


    def update(self):

        # calculate new position
        dx, dy = self.direction
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # torch tree if possible
        self.torch_tree(new_rect)

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
