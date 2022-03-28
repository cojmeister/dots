import logging
from typing import List

import numpy as np
import pygame

from app.entities.dot import Dot

logger = logging.getLogger()


class Grid:
    def __init__(self, size: int = 6):
        self.grid_size: int = size
        self.dots: np.ndarray = np.array(
            [[Dot(i, j, np.random.randint(1, 6)) for i in range(self.grid_size)] for j in range(self.grid_size)])

    def render(self, window: pygame.Surface):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.dots[i, j].render(window, num_of_dots=self.grid_size)

    @property
    def matrix(self) -> np.ndarray:
        return np.array([dot.value for dot in self.dots.reshape(-1)]).reshape((6, 6))

    def update(self):
        out = np.array([self.__process_column(column, index) for index, column in enumerate(self.dots.T)]).T
        # print("New \n" + "\n".join(" - ".join(f"{dot.value}" for dot in row) for row in out))
        print(out - self.dots)
        self.dots = out
        return out

    def __process_column(self, column: np.ndarray, col_index: int) -> np.ndarray:
        new_col: List[Dot] = [dot for dot in column[::-1] if not dot.selected]
        while len(new_col) < self.grid_size:
            new_col.append(Dot(len(new_col) - 1, col_index, np.random.randint(1, 6)))

        return np.array(new_col[::-1])

    def randomize(self):
        for dot in self.dots.reshape(-1):
            dot.value = np.random.randint(1, 6)

    def __str__(self) -> str:
        return "\n".join(" - ".join(f"{dot.value}" for dot in row) for row in self.dots)
