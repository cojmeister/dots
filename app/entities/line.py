import logging
from typing import List, Optional, Tuple, Dict

import numpy as np

from app.entities.colors import colorType, BaseColorTheme

logger = logging.getLogger()


class Line:
    def __init__(self, grid: np.ndarray = np.empty((6, 6)),
                 color_theme: Dict[int, colorType] = BaseColorTheme,
                 ):
        self.value: Optional[int] = None
        self.grid: np.ndarray = grid
        self.nodes: List[Tuple[int, int]] = []
        self.color_theme: Dict[int | str, colorType] = color_theme
        self.width = 3
        self.end: bool = False
        self.closed: bool = False
        self.valid: bool = False

    def append(self, dot: Tuple[int, int]) -> bool:
        # If line matches dot's color
        if not self._check_values(dot):
            return False
        # If dot is adjacent, but not diagonal
        if not self._check_indexes(dot):
            return False
        # If line is a closed loop
        if self._checked_closed(dot):
            self.closed = True
        # Then append the node to the list:
        self.nodes.append(dot)
        # And return True
        return True

    def _check_values(self, dot: Tuple[int, int]) -> bool:
        dot_value: int = self.grid[dot]
        # If line is empty, make line value that of first dot
        if not self.nodes:
            self.value = dot_value
            return True

        # If line isn't empty check if value is correct.
        if self.value == dot_value:
            return True

        return False

    def _check_indexes(self, dot: Tuple[int, int]) -> bool:
        if not self.nodes:
            return True

        last_dot = self.nodes[-1]

        horizontal_condition: bool = 0 < (last_dot[0] - dot[0]) ** 2 <= 1
        vertical_condition: bool = 0 < (last_dot[1] - dot[1]) ** 2 <= 1

        if vertical_condition or horizontal_condition:
            return True
        return False

    def _checked_closed(self, dot: Tuple[int, int]) -> bool:
        pass

    def __len__(self) -> int:
        return len(self.nodes)

    def __str__(self):
        return "Line: " + ", ".join([f"({dot[0]},{dot[1]})" for dot in self.nodes])
