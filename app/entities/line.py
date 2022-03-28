import logging
from typing import List, Optional, Tuple, Dict

import pygame

from app.entities.colors import colorType, BaseColorTheme
from app.entities.dot import Dot

logger = logging.getLogger()


class Line:
    def __init__(self, color_theme: Dict[int, colorType] = BaseColorTheme):
        self.value: Optional[int] = None
        self.color: Optional[Tuple[int, int, int]] = None
        self.nodes: List[Dot] = []
        self.color_theme: Dict[int, colorType] = color_theme
        self.end: bool = False
        self.valid: bool = False
        self.closed: bool = False

    def append(self, dot: Dot) -> bool:
        if self._check_values(dot):
            self.nodes.append(dot)
            if len(self) > 1:
                self.valid = True
            return True
        return False

    def _check_indexes(self, dot: Dot) -> bool:
        logger.debug("Checking Indexes")
        last_dot = self.nodes[-1]

        delta_x: int = (last_dot.x_ind - dot.x_ind) ** 2
        delta_y: int = (last_dot.y_ind - dot.y_ind) ** 2

        condition: bool = 0 < delta_x + delta_y < 2

        if condition:
            logger.debug("\t Indexes Correct")
            return True
        logger.debug("\t Indexes Incorrect")
        return False

    def _check_values(self, dot: Dot) -> bool:
        if not self.nodes:
            self.value = dot.value
            self.color: colorType = self.color_theme[self.value]
            return True

        if self.value == dot.value:
            return self._check_in_line(dot)

        return False

    def _check_in_line(self, dot: Dot) -> bool:
        if len(self) < 2:
            return self._check_indexes(dot)

        if dot is self.nodes[-1]:
            return self._end(closed=False)
        elif dot is self.nodes[-2]:
            return False
        elif dot in self.nodes[:-2]:
            return self._end(closed=True)

        return self._check_indexes(dot)

    def render(self, window: pygame.surface, width: int = 3):
        if len(self) > 1:
            for dot1, dot2 in zip(self.nodes[:-1], self.nodes[1:]):
                pygame.draw.line(window, self.color, dot1.rect.center, dot2.rect.center, width=width)

        pygame.draw.line(window, self.color, self.nodes[-1].rect.center, pygame.mouse.get_pos(), width=width)

    def _end(self, closed: bool = False) -> bool:
        if closed:
            self.closed = True
        logger.info(f"Ending line with {len(self)} dots.")
        self.end = True
        return False

    def __len__(self):
        return len(self.nodes)
