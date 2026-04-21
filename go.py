from abc import ABC, abstractmethod

GREEN = (0, 255, 0)

class GameObject(ABC):
    def __init__(self):
        def __init__(self, gridx, gridy, x,  y, tile_width, tile_height, color):

            self.gridx = gridx
            self.gridy = gridy

            self.x = x
            self.y = y

            self.tile_width = tile_width
            self.tile_height = tile_height

            self.color = color

        @abstractmethod
        def draw(self, _surface):
            pass

        @abstractmethod
        def update(self):
            pass
