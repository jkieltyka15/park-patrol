import pygame
import sys
import os

# local libraries
import constants as const
import colors as color
import camera as cam
import player
import litterbug
import fireant
import tree
import pond

# initalize pygame and core game components and returns (screen, clock) tuple
def initialize(screen, clock):

    # initialize Pygame
    pygame.init()

    # hide the mouse
    pygame.mouse.set_visible(False)

    # start background music
    pygame.mixer.init()
    pygame.mixer.music.load(const.MUSIC_FILE)
    pygame.mixer.music.set_volume(const.MUSIC_VOLUME)
    pygame.mixer.music.play(-1,0.0)

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
    
    # create trees
    const.TREES.append(tree.Tree(const.TREE_STUMP, 13, 13))
    const.TREES.append(tree.Tree(const.TREE_ON_FIRE, 40, 15))
    const.TREES.append(tree.Tree(const.TREE_STUMP, 8, 5))
    const.TREES.append(tree.Tree(const.TREE_STUMP, 2, 15))
    const.TREES.append(tree.Tree(const.TREE_ON_FIRE, 40, 6))

    # create pond
    const.POND = pond.Pond(20, 8)
    
    # create player
    const.RANGER_RACHEL = player.Player(5, 5)

    # create litterbugs
    const.LITTERBUGS.append(litterbug.Litterbug(35, 5, 0, const.DOWN))
    const.LITTERBUGS.append(litterbug.Litterbug(20, 2, const.LEFT, const.DOWN))
    const.LITTERBUGS.append(litterbug.Litterbug(35, 9, const.RIGHT, const.DOWN))
    const.LITTERBUGS.append(litterbug.Litterbug(35, 11, 0, const.UP))
    const.LITTERBUGS.append(litterbug.Litterbug(35, 13, const.LEFT, const.UP))
    const.LITTERBUGS.append(litterbug.Litterbug(35, 15, const.RIGHT, const.UP))
    const.LITTERBUGS.append(litterbug.Litterbug(35, 17, const.LEFT, 0))
    const.LITTERBUGS.append(litterbug.Litterbug(5, 1, const.RIGHT, 0))

    # create fireants
    const.FIREANTS.append(fireant.Fireant(40, 5, const.LEFT, const.DOWN))
    const.FIREANTS.append(fireant.Fireant(15, 2, const.LEFT, const.UP))
    const.FIREANTS.append(fireant.Fireant(15, 9, const.RIGHT, const.DOWN))
    const.FIREANTS.append(fireant.Fireant(15, 20, const.RIGHT, const.UP))
    
    return (screen, clock)


# display ranger rachel's inventory
def display_inventory(screen):

    # setup font for item counter display
    font = pygame.font.SysFont(None, 36)

    # render the text showing the number of items collected
    hasWater = "No" if const.INVENTORY_WATER == 0 else "Yes" 
    item_text = font.render(f"  Water: {hasWater}  Junk: {const.INVENTORY_JUNK}   Trees: {const.INVENTORY_TREES}",
                            True, color.BLACK)
    
    # draw the box for the text
    position = (const.SCREEN_WIDTH - 380, 10, 380, 40)
    pygame.draw.rect(screen, color.WHITE, position)

    # draw box border
    pygame.draw.rect(screen, color.BLACK, position, 2)
    
    # blit the text onto the screen
    screen.blit(item_text, (position[0], position[1] + 10))

# display victory screen when all objectives are completed
def display_victory(screen):

    win_font = pygame.font.SysFont(None, 144)
    win_text = win_font.render("You saved the park!", True, color.WHITE)

    # black out screen
    screen.fill(color.BLACK)

    # write text
    screen.blit(win_text, (const.SCREEN_WIDTH // 2 - win_text.get_width() // 2,
                           const.SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
    
    # update display
    pygame.display.update()

    # display screen for 3 seconds
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


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
        if keys[pygame.K_LEFT]:
            dx = const.LEFT
        
        # right
        if keys[pygame.K_RIGHT]:
            dx = const.RIGHT

        # up
        if keys[pygame.K_UP]:
            dy = const.UP

        # down
        if keys[pygame.K_DOWN]:
            dy = const.DOWN
        
        # update ranger rachel and camera
        const.RANGER_RACHEL.move(dx, dy)
        camera.update(const.RANGER_RACHEL)

        # update litterbugs
        for bug in const.LITTERBUGS:
            bug.update()

        # update fireants
        for bug in const.FIREANTS:
            bug.update()
        
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

        # draw pond
        screen.blit(const.POND.image, camera.apply(const.POND.rect))

        # draw ranger rachel
        screen.blit(const.RANGER_RACHEL.image, camera.apply(const.RANGER_RACHEL.rect))

        # draw junk
        for trash in const.JUNK:
            screen.blit(trash.image, camera.apply(trash.rect))

        # draw litterbugs
        for bug in const.LITTERBUGS:
            screen.blit(bug.image, camera.apply(bug.rect))

        # draw fireants
        for bug in const.FIREANTS:
            screen.blit(bug.image, camera.apply(bug.rect))

        # draw trees
        for tree in const.TREES:
            screen.blit(tree.image, camera.apply(tree.rect))

        # draw inventory board
        display_inventory(screen)

        # all fireants must have been eliminated
        if len(const.FIREANTS) == 0:

            is_victory = True;

            # all trees must be healthy
            for veggie in const.TREES:

                if veggie.get_state() != const.TREE_GOOD:
                    is_victory = False;

            # player has won
            if is_victory:
                pygame.time.delay(1000)
                pygame.mixer.stop()
                display_victory(screen)
        
        # Update the display
        pygame.display.flip()
        
        # cap the framerate
        clock.tick(const.TARGET_FPS)

# start the game
if __name__ == "__main__":
    main()
