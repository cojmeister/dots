from typing import Final

import pygame

from app.entities.colors import BaseColorTheme
from app.entities.grid import Grid
from app.entities.line import Line

WINDOW_SIZE: Final[int] = 500
FPS: Final[int] = 30

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Dots")
clock = pygame.time.Clock()  # For syncing the FPS
grid = Grid(size=12)

# Game loop
running = True
while running:

    # 1 Process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occurred till now and keeps tab of them.
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

    # 2 Update

    # 3 Draw/render
    screen.fill(BaseColorTheme['BG'])
    ########################

    grid.render(window=screen)
    line = Line()
    print(pygame.mouse.get_pressed(3))
    while pygame.mouse.get_pressed(3)[0]:
        for dot in grid.dots.reshape(-1):
            if dot.mouse_in_zone(pygame.mouse.get_pos()):
                line.append(dot)
    if line.nodes:
        print(line.nodes)

    ########################

    # Done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
