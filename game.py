import pygame

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

    def run_game_loop(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    def _setup_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption) 

    def _handle_events(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.running = False

    def _draw(self):
        self.display.fill(WHITE)

        for col in range(self.tile_cols):
            for row in range(self.tile_rows):
                rect = (col * self.tile_width, row * self.tile_height, self.tile_width, self.tile_height)
                pygame.draw.rect(self.display, BLACK, rect, 1)
        pygame.display.update()
    
    def _update(self):
        pass 