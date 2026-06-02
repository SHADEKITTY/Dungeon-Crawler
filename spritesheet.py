import pygame

def load_spritesheet(path, frame_width, frame_height, scale_to=None):
    sheet = pygame.image.load(path).convert_alpha()

    sheet_w, sheet_h = sheet.get_size()

    frames = []
    for y in range(0, sheet_h, frame_height):
        for x in range(0, sheet_w, frame_width):
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            if scale_to:
                frame = pygame.transform.scale(frame, (int(scale_to[0]),
                                                       int(scale_to[1])))
            frames.append(frame)

    return frames


class Animation:
    def __init__(self, frames, speed):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.timer = 0
    def tick(self):
        self.timer += 1
        if self.timer >= self.speed:
            self.timer = 0
            self.current_frame = (self.current_frame +1) % len(self.frames)
        return self.frames[self.current_frame]
    
    def get_frame(self):
        return self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0