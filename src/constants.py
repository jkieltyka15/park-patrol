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

# the game map, which will be set in main
PARK_MAP = None

# sprite assets
SPRITE_GRASS = os.path.join(ASSET_DIR, "grass.png")
SPRITE_ROCK = os.path.join(ASSET_DIR, "rock.png")

# dimensions
TILE_SIZE = 100
TILE_2D = (TILE_SIZE, TILE_SIZE)
MAP_HEIGHT = 25
MAP_WIDTH = MAP_HEIGHT * 2

# traversable terrains
TRAVERSABLE = 0
GRASS = 0

# terrain obstacles
OBSTACLE = 1
ROCK = 1