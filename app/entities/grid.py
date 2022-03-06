from typing import Tuple

import numpy as np
import pygame

from app.entities.dot import Dot


class Grid:
    def __init__(self, size: int = 6):
        self.grid_size: int = size
        self.dots: np.ndarray = np.array(
            [[Dot(i, j, np.random.randint(1, 6)) for i in range(self.grid_size)] for j in range(self.grid_size)])

    def render(self, window: pygame.Surface):
        window_size: Tuple[int, int] = window.get_size()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.dots[i, j].render(window, num_of_dots=self.grid_size)
