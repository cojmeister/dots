import logging
from typing import Tuple, Any

import pygame

from app.utils import node_type

logger = logging.getLogger()


def check_events() -> Tuple[bool, Tuple[Any, bool], bool, bool]:
    running: bool = True
    esc: bool = False
    reset: bool = False
    mouse_pos: node_type = pygame.mouse.get_pos()
    mouse_pos_bool: bool = False
    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get Mouse position
            mouse_pos_bool: bool = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc = True
            elif event.key == pygame.K_SPACE:
                reset = True
    # If no click then reset mouse pos
    return running, (*mouse_pos, mouse_pos_bool), esc, reset
