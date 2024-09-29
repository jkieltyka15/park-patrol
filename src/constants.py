import sys
import os

# name of game
GAME_NAME = "PARK PATROL"

# directory of where game is located
GAME_DIR = sys.path[0]
ASSET_DIR = os.path.join(GAME_DIR, "../assets/")

# target frame rate
TARGET_FPS = 60

# screen size, which will be set in main
SCREEN_WIDTH = None
SCREEN_HEIGHT = None

# the game map, which will be set in main (dynamic)
PARK_MAP = None

# pond for the map
POND = None

# list of trees (dynamic)
TREES = []
TREE_GOOD = 0
TREE_STUMP = 1
TREE_ON_FIRE = 2

# ranger rachel player, which will be set in (dynamic)
RANGER_RACHEL = None
INVENTORY_WATER = 0
INVENTORY_JUNK = 0
INVENTORY_TREES = 0
JUNK_TO_TREES = 10

# litterbugs
LITTERBUGS = []
JUNK = []

# dimensions
TILE_SIZE = 100
TILE_2D = (TILE_SIZE, TILE_SIZE)
MAP_HEIGHT = 25
MAP_WIDTH = MAP_HEIGHT * 2

# sprite assets
SPRITE_GRASS = os.path.join(ASSET_DIR, "grass.png")
SPRITE_ROCK = os.path.join(ASSET_DIR, "rock.png")

# traversable 
TRAVERSABLE = 0
GRASS = 0 - 0

# terrain obstacles
OBSTACLE = TRAVERSABLE + 1
ROCK = OBSTACLE + 0

# directions
UP = -1
DOWN = 1
LEFT = -1
RIGHT =  1