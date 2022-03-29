import logging
from typing import Optional

import pygame

from app.entities.line import Line
from entities.colors import BaseColorTheme, SecondaryColorTheme
from entities.grid import Grid
# Get constants
from utils import check_events
from utils.constants import *
from utils.utils import render_end_screen

# Create logger
logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Logging StartUp")

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE * 1.2))
screen.fill(BaseColorTheme['BG'])
pygame.display.set_caption("Dots")
clock = pygame.time.Clock()  # For syncing the FPS

# Initialize grid and first line
color_theme = SecondaryColorTheme
grid = Grid(size=6, screen=screen, color_theme=color_theme)
line: Optional[Line] = Line(grid=grid.dots, color_theme=color_theme)

# Game loop
running: int = True
end_screen: bool = False

while running:
    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time

    running, mouse_pos, esc, reset = check_events()

    if mouse_pos[-1]:
        index: node_type = grid.get_mouse_ind(mouse_pos)
        line.append(index)

    if line.end:
        logger.info("Line Finished - Updating Grid")
        grid.update(line)
        line = Line(grid=grid.dots,
                    color_theme=color_theme)

    if esc:
        logger.info("Line Terminated")
        line = Line(grid=grid.dots,
                    color_theme=color_theme)

    if reset:
        logger.info("Resetting Grid")
        grid.reset()
        line = Line(grid=grid.dots,
                    color_theme=color_theme)

    if grid.turns_left == 0:
        end_screen: bool = True

    # 3 Render Screen
    if not end_screen:
        grid.render(line)
    else:
        running, reset_end = render_end_screen(color_theme, screen, mouse_pos[-1], grid.score)

        if reset_end and mouse_pos[-1]:
            logger.info("Game Restart")
            grid.reset()
            line = Line(grid=grid.dots,
                        color_theme=color_theme)
            end_screen = False

logger.info("Quitting Game")

pygame.quit()
