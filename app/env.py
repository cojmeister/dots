from abc import ABC
from typing import Optional, Final, Tuple, Dict, Type, List

import gym
import numpy as np
import pygame
from gym import spaces

from app.entities.grid import Grid
from app.entities.line import Line
from app.utils.constants import FPS

observation_type: Type = np.ndarray


class Dots(gym.Env, ABC):
    """
    ### Description
    The dots' environment is based on the Dots game for smartphones, where the user is presented a grid of dots of
    different colors and must join these in order to score points.  The user has 30 turns and each dot in the line
    that is selected is worth a point.  When the line is a closed loop, then all dots of that color are considered
    towards the score.
    When a line is finished the dots of the line are removed, and those above them are shifted downwards;
    if the line is a closed loop, all the dots of that same color are removed.

    The environment greatly mimics a gym environment, as it is meant to be used with
    stable-baselines3

    ### Observation Space
    The observation is a `ndarray` with shape `(6,6)` where the elements are integers between 1 and 6 (included) where
    each number is a different dot color.

    ### Action Space
    The actions are given as the indexes of the dots in the array, thus it considered a multi-discrete action space,
    where the two deterministic actions are:
    | Num | Observation                                                 | Min                | Max    |
    |-----|-------------------------------------------------------------|--------------------|--------|
    | 0   | X-Index of dot selected.                                    | 0                  | 5      |
    | 1   | Y-Index of dot selected.                                    | 0                  | 5      |

    ### Game Dynamics:
    Given an action if there is no selected dot, the dot will be selected.  Otherwise, if the dot is adjacent to the
    previous dot in the line and of the same value (color) as the previous dot in the line, the dot will be
    added (appended) to the line.  If the dot chosen is the same as the previous selected dot, then the line is ended,
    reducing the turns left by one, and adding to the game score by the length of the line (or the amount of dots
    of said value/color if the line is closed).
    The grid is then updated and a new turn begins.

    ### Rewards:
    * 0.1 for dot correctly appended to line
    * 1*N where N is the score added to the game
    * -0.5 when an incorrect dot is selected.

    ### Starting State
    The starting state is a randomly initialized grid.
    30 Turns left and score is 0.

    ### Episode Termination
    The episode terminates when there are no turns left, i.e.:
     - not bool(turns_left>0)

    """
    metadata = {
        "render_modes": ["human"],
        "render_fps": FPS,
    }

    def __init__(self):
        pygame.init()
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.grid: Optional[Grid] = None
        self.line: Optional[Line] = None

        self.min_score: Final[int] = 0
        self.max_score: Final[int] = 1_000

        self.min_turns: Final[int] = 0
        self.max_turns: Final[int] = 30

        self.action_space = spaces.MultiDiscrete([6, 6], dtype=np.uint8)

        self.low = np.array([self.min_score, self.min_turns], dtype=np.uint32)
        self.high = np.array([self.max_score, self.max_turns], dtype=np.uint32)

        self.observation_space = spaces.Box(low=1, high=6, shape=(6, 6), dtype=np.uint8)

    def _destroy(self):
        if not self.grid and not self.grid:
            return
        self.grid = None
        self.line = None

    def _create_grid(self, grid_size: int = 6):
        self.grid = Grid(size=grid_size, screen=self.screen)
        self.line = Line(grid=self.grid.dots)

    def step(self, action: np.ndarray | List[int]) -> Tuple[observation_type, float, bool, Dict[str, int]]:
        assert self.action_space.contains(
            action
        ), f"{action!r} ({type(action)}) invalid"

        if self.grid is None:
            self._create_grid()

        done: bool = not bool(self.grid.turns_left > 0)

        if self.line.append(action):
            reward = 0.1
        elif self.line.end:
            reward = self.grid.update(self.line)
            self.line = Line(self.grid.dots)
        else:
            reward = -0.5

        info: Dict[str, int] = {"score": self.grid.score, "turns_left": self.grid.turns_left}

        return self._get_obs, reward, done, info

    @property
    def _get_obs(self) -> observation_type:
        return self.grid.dots

    def reset(self,
              seed: Optional[int] = None,
              return_info: bool = False,
              options: Optional[dict] = None) -> observation_type | Tuple[observation_type, Dict[str, int]]:
        self._create_grid()

        if not return_info:
            return self._get_obs
        else:
            return self._get_obs, {"score": 0, "turns_left": 30}

    def render(self, mode="human"):
        return NotImplementedError
