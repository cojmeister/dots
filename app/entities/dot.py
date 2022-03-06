from typing import Tuple, Dict, Union, Optional

import pygame

from app.entities.colors import BaseColorTheme, colorType


class Dot:
    def __init__(self, x_ind: int, y_ind: int, val: int, radius: int = 10):
        """
        Constructor
        """
        self.x_ind: int = x_ind
        self.y_ind: int = y_ind
        self.selected: bool = False
        self.currently_selected: bool = False
        self.value: int = val
        self.radius: int = radius

    def select(self, window: Optional[pygame.Surface] = None) -> 'Dot':
        self.selected = self.currently_selected = True
        if window is not None:
            pass
        return self

    def render(self, window: pygame.Surface, color_theme: Dict[int, colorType] = BaseColorTheme,
               num_of_dots: int = 6) -> None:
        color: colorType = color_theme[self.value]
        x, y = self._get_xy(window, num_of_dots)
        pygame.draw.circle(window, color, (x, y), self.radius)

    def _get_xy(self, window: pygame.Surface, num_of_dots: Union[int, Tuple[int, int]]) -> Tuple[float, float]:
        width, height = window.get_size()
        if type(num_of_dots) is tuple:
            spacing_x = width / (num_of_dots[0] + 1)
            spacing_y = height / (num_of_dots[1] + 1)
        else:
            spacing_x = width / (num_of_dots + 1)
            spacing_y = height / (num_of_dots + 1)

        x: float = (self.x_ind + 1) * spacing_x
        y: float = (self.y_ind + 1) * spacing_y

        return x, y
