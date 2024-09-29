# local libraries
import constants as const

# Function to check for wall collision based on player's new position
def check_collision(rect):

    # convert pixel position to tile indices for all four corners of the object's rect
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
