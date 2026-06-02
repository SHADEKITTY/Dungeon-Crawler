import pygame
from go import *
from wall import *
from spritesheet import *
import os

GREEN = (0, 255, 0)

M_F = 10

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets", "1 Pink_Monster")

class Player(GameObject):

    def __init__(self, gridx, gridy, tile_width, tile_height, color = GREEN):
        x = gridx * tile_width
        y = gridy * tile_height
        super().__init__(gridx, gridy, x, y, tile_width, tile_height, color)


        self.m_s = tile_width / M_F


        scale = (tile_width, tile_height)
        self.animations = {
            "idle": Animation(load_spritesheet(os.path.join(ASSET_DIR, "Pink_Monster_Idle_4.png"), 32, 32, scale), speed=max(1, M_F // 8)),
            "walk": Animation(load_spritesheet(os.path.join(ASSET_DIR, "Pink_Monster_Walk_6.png"), 32, 32, scale), speed=max(1, M_F // 8))
        }
        self.current_animation = "idle"
        self.direction = "right"
        self.is_moving = False

    def draw(self, surface):
        
        frame = self.animations[self.current_animation].get_frame()

        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, (self.x, self.y))

    def handle_input(self, event, game_map, tile_rows, tile_cols):
        if self.is_moving:
            return False
        
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
                self.direction = "left"
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                new_gridx += 1
                self.direction = "right"

        if new_gridx >= 0 and new_gridx < tile_cols and new_gridy >= 0 and new_gridy < tile_rows:
            

            if game_map[new_gridx][new_gridy] == 0:
                game_map[new_gridx][new_gridy] = game_map[self.gridy][self.gridx]
                game_map[self.gridy][self.gridx] = 0
                self.gridx = new_gridx
                self.gridy = new_gridy
                moved = True

        return moved
        
    def update(self):
        targetx = self.gridx * self.tile_width
        targety = self.gridy * self.tile_height

        if self.x < targetx:
            self.x = min(self.x + self.m_s, targetx)
        elif self.x > targetx:
            self.x = max(self.x - self.m_s, targetx)

        if self.y < targety:
            self.y = min(self.y + self.m_s, targety)
        elif self.y > targety:
            self.y = max(self.y - self.m_s, targety)

        if self.is_moving:
            if self.current_animation != "walk":
                self.current_animation = "walk"
                self.animations["walk"].reset()
            self.animations["walk"].tick()

            if self.current_animation != "idle":
                self.current_animation = "idle"
                self.animations["idle"].reset()
            self.animations["idle"].tick()