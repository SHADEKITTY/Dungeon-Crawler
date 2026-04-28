import pygame
from go import *

GREEN = (0, 255, 0)

class Player(GameObject):

    def __init__(self, gridx, gridy, tile_width, tile_height, color = GREEN):
        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.tile_width, self.tile_height))

    def update(self):
        pass