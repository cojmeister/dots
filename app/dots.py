# Create logger
import logging
from typing import Optional

import pygame

from app.entities.line import Line
from entities.colors import BaseColorTheme
from entities.grid import Grid
# Create logger and get constants
from utils import check_events
from utils.constants import *

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.info("Logging StartUp")

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE * 1.2))
pygame.display.set_caption("Dots")
clock = pygame.time.Clock()  # For syncing the FPS
grid = Grid(size=6)

# Game loop
screen.fill(BaseColorTheme['BG'])
# grid.render(window=screen)
running: int = True
score: int = 0
turns: int = 30
line: Optional[Line] = None
while running:
    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    mouse_pos, running, line = check_events(line)

    grid.render(screen)
    # if line is None:
    #     logger.debug("Generating New Line")
    #     line = Line()
    #
    # # # 2 Update
    # # # Select dot that is in mouse position
    # # TODO: Check for efficiency
    # for dot in grid.dots.reshape(-1):  # We flatten the 2d array to iterate over it in a simpler manner
    #     if dot.rect.collidepoint(mouse_pos):
    #         logger.debug(f"Mouse in Dot {dot.x_ind}, {dot.y_ind}")
    #         # Select dot and append to line
    #         if line.append(dot.select()):
    #             logger.info(f"Line is {len(line.nodes)} dots long.")
    #
    # # 3 Draw/render
    # screen.fill(BaseColorTheme['BG'])
    # grid.render(window=screen)
    #
    # # Draw Line from last selected dot to current mouse position of there is a line
    # if len(line) > 0:
    #     line.render(screen)
    #
    # # If line end then remove dots, and update with new dots
    # if line.end:
    #     grid.remove(line.nodes)
    #     grid.update()
    #     if line.valid:
    #         score += len(line)
    #         turns -= 1
    #     logger.info(f"\tScore: {score} points! \n\t Turns Left {turns}")
    #     line = None
    #
    # # Print score
    # print_score_and_turns(screen, score, turns)
    #
    # # Done after drawing everything to the screen
    # pygame.display.flip()

pygame.quit()
