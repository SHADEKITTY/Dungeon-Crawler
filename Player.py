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

    def handle_input(self, event, tile_rows, tile_cols):
        moved = False

        new_gridx = self.gridx
        new_gridy = self.gridy

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                new_gridy -= 1

            elif event.key in (pygame.K_DOWN,pygame.K_s):
                new_gridy += 1

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                new_gridx -= 1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                new_gridx += 1

        if new_gridx >= 0 and new_gridx < tile_cols and new_gridy >= 0 and new_gridy < tile_rows:
            self.gridx = new_gridx
            self.gridy = new_gridy

        return moved
        
    def update(self):
        pass

        self.x = self.gridx * self.tile_width
        self.y = self.gridy * self.tile_height


   