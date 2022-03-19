import logging
from typing import List, Optional, Tuple, Dict

import pygame

from app.entities.colors import colorType, BaseColorTheme
from app.entities.dot import Dot

logger = logging.getLogger()


class Line:
    def __init__(self):
        self.value: Optional[int] = None
        self.color: Optional[Tuple[int, int, int]] = None
        self.nodes: List[Dot] = []
        self.color_theme: Dict[int, colorType] = BaseColorTheme
        self.end: bool = False
        self.valid: bool = False

    def append(self, dot: Dot) -> bool:
        if self._check_values(dot):
            # dot.select()
            self.nodes.append(dot)
            if len(self) > 1:
                self.valid = True
            return True
        return False

    def _check_indexes(self, dot: Dot) -> bool:
        logger.debug("Checking Indexes")
        last_dot = self.nodes[-1]

        vertical_condition: bool = 0 < (last_dot.y_ind - dot.y_ind) ** 2 <= 1
        horizontal_condition: bool = 0 < (last_dot.x_ind - dot.x_ind) ** 2 <= 1

        if vertical_condition or horizontal_condition:
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
            if dot not in self.nodes:
                return self._check_indexes(dot)
            else:
                self._end()
        return False

    def render(self, window: pygame.surface, width: int = 3):
        if len(self) > 1:
            for dot1, dot2 in zip(self.nodes[:-1], self.nodes[1:]):
                pygame.draw.line(window, self.color, dot1.rect.center, dot2.rect.center, width=width)

        pygame.draw.line(window, self.color, self.nodes[-1].rect.center, pygame.mouse.get_pos(), width=width)

    def _end(self):
        logger.info(f"Ending line with {len(self)} dots.")
        self.end = True

    def __len__(self):
        return len(self.nodes)
