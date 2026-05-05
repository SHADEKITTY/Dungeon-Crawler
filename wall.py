import pygame
from go import *

Blue = (0, 0, 255)

class Wall(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height, color=Blue):

        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)

    def update(self):
        pass

    def draw(self, _surface):
        pygame.draw.rect(_surface, self.color, (self.x, self.y, self.tile_width, self.tile_height))

