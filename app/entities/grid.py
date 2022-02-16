import numpy as np
import pygame

from app.entities.colors import BaseColorTheme
from app.entities.dot import Dot


class Grid:
    def __init__(self, size: int = 6, window_size: int = 500):
        self.size: int = size
        self.window_size: int = window_size
        self.dots: np.ndarray = np.array(
            [[Dot(i, j, BaseColorTheme(np.random.randint(0, 6))) for i in range(self.size)] for j in range(self.size)])

    def render(self, window: pygame.display):
        pass
