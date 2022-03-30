import logging
from typing import Optional, Dict, List

import numpy as np

from app.entities.colors import colorType, BaseColorTheme
from app.utils import line_type, node_type

logger = logging.getLogger()


class Line:
    def __init__(self, grid: np.ndarray = np.empty((6, 6)),
                 color_theme: Dict[int, colorType] = BaseColorTheme,
                 width=5
                 ):
        self.value: Optional[int] = None
        self.grid: np.ndarray = grid
        self.nodes: line_type = []
        self.color_theme: Dict[int | str, colorType] = color_theme
        self.width = width
        self.end: bool = False
        self.closed: Optional[node_type] = None
        self.valid: bool = False

    def append(self, dot: node_type | None | List[int] | np.ndarray) -> bool:
        dot = tuple(int(i) for i in dot)
        if dot is None:
            return False
        # If line matches dot's color
        if not self._check_values(dot):
            return False

        # If line is being ended:
        if not self._check_end(dot):
            return False

        # If dot is adjacent, but not diagonal
        if not self._check_indexes(dot):
            return False

        # If line is a closed loop
        closed = self._checked_closed(dot)
        if closed:
            self.closed = closed

        # Then append the node to the list:
        # logger.debug(f"Appending Dot at {dot} \n\t Value: {self.grid[dot]}")
        self.nodes.append(dot)

        # Check if valid
        if len(self) >= 2:
            self.valid = True
        # And return True
        return True

    def _check_values(self, dot: node_type) -> bool:
        dot_value: int = self.grid[dot]
        # If line is empty, make line value that of first dot
        if not self.nodes:
            self.value = dot_value
            return True

        # If line isn't empty check if value is correct.
        if self.value == dot_value:
            return True

        return False

    def _check_indexes(self, dot: node_type) -> bool:
        if not self.nodes:
            return True

        last_dot = self.nodes[-1]

        delta_x: int = (last_dot[0] - dot[0]) ** 2
        delta_y: int = (last_dot[1] - dot[1]) ** 2

        if 0 < delta_x + delta_y <= 1:
            return True
        return False

    def _checked_closed(self, dot: node_type) -> Optional[node_type]:
        if dot in self.nodes[:-2]:
            return dot
        return None

    def _check_end(self, dot):
        if len(self) == 0:
            return True

        if dot == self.nodes[-1]:
            self.end = True
            return False
        return True

    def __len__(self) -> int:
        return len(self.nodes)

    def __str__(self):
        out = "Line"
        if self.valid:
            out += " - Valid"
        if self.end:
            out += " - Ended - "
        return out + ", ".join([f"({dot[0]},{dot[1]})" for dot in self.nodes])
