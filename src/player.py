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


    def get_water(self, rect):

        if rect.colliderect(const.POND.rect):

            fill_sound = pygame.mixer.Sound(const.WATER_FILL_SOUND_FILE)
            pygame.mixer.Sound.play(fill_sound)
            const.INVENTORY_WATER = 1


    def pickup_junk(self):

        # check if junk can be picked up
        litter = const.JUNK
        for trash in litter:

            # junk can be picked up
            if self.rect.colliderect(trash.rect):

                can_sound = pygame.mixer.Sound(const.CAN_CRUSH_SOUND_FILE)
                pygame.mixer.Sound.play(can_sound)
                const.JUNK.remove(trash)
                const.INVENTORY_JUNK += 1


    def eleminate_fireants(self, new_rect):

        # check if fireant can be eliminated
        bugs = const.FIREANTS
        for bug in bugs:

            # fireant can be eliminated
            if self.rect.colliderect(bug.rect) and const.INVENTORY_WATER > 0:

                splash_sound = pygame.mixer.Sound(const.SPLASH_SOUND_FILE)
                pygame.mixer.Sound.play(splash_sound)
                const.FIREANTS.remove(bug)
                const.INVENTORY_WATER -= 1


    def tend_trees(self, rect):

        # check if tree is is being contacted
        forest = const.TREES
        for veggie in forest:

            # tree is within reach
            if rect.colliderect(veggie):

                # tree is on fire and can be put out
                if (veggie.get_state() == const.TREE_ON_FIRE) and (const.INVENTORY_WATER > 0):

                    splash_sound = pygame.mixer.Sound(const.SPLASH_SOUND_FILE)
                    pygame.mixer.Sound.play(splash_sound)
                    veggie.set_state(const.TREE_STUMP)
                    const.INVENTORY_WATER -= 1

                # new tree can be planted
                if (veggie.get_state() == const.TREE_STUMP) and (const.INVENTORY_TREES > 0):

                    build_sound = pygame.mixer.Sound(const.BUILDING_SOUND_FILE)
                    pygame.mixer.Sound.play(build_sound)
                    veggie.set_state(const.TREE_GOOD)
                    const.INVENTORY_TREES -= 1

    
    def trade_junk_for_trees(self):

        num_of_trees = int(const.INVENTORY_JUNK / const.JUNK_TO_TREES)
        const.INVENTORY_JUNK -= num_of_trees * const.JUNK_TO_TREES
        const.INVENTORY_TREES += num_of_trees

        # play sound effect when a new trey is obtained
        if num_of_trees > 0:
            cash_sound = pygame.mixer.Sound(const.CASH_REGISTER_SOUND_FILE)
            pygame.mixer.Sound.play(cash_sound)


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
        obstacles.append(const.POND)
        obstacles = obstacles + [veggie for veggie in const.TREES if veggie.get_state() != const.TREE_GOOD]
        obstacles = obstacles + const.LITTERBUGS
        obstacles = obstacles + const.FIREANTS

        # check if collision with all obstacles
        for obstacle in obstacles:

            # collision detected
            if rect.colliderect(obstacle.rect):

                # firant sound effect
                if obstacle in const.FIREANTS:
                    fire_sound = pygame.mixer.Sound(const.FIRE_SOUND_FILE)
                    pygame.mixer.Sound.play(fire_sound)

                # litterbug sound effect
                if obstacle in const.LITTERBUGS:
                    honk_sound = pygame.mixer.Sound(const.HONK_SOUND_FILE)
                    pygame.mixer.Sound.play(honk_sound)

                return True
                
        return False


    def move(self, dx, dy):

        # pickup junk if possible
        self.pickup_junk()

        # trade junk for trees if player has enough in inventory
        self.trade_junk_for_trees()

        # calculate new position
        new_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # get water if by pond
        self.get_water(new_rect)

        # tend to trees if within reach
        self.tend_trees(new_rect)

        # eleminate fireant if possible
        self.eleminate_fireants(new_rect)

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
        if dx < 0:
            self.image = self.image_player_left

        elif dx > 0:
            self.image = self.image_player_right
