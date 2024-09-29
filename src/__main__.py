import pygame
import sys

# local libraries
import constants as const
import camera as cam
import player

# initalize pygame and core game components and returns (screen, clock) tuple
def initialize(screen, clock):

    # initialize Pygame
    pygame.init()

    # get display information for fullscreen mode
    infoObject = pygame.display.Info()
    const.SCREEN_WIDTH = infoObject.current_w
    const.SCREEN_HEIGHT = infoObject.current_h

    # create screen in fullscreen mode
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption(const.GAME_NAME)

    # create clock for FPS control
    clock = pygame.time.Clock()

    # create a 500x500 park map with a rock perimeter
    const.PARK_MAP = [[const.OBSTACLE 
                        if (x == 0) or (x == const.MAP_WIDTH - 1)
                        or (y == 0) or (y == const.MAP_HEIGHT - 1) 
                        else const.TRAVERSABLE for x in range(const.MAP_WIDTH)] for y in range(const.MAP_HEIGHT)]
    
    return (screen, clock)

# initializes game and runs game loop
def main():

    # initialize pygame and map
    screen = None
    clock = None
    (screen, clock) = initialize(screen, clock)

    # load terrain sprites
    grass_image = pygame.image.load(const.SPRITE_GRASS)
    rock_image = pygame.image.load(const.SPRITE_ROCK)

    # scale terrain sprites
    grass_image = pygame.transform.scale(grass_image, const.TILE_2D)
    rock_image = pygame.transform.scale(rock_image, const.TILE_2D)

    # create player
    ranger = player.Player(5, 5)

    # initialize camera
    camera = cam.Camera(const.MAP_WIDTH * const.TILE_SIZE, const.MAP_HEIGHT * const.TILE_SIZE)

    running = True
    
    # main game loop
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
        
        # ranger rachel actions input
        keys = pygame.key.get_pressed()
        dx = dy = 0

        # left
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        
        # right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1

        # up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1

        # down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1

        # run
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            dy *= 2
            dx *= 2
        
        # update ranger rachel and camera
        ranger.move(dx, dy)
        camera.update(ranger)
        
        # draw park map
        for row in range(const.MAP_HEIGHT):
            for col in range(const.MAP_WIDTH):

                tile = const.PARK_MAP[row][col]
                tile_rect = pygame.Rect(col * const.TILE_SIZE, row * const.TILE_SIZE, const.TILE_SIZE, const.TILE_SIZE)

                # tile is a rock
                if tile == const.ROCK:
                    
                    # draw rock
                    screen.blit(rock_image, camera.apply(tile_rect))

                # tile is grass
                else:
                    screen.blit(grass_image, camera.apply(tile_rect))

        
        # draw ranger rachel
        screen.blit(ranger.image, camera.apply(ranger.rect))
        
        # Update the display
        pygame.display.flip()
        
        # cap the framerate
        clock.tick(const.TARGET_FPS)

# start the game
if __name__ == "__main__":
    main()
