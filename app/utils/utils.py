import logging
from typing import Tuple, Dict, Union, Optional

import pygame

from app.entities.colors import BaseColorTheme, colorType
from app.entities.line import Line
from .constants import *

logger = logging.getLogger()


def check_events(line: Optional[Line]) -> Tuple[Tuple[int, int], bool, Line]:
    running: bool = True
    mouse_pos: Tuple[int, int] = (0, 0)
    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get Mouse position
            if pygame.mouse.get_pressed(NUM_OF_BUTTONS)[0]:
                mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if line is not None:
                    line.end = True
                    line.valid = False

    # If no click then reset mouse pos
    return mouse_pos, running, line


def print_score_and_turns(window: pygame.Surface, score: int, turns: int,
                          color_theme: Dict[Union[int, str], colorType] = BaseColorTheme):
    width, height = window.get_size()
    starting_height = height / 1.2
    height -= starting_height
    font_small: pygame.font.Font = pygame.font.SysFont("arial", int(width / 20))
    font_big: pygame.font.Font = pygame.font.SysFont("arial_bold", int(width / 10))

    score_title = font_small.render("SCORE", True, color_theme['text'])
    score_title_rect = score_title.get_rect()
    score_title_rect.center = (width // 4, starting_height)
    window.blit(score_title, score_title_rect)

    score_number = font_big.render(f"{score}", True, color_theme['text'])
    score_number_rect = score_number.get_rect()
    score_number_rect.center = (width // 4, starting_height + score_title_rect.height * 1.2)
    window.blit(score_number, score_number_rect)

    turns_title = font_small.render("MOVES", True, color_theme['text'])
    turns_title_rect = turns_title.get_rect()
    turns_title_rect.center = (3 * (width // 4), starting_height)
    window.blit(turns_title, turns_title_rect)

    turns_number = font_big.render(f"{turns}", True, color_theme['text'])
    turns_number_rect = turns_number.get_rect()
    turns_number_rect.center = (3 * (width // 4), starting_height + turns_title_rect.height * 1.2)
    window.blit(turns_number, turns_number_rect)

    pygame.draw.line(window, color_theme['text'], (width // 2, starting_height - score_title_rect.height),
                     (width // 2, starting_height + 0.8 * height), width=2)
