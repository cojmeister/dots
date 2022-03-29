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


def render_end_screen(color_theme, screen, click, score):
    width, height = screen.get_size()
    running, mouse, _, reset = check_events()

    screen.fill(color_theme["BG"])
    font: pygame.font.Font = pygame.font.SysFont("arial_bold", width // 10)

    score_text = font.render(f"{score}", True, color_theme[5])
    score_rect = score_text.get_rect()
    score_rect.center = (width // 2, 1 * height // 4)
    screen.blit(score_text, score_rect)

    restart_text = font.render("RESTART", True, 'white')
    restart_rect = restart_text.get_rect()
    restart_rect.center = (width // 2, 2 * height // 4)
    restart_highlight = restart_rect.inflate(restart_rect.width * 1.5 - restart_rect.width,
                                             restart_rect.height * 1.5 - restart_rect.height)
    if restart_highlight.collidepoint(mouse[:2]):
        pygame.draw.rect(screen,
                         color_theme[1],
                         restart_highlight,
                         width=0,
                         border_radius=3)
        reset = True
    else:
        pygame.draw.rect(screen,
                         color_theme[2],
                         restart_highlight,
                         width=0,
                         border_radius=3)

    screen.blit(restart_text, restart_rect)

    quit_text = font.render("QUIT", True, 'white')
    quit_rect = quit_text.get_rect()
    quit_rect.center = (width // 2, 3 * height // 4)
    quit_highlight = quit_rect.inflate(quit_rect.width * 1.5 - quit_rect.width,
                                       quit_rect.height * 1.5 - quit_rect.height)

    if quit_highlight.collidepoint(mouse[:2]):
        pygame.draw.rect(screen,
                         color_theme[3],
                         quit_highlight,
                         width=0,
                         border_radius=3)
        if click:
            running = False
    else:
        pygame.draw.rect(screen,
                         color_theme[4],
                         quit_highlight,
                         width=0,
                         border_radius=3)

    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

    return running, reset
