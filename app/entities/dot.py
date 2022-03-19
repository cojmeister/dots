from functools import lru_cache
from typing import Tuple, Dict, Union, Optional

import pygame

from app.entities.colors import BaseColorTheme, colorType


class Dot:
    def __init__(self, x_ind: int, y_ind: int, val: int, radius: int = 10, window: Optional[pygame.Surface] = None):
        """
        Constructor
        """
        self.x_ind: int = x_ind
        self.y_ind: int = y_ind
        self.selected: bool = False
        self.currently_selected: bool = False
        self.value: int = val
        self.radius: int = radius
        self.rect: Optional[pygame.Rect] = None
        self.window: pygame.Surface = window

    def select(self, window: Optional[pygame.Surface] = None) -> 'Dot':
        self.selected = self.currently_selected = True
        if window is not None:
            pass
        return self

    def render(self, window: pygame.Surface, color_theme: Dict[int, colorType] = BaseColorTheme,
               num_of_dots: int = 6) -> None:
        color: colorType = color_theme[self.value]
        x, y, _, _ = self._get_xy(window, num_of_dots)
        self.rect: pygame.rect.Rect = pygame.draw.circle(window, color, (x, y), self.radius)

    @lru_cache(maxsize=1)
    def _get_xy(self, window: pygame.Surface, num_of_dots: Union[int, Tuple[int, int]] = 12) \
            -> Tuple[float, float, float, float]:
        width, height = window.get_size()
        height /= 1.2
        if type(num_of_dots) is tuple:
            spacing_x = width / (num_of_dots[0] + 1)
            spacing_y = height / (num_of_dots[1] + 1)
        else:
            spacing_x = width / (num_of_dots + 1)
            spacing_y = height / (num_of_dots + 1)

        x: float = (self.x_ind + 1) * spacing_x
        y: float = (self.y_ind + 1) * spacing_y

        return x, y, spacing_x, spacing_y

    @property
    def xy(self) -> Tuple[int, int]:
        return

    def mouse_in_zone(self, mouse_pos: Tuple[int, int], window: pygame.Surface,
                      num_of_dots: Union[int, Tuple[int, int]]) -> bool:
        """
        Check whether the mouse is close enough to a dot to select it.

        Parameters
        ----------
        mouse_pos: Current mouse position, a tuple used from pygame format.
        window: a pygame window
        num_of_dots: number of dots in the grid

        Returns
        -------
        True if mouse is close enough to dot
        False otherwise
        """
        x, y, spacing_x, spacing_y = self._get_xy(window, num_of_dots)

        delta_x: float = ((mouse_pos[0] - x) ** 2) ** 0.5 < spacing_x / 2
        delta_y: float = ((mouse_pos[1] - y) ** 2) ** 0.5 < spacing_y / 2
        if delta_x and delta_y:
            return True
        return False
