from typing import Optional

import numpy as np
import pygame

from app.entities.line import Line


class Grid:
    def __init__(self, size: int = 6, screen: Optional[pygame.Surface] = None,
                 screen_dim: int = 500, fps: int = 30):
        self.grid_size: int = size
        self.dots: np.ndarray = np.random.randint(1, 6, (6, 6))
        self.screen: Optional[pygame.Surface] = screen
        self.screen_dim: int = screen_dim
        self.fps: int = fps
        self.score: int = 0
        self.turns_left: int = 30

    def render(self, line: Optional[Line] = None):
        pass

    def update(self):
        pass
