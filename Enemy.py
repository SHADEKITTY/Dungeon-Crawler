import os
import pygame
import random
from go import *
from Player import *
from spritesheet import load_spritesheet, Animation

Red = (255, 0, 0)

M_F = 10

A_DIR = os.path.join(os.path.dirname(__file__), "assets", "3 Dude_Monster")

class Enemy(GameObject):
    def __init__(self, gridx, gridy, tile_width, tile_height, color = Red):
        x = gridx + tile_width
        y = gridy + tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)

        self.m_s = tile_width / M_F

        scale = (tile_width, tile_height)
        self.animation = {
            "idle": Animation(load_spritesheet(os.path.join(A_DIR, "Dude_Monster_Idle_4.png"), 32, 32, scale), speed=8),
            "walk"
: Animation(load_spritesheet(os.path.join(A_DIR, "Dude_Monster_Walk_6.png"), 32, 32, scale), speed=max(1, M_F // 6)),
        }
        self.current_animation = "idle"
        self.direction = "right"
        self.is_moving = False

    def draw(self, surface):
        frame = self.animation[self.current_animation].get_frame()

        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, (self.x, self.y))

    def update(self):
        target_x = self.gridx * self.tile_width
        target_y = self.gridy * self.tile_height

        if self.x < target_x:
            self.x = min(self.x + self.m_s, target_x)
        elif self.x > target_x:
            self.x = max(self.x - self.m_s, target_x)

        if self.y < target_y:
            self.y = min(self.y + self.m_s, target_y)
        elif self.y > target_y:
            self.y = max(self.y - self.m_s, target_y)

        self.is_moving = (self.x != target_x or self.y != target_y)

        if self.is_moving:
            if self.current_animation != "walk":
                self.current_animation = "walk"
                self.animation["walk"].reset()
            self.animation["walk"].tick()
        else:
            if self.current_animation != "idle":
                self.current_animation = "idle"
                self.animation["idle"].reset()
                self.animation["idle"].tick()


    def take_turn(self, game_map, tile_cols, tile_rows, old_player_x, old_player_y):
        self._move_rand_adj(game_map, tile_cols, tile_rows, old_player_x, old_player_y)
        

    def _move_rand_adj(self, game_map, tile_cols, tile_rows, old_player_x, old_player_y):
        directions = [(0, -1),
                      (0, 1),
                      (-1, 0),
                      (1, 0)]
        
        for dx, dy in directions:
            new_gridx = self.gridx + dx
            new_gridy = self.gridy + dy

            if 0 <= new_gridx < tile_rows and 0 <= new_gridy < tile_cols:
                if game_map[new_gridx][new_gridy] == 0 and new_gridx == old_player_x and new_gridy == old_player_y:
                    self._move(game_map, new_gridx, new_gridy, dx, dy)
                    return
        
        random.shuffle(directions)

        for dx, dy in directions:
            new_gridx = self.gridx + dx
            new_gridy = self.gridy + dy

            if 0 <= new_gridx < tile_rows and 0 <= new_gridy < tile_cols:

                if game_map[new_gridx][new_gridy] == 0 or isinstance(game_map[new_gridx][new_gridy], Player):
                    self._move(game_map, new_gridx, new_gridy, dx, dy)
                    break

    def _move(self, game_map, new_gridx, new_gridy, dx, dy):
        game_map[new_gridx][new_gridy] = self
        game_map[self.gridx][self.gridy] = 0

        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"

        self.gridx = new_gridx
        self.gridy = new_gridy