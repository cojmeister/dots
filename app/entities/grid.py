from typing import Optional, Dict, Tuple

import numpy as np
import pygame

from app.entities.colors import colorType, BaseColorTheme
from app.entities.line import Line


class Grid:
    def __init__(self, size: int = 6,
                 screen: Optional[pygame.Surface] = None,
                 screen_dim: int = 500,
                 color_theme: Dict[int, colorType] = BaseColorTheme,
                 dot_radius: int = 10
                 ):
        self.grid_size: int = size
        self.screen: Optional[pygame.Surface] = screen
        self.screen_dim: int = screen_dim
        self.color_theme: Dict[int | str, colorType] = color_theme
        self.dots: np.ndarray = np.random.randint(1, 6, (size, size))
        self.score: int = 0
        self.turns_left: int = 30
        self.radius: int = dot_radius

    def render(self, mouse_pos, line: Optional[Line] = None):
        if self.screen is None:
            self._init_screen()
        self.screen.fill(BaseColorTheme['BG'])
        self._render_score_and_turns()
        self._render_dots()
        if line is not None:
            self._render_line(line, mouse_pos)

        pygame.display.flip()

    def update(self):
        pass

    def _init_screen(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("Dots")
        self.screen = pygame.display.set_mode((self.screen_dim, self.screen_dim * 1.2))

    def _render_score_and_turns(self):
        width, starting_height = self.screen_dim, self.screen_dim
        height = self.screen_dim * 0.2

        font_small: pygame.font.Font = pygame.font.SysFont("arial", int(width / 20))
        font_big: pygame.font.Font = pygame.font.SysFont("arial_bold", int(width / 10))

        score_title = font_small.render("SCORE", True, self.color_theme['text'])
        score_title_rect = score_title.get_rect()
        score_title_rect.center = (width // 4, starting_height)
        self.screen.blit(score_title, score_title_rect)

        score_number = font_big.render(f"{self.score}", True, self.color_theme['text'])
        score_number_rect = score_number.get_rect()
        score_number_rect.center = (width // 4, starting_height + score_title_rect.height * 1.2)
        self.screen.blit(score_number, score_number_rect)

        turns_title = font_small.render("MOVES", True, self.color_theme['text'])
        turns_title_rect = turns_title.get_rect()
        turns_title_rect.center = (3 * (width // 4), starting_height)
        self.screen.blit(turns_title, turns_title_rect)

        turns_number = font_big.render(f"{self.turns_left}", True, self.color_theme['text'])
        turns_number_rect = turns_number.get_rect()
        turns_number_rect.center = (3 * (width // 4), starting_height + turns_title_rect.height * 1.2)
        self.screen.blit(turns_number, turns_number_rect)

        pygame.draw.line(self.screen, self.color_theme['text'], (width // 2, starting_height - score_title_rect.height),
                         (width // 2, starting_height + 0.8 * height), width=2)

    def _render_line(self, line: Line, mouse_pos: Tuple[int, int]):
        if not len(line):
            pass

        spacing: float = self.screen_dim / (self.grid_size + 1)
        line_color: colorType = self.color_theme[line.value]

        for dot1, dot2 in zip(line.nodes[:-1], line.nodes[1:]):
            dot1_y = (dot1[0] + 1) * spacing
            dot1_x = (dot1[1] + 1) * spacing

            dot2_y = (dot2[0] + 1) * spacing
            dot2_x = (dot2[1] + 1) * spacing

            pygame.draw.line(self.screen,
                             line_color,
                             (dot1_x, dot1_y),
                             (dot2_x, dot2_y),
                             width=line.width)

        pygame.draw.line(self.screen,
                         line_color,
                         (dot2_x, dot2_y),
                         pygame.mouse.get_pos(),
                         width=line.width)

    def _render_dots(self):
        spacing: float = self.screen_dim / (self.grid_size + 1)
        for i, row in enumerate(self.dots):
            y: int = int((i + 1) * spacing)
            for j, dot in enumerate(row):
                x: int = int((j + 1) * spacing)
                color = self.color_theme[dot]
                pygame.draw.circle(self.screen, color, (x, y), self.radius)
