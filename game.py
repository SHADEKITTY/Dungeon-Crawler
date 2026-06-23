import os
import pygame
import random

from Enemy import *
from Player import *
from wall import Wall
from hole import Hole


FPS = 60

BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
RED = (255, 0, 0)

MAX_LIVES = 3

INITIAL_PLAYER_GRID_X = 2
INITIAL_PLAYER_GRID_Y = 2

# Path to tile assets (relative to this file)
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
FLOOR_TILE = "floor.jpg"
WALL_TILE = "wall.jpg"

class Game:
    def __init__(self, _width, _height, _caption):
        self.width = _width
        self.height = _height
        self.caption = _caption

        # have a set amount of rows and columns and determine the width and height of each
        self.tile_cols = 10
        self.tile_rows = 10
        self.tile_width = self.width / self.tile_cols
        self.tile_height = self.height / self.tile_rows

        self.clock = pygame.time.Clock()
        self.running = True
        self.pending_death = False
        self.lives = MAX_LIVES
        self.game_over = False
        self.pending_hole_fall = False  # True after stepping on the hole, until the slide finishes


        # Gme setup
        self._setup_pygame()
        self._load_tiles()
        self._init_game_objects()

    def run_game_loop(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    def _init_game_objects(self):
        ## create empty map using 2D list
        self.map = []
        for _ in range(self.tile_cols):
            # generate empty col to be added to each raw
            new_col = []
            for _ in range(self.tile_rows):
                new_col.append(0)

            # add new col to map
            self.map.append(new_col)
            self.map = [[0] * self.tile_cols for _ in range(self.tile_rows)]

        # set up player
        self.player = Player(INITIAL_PLAYER_GRID_X, INITIAL_PLAYER_GRID_Y, self.tile_width, self.tile_height)
        self.map[INITIAL_PLAYER_GRID_X][INITIAL_PLAYER_GRID_Y] = self.player

        ## Create Enemies
        self.enemies = []

        ## Initial level generation
        self._generate_level()

    def _generate_level(self, num_internal_walls=10, num_enemies = 3):

        for col in range(self.tile_cols):
            # first col
            self.map[col][0] = Wall(col, 0, self.tile_width, self.tile_height)

            # last col
            self.map[col][self.tile_cols - 1] = Wall(col, self.tile_cols - 1, self.tile_width, self.tile_height)

        for row in range(self.tile_rows):
            # first row
            self.map[0][row] = Wall(0, row, self.tile_width, self.tile_height)

            # last row
            self.map[self.tile_rows - 1][row] = Wall(self.tile_cols - 1, row, self.tile_width, self.tile_height)

        ### create random internal walls
        for _ in range(num_internal_walls):
            # Initial randomization, avoid clashing with the border
            x = random.randint(1, self.tile_cols - 2)
            y = random.randint(1, self.tile_rows - 2)

            ## if space is not free
            while self.map[x][y] != 0:
                x = random.randint(1, self.tile_cols - 2)
                y = random.randint(1, self.tile_rows - 2)

            self.map[x][y] = Wall(x, y, self.tile_width, self.tile_height)


     ### Create random enemies with initial tile spawn on free tile
        for _ in range(num_enemies):
            minx_tile_spawn_range = 3
            maxx_tile_spawn_range = self.tile_rows - 1
            miny_tile_spawn_range = 1
            maxy_tile_spawn_range = self.tile_cols - 1

            enemy_x, enemy_y = self._find_free_tile(minx_tile_spawn_range, 
                                                    maxx_tile_spawn_range, 
                                                    miny_tile_spawn_range, 
                                                    maxy_tile_spawn_range)
            enemy = Enemy(enemy_x, enemy_y, self.tile_width, self.tile_height)
            self.map[enemy_x][enemy_y] = enemy
            self.enemies.append(enemy)

        # Place a hole on a free interior tile
        hole_x, hole_y = self._find_free_tile(1, self.tile_cols - 2, 1, self.tile_rows - 2)
        self.hole = Hole(hole_x, hole_y, self.tile_width, self.tile_height)


        # Pre-render tiles into a single surface after map is built
        self._bake_tile_layer()

    def _load_tiles(self):
        # Covert tile sizes to ints for pygame load
        tw, th = int(self.tile_width), int(self.tile_height)

        self.floor_tile = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, FLOOR_TILE)).convert(), (tw, th))
        self.wall_tile = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_DIR, WALL_TILE)).convert(), (tw, th))

    def _bake_tile_layer(self):
        """Pre-render all floor and wall tiles into a single static surface.
        Call this once after the map is generated. Drawing then becomes one fast blit."""
        self.tile_layer = pygame.Surface((self.width, self.height))
        for col in range(self.tile_cols):
            for row in range(self.tile_rows):
                tile = self.wall_tile if isinstance(self.map[col][row], Wall) else self.floor_tile
                self.tile_layer.blit(tile, (col * self.tile_width, row * self.tile_height))


    def _find_free_tile(self, min_x, max_x, min_y, max_y):
        ## loop to get the first free tile
        while True:
            check_x = random.randint(min_x, max_x)
            check_y = random.randint(min_y, max_y)

            if self.map[check_x][check_y] == 0:
                return check_x, check_y
 

    def _setup_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        self.font = pygame.font.SysFont(None, 36)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    self._restart_game()
                continue

            if self.player:
                curr_player_x, curr_player_y = self.player.gridx, self.player.gridy
                moved = self.player.handle_input(event, self.map, self.tile_cols, self.tile_rows)



                if moved: 
                    for enemy in self.enemies:
                        enemy.take_turn(self.map, self.tile_cols, self.tile_rows, curr_player_x, curr_player_y)
                    
                    for enemy in self.enemies:
                        if enemy.gridx == self.player.gridx and enemy.gridy == self.player.gridy:
                            self.pending_death = True
                            break
                        

                    # Check if the player stepped onto the hole and wait until they
                    # finish sliding to the tile before triggering the fall animation
                    if not self.pending_death and self.player.gridx == self.hole.gridx and self.player.gridy == self.hole.gridy:
                        self.pending_hole_fall = True

    def _respawn_player(self):
        self.map[self.player.gridx][self.player.gridy] = 0

        self.player.gridx = INITIAL_PLAYER_GRID_X
        self.player.gridy = INITIAL_PLAYER_GRID_Y
        self.player.x = INITIAL_PLAYER_GRID_X * self.tile_width
        self.player.y = INITIAL_PLAYER_GRID_Y * self.tile_height
        self.player.is_moving = False
        self.player.hole_falling = False
        self.player.hole_fall_done = False
        self.player.dying = False
        self.player.death_done = False
        self.player.current_animation = "idle"
        self.map[INITIAL_PLAYER_GRID_X][INITIAL_PLAYER_GRID_Y] = self.player

    def _lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.pending_hole_fall = False
            self.pending_death = False
            self._respawn_player()
    
    def _restart_game(self):
        self.lives = MAX_LIVES
        self.game_over = False
        self.pending_hole_fall = False
        self.pending_death = False
        self.map = [[0] * self.tile_rows for _ in range(self.tile_cols)]
        self.enemies = []
        self._respawn_player()
        self._generate_level()

    def _draw_hud(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.display.blit(lives_text, (8, 8))

    def _draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.display.blit(overlay, (0, 0))
                             
        go_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.font.render("Press any key to restart", True, WHITE)
        self.display.blit(go_text, (self.width // 2 - go_text.get_width() // 2, self.height // 2 - go_text.get_height() - 8))
        self.display.blit(restart_text, (self.width // 2 - restart_text.get_width() //2, self.height // 2 + 8))
 
    def _next_level(self):
        # Clear map, enemies, place player back at start, and regenerate
        self.pending_hole_fall = False
        self.map = [[0] * self.tile_rows for _ in range(self.tile_cols)]
        self.enemies = []

        # Reset player to starting position
        self.player.gridx = INITIAL_PLAYER_GRID_X
        self.player.gridy = INITIAL_PLAYER_GRID_Y
        self.player.x = INITIAL_PLAYER_GRID_X * self.tile_width
        self.player.y = INITIAL_PLAYER_GRID_Y * self.tile_height
        self.map[INITIAL_PLAYER_GRID_X][INITIAL_PLAYER_GRID_Y] = self.player

        self._generate_level()


    def _draw(self):
        ### Draw the pre-baked tile layer: a single blit covers the whole background
        self.display.blit(self.tile_layer, (0, 0))

        # draw hole
        self.hole.draw(self.display)


        ## draw enemies
        for enemy in self.enemies:
            enemy.draw(self.display)

        ## draw player
        self.player.draw(self.display)
        self._draw_hud()

        if self.game_over:
            self._draw_game_over()

        pygame.display.update()


    def _update(self):

        if self.game_over:
            return
        self.player.update()

        if self.pending_death and not self.player.is_moving and all(not e.is_moving for e in self.enemies):
            self.pending_death = False
            self.player.start_death()

       # Once the player finishes sliding onto the hole tile, start the fall animation
        if self.pending_hole_fall and not self.player.is_moving:
            self.pending_hole_fall = False
            self.player.start_hole_fall()

        if self.player.death_done:
            self.player.death_done = False
            self._lose_life()
            return

        # When the player's fall animation finishes, load the next level
        if self.player.hole_fall_done:
            self.player.hole_fall_done = False
            self._next_level()
            return

        # Update enemies (frozen while player is falling through a hole)
        if not self.player.hole_falling and not self.player.dying:
            for enemy in self.enemies:
                enemy.update()