import pygame
import sys
import os.path

# name of game
GAME_NAME = "PARK PATROL"

# directory of where game is located
GAME_DIR = sys.path[0]

# target frame rate
TARGET_FPS = 60

# sprite assets
SPRITE_RANGER_RACHEL = os.path.join(GAME_DIR, "../assets/ranger-rachel.png")

# dimensions
TILE_SIZE = 80
MAP_HEIGHT = 25
MAP_WIDTH = MAP_HEIGHT * 2

# colors
GRASS_COLOR = (0, 154, 23)
FENCE_COLOR = (153, 101, 21)

# traversable terrains
GRASS = 0

# terrain obstacles
FENCE = 1

# initialize Pygame
pygame.init()

# get display information for fullscreen mode
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# create screen in fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption(GAME_NAME)

# create clock for FPS control
clock = pygame.time.Clock()

# create a 500x500 park map with a fence perimeter
park_map = [[1 if x == 0 or x == MAP_WIDTH - 1 or y == 0 or y == MAP_HEIGHT - 1 else 0 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

# Load player sprite
player_image = pygame.image.load(SPRITE_RANGER_RACHEL)

# player class
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.speed = 4


    def move(self, dx, dy):

        # update player position based on input
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # prevent moving off-screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.right > MAP_WIDTH * TILE_SIZE:
            self.rect.right = MAP_WIDTH * TILE_SIZE

        if self.rect.bottom > MAP_HEIGHT * TILE_SIZE:
            self.rect.bottom = MAP_HEIGHT * TILE_SIZE

# create player
player = Player(5, 5)


# camera class to handle scrolling
class Camera:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def apply(self, rect):
        return rect.move(self.camera.topleft)


    def update(self, target):

        # calculate camera position
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        
        # limit scrolling to map bounds
        x = min(0, x)                               # left side
        x = max(-(self.width - SCREEN_WIDTH), x)    # right side
        y = min(0, y)                               # top side
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom side
        
        self.camera = pygame.Rect(x, y, self.width, self.height)


# initialize camera
camera = Camera(MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)


# main game loop
def main():

    running = True
    
    while running:
        
        # handle events
        for event in pygame.event.get():
            
            # quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # escape key quits the game in fullscreen mode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow escape key to quit fullscreen mode
                    pygame.quit()
                    sys.exit()
        
        # player movement input
        keys = pygame.key.get_pressed()
        dx = dy = 0

        # left
        if keys[pygame.K_a]:
            dx = -1
        
        # right
        if keys[pygame.K_d]:
            dx = 1

        # down
        if keys[pygame.K_w]:
            dy = -1

        # up
        if keys[pygame.K_s]:
            dy = 1
        
        # update player and camera
        player.move(dx, dy)
        camera.update(player)
        
        # fill background with grass
        screen.fill(GRASS_COLOR)
        
        # draw park map
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):

                tile = park_map[row][col]

                # tile is a fence
                if tile == FENCE:
                    
                    # draw fence
                    fence = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, FENCE_COLOR, camera.apply(fence))
        
        # draw player
        screen.blit(player.image, camera.apply(player.rect))
        
        # Update the display
        pygame.display.flip()
        
        # cap the framerate
        clock.tick(TARGET_FPS)

# Start the game
if __name__ == "__main__":
    main()
