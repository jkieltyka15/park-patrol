import pygame
import constants as const

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
        x = -target.rect.centerx + int(const.SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(const.SCREEN_HEIGHT / 2)
        
        # limit scrolling to map bounds
        x = min(0, x)                                       # left side
        x = max(-(self.width - const.SCREEN_WIDTH), x)      # right side
        y = min(0, y)                                       # top side
        y = max(-(self.height - const.SCREEN_HEIGHT), y)    # bottom side
        
        self.camera = pygame.Rect(x, y, self.width, self.height)