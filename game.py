import pygame
import random
from Player import *
from wall import *
from Enemy import *

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

IPGX = 2
IPGY = 2

class Game:
    def __init__(self, _width, _height, _caption):
        self.width = _width
        self.height = _height
        self.caption = _caption
        self.tile_cols = 10
        self.tile_rows = 10
        self.tile_width = self.width / self.tile_cols
        self.tile_height = self.height / self.tile_rows

        self.clock = pygame.time.Clock()
        self.running = True
        self._setup_pygame()
        self._init_gos()

    def run_game_loop(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    def _init_gos(self):
        self.map = []

        for _ in range(self.tile_cols):
            new_col = []
            for _ in range(self.tile_rows):
                new_col.append(0)
            
            self.map.append(new_col)

        self.map = [[0] * self.tile_cols for _ in range(self.tile_rows)]
        self.player = Player(IPGX, IPGY, self.tile_width, self.tile_height)
        self.map[IPGX][IPGY] = self.player

        self.enemies = []

        self.genL()


    def genL(self, num_internal_wall = 10, num_enemy = 3):
        for col in range(self.tile_cols):
            self.map[col][0] = Wall(col, 0, self.tile_width, self.tile_height)
            self.map[col][self.tile_cols - 1] = Wall(col, self.tile_cols - 1, self.tile_width, self.tile_height)

        for row in range(self.tile_rows):
            self.map[0][row]= Wall(0, row, self.tile_width, self.tile_height)
            self.map[self.tile_rows - 1][row]= Wall(self.tile_cols - 1, row, self.tile_width, self.tile_height)
        
        for _ in range(num_internal_wall):
            x = random.randint(1, self.tile_cols - 2)
            y = random.randint(1, self.tile_rows - 2)

            while self.map[x][y] != 0:
                x = random.randint(1, self.tile_cols - 2)
                y = random.randint(1, self.tile_rows - 2)

            self.map[x][y] = Wall(x, y, self.tile_width, self.tile_height)


        for _ in range(num_enemy):
            minxTSR = 3
            maxxTSR = self.tile_rows - 1
            minyTSR = 1
            maxyTSR = self.tile_cols - 1

            enemy_x, enemy_y = self._findFT(minxTSR, maxxTSR, minyTSR, maxyTSR)

            enemy = Enemy(enemy_x, enemy_y, self.tile_height, self.tile_width)
            self.map[enemy_x][enemy_y] = enemy
            self.enemies.append(enemy)

    def _findFT(self, min_x, max_x, min_y, max_y):
        while True:
            check_x = random.randint(min_x, max_x)
            check_y = random.randint(min_y, max_y)

            if self.map[check_x][check_y] == 0:
                return check_x, check_y

        
            

    def _setup_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption) 

    def _handle_events(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.running = False
            if self.player:
                moved = self.player.handle_input(event, self.map, self.tile_cols, self.tile_rows)

                if moved:
                    for enemy in self.enemies:
                        enemy.take_turn(self.map, self.tile_cols, self.tile_rows)

    def _draw(self):
        self.display.fill(WHITE)

        for col in range(self.tile_cols):
            for row in range(self.tile_rows):
                if isinstance(self.map[col][row], Wall):
                    self.map[col][row].draw(self.display)
                rect = (col * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
                pygame.draw.rect(self.display, BLACK, rect, 1)

        for enemy in self.enemies:
            enemy.draw(self.display)

        self.player.draw(self.display)
        pygame.display.update()
    
    def _update(self):
        
        self.player.update()

        for enemy in self.enemies:
            enemy.update()