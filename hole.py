import os
import pygame
from go import GameObject


ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


class Hole(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height):
        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color=None)


        img = pygame.image.load(os.path.join(ASSET_DIR, "hole.png")).convert_alpha()
        self.image = pygame.transform.scale(img, (int(tile_width), int(tile_height)))


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


    def update(self):
        pass  # Hole is static