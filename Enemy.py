import pygame
import random
from go import *

Red = (255, 0, 0)

class Enemy(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height, color = Red):
        x = gridx + tile_width
        y = gridy + tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)

    def draw(self, surface):
        ##TODO:
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.tile_width, self.tile_height))

    def update(self):
        self.x = self.gridx * self.tile_width
        self.y = self.gridy * self.tile_height

    def take_turn(self, game_map, tile_cols, tile_rows):
        self._move_rand_adj(game_map, tile_cols, tile_rows)

    def _move_rand_adj(self, game_map, tile_cols, tile_rows):
        directions = [(0, -1),
                      (0, 1),
                      (-1, 0),
                      (1, 0)]
        
        random.shuffle(directions)

        for dx, dy in directions:
            new_gridx = self.gridx + dx
            new_gridy = self.gridy + dy

            if 0 <= new_gridx < tile_rows and 0 <= new_gridy < tile_cols:

                if game_map[new_gridx][new_gridy] == 0:

                    game_map[new_gridx][new_gridy] = game_map[self.gridx][self.gridy]
                    game_map[self.gridx][self.gridy] = 0
                    self.gridx = new_gridx
                    self.gridy = new_gridy
                    break

