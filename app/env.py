from abc import ABC
from enum import Enum, auto
from typing import Optional, Tuple, Dict, Type, List

import gym
import numpy as np
import pygame
from gym import spaces

from app.entities.grid import Grid
from app.entities.line import Line
from app.utils.constants import FPS, node_type

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
    The action space is given by an N*N vector, which is then reshaped into an (N,N) matrix.
    The values vary from 0 to 36:
        -0 being not selected
        -1 being the line first point
        -2 the second
        - and so on,
    it doesn't need to cover all dots, as long as it is 2 dots long it works.

    ### Game Dynamics:
    Given an action if there is no selected dot, the dot will be selected.  Otherwise, if the dot is adjacent to the
    previous dot in the line and of the same value (color) as the previous dot in the line, the dot will be
    added (appended) to the line.  If the dot chosen is the same as the previous selected dot, then the line is ended,
    reducing the turns left by one, and adding to the game score by the length of the line (or the amount of dots
    of said value/color if the line is closed).
    The grid is then updated and a new turn begins.

    ### Rewards:
    * 0.0 for dot correctly appended to line
    * 1*N where N is the score added to the game
    * -1.0 when an incorrect dot is selected.
    Unless a factor dict is provided.

    ### Starting State:
    The starting state is a randomly initialized grid.
    30 Turns left and score is 0.
    Unless turns left is provided.

    ### Episode Termination:
    The episode terminates when there are no turns left, i.e.:
     - not bool(turns_left>0)

    ### Arguments:
    Parameters
    ----------
    initial_turns: int with the default amount of initial turns, it will always be this value;
                    unless specified in reset method
    grid_size: int  -grid size for gameplay.

    '''
    env = Dots(initial_turns=10,  grid_size=5)
    '''

    '''
    rewards = {"append": 0.1, "end": 1, "fail_to_append": -5}
    env = Dots(rewards=rewards)
    '''

    """
    metadata = {
        "render_modes": ["human", "ansi"],
        "render_fps": FPS,
    }

    class PossibleActions(Enum):
        """
        An Enum class representing the different possible outcomes for the actions, from here
        we set the reward.
        """
        ProperLine = auto()
        GapInNodes = auto()
        RepeatedPoints = auto()
        LineInvalid = auto()
        LineTooShort = auto()

    def __init__(self,
                 initial_turns: int = 30,
                 grid_size: int = 6):
        # Initialize Pygame and set variables
        pygame.init()
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None

        # Set Grid and Line, needed to play the game.
        self.grid: Optional[Grid] = None
        self.line: Optional[Line] = None

        self.default_initial_turns: int = initial_turns
        self.default_grid_size: int = grid_size

        # Defining action space as a selection of the next dot, if the same dot is selected then release
        # self.action_space = spaces.MultiDiscrete([self.default_grid_size, self.default_grid_size], dtype=np.uint8)

        # But, what if we define the action space as the selection of the line?
        # We define a box, where the value of the number represents the index in the line
        space_squared: int = int(self.default_grid_size ** 2)
        self.action_space = spaces.Box(low=0, high=space_squared,
                                       shape=(space_squared,),
                                       dtype=int)
        # self.action_space = spaces.Box(low=0, high=int(space_squared),
        #                                        shape=(self.default_grid_size, self.default_grid_size),
        #                                        dtype=int)

        # Observation Space is an NxN grid with the amount of dots in grid.
        self.observation_space = spaces.Box(low=1, high=6, shape=(self.default_grid_size, self.default_grid_size),
                                            dtype=np.uint8)

        # This is currently irrelevant, in case that the algorithm can interpret Tuples then we'd be able to return the
        # score and turns left in the observation as well.
        # self.min_score: Final[int] = 0
        # self.max_score: Final[int] = 1_000
        #
        # self.min_turns: Final[int] = 0
        # self.max_turns: Final[int] = initial_turns
        #
        # self.low = np.array([self.min_score, self.min_turns], dtype=np.uint32)
        # self.high = np.array([self.max_score, self.max_turns], dtype=np.uint32)
        #
        # self.observation_space = spaces.Tuple(
        #     spaces.Box(low=1, high=6, shape=(self.default_grid_size, self.default_grid_size), dtype=np.uint8),
        #     spaces.Box(low=self.low, high=self.high))

    def _destroy(self):
        """
        Destroys the grid and line variables
        Returns
        -------

        """
        if not self.grid and not self.grid:
            pass
        self.grid = None
        self.line = None

    def _create_grid(self,
                     initial_turns: Optional[int] = None):
        """
        Creates a grid and line with proper grid nodes.
        Parameters
        ----------
        initial_turns: optional parameter that sets the initial turns for the rest of the environment

        Returns
        -------

        """
        if initial_turns is None:
            initial_turns = self.default_initial_turns
        self.grid = Grid(size=self.default_grid_size,
                         screen=self.screen,
                         initial_turns=initial_turns)
        self.line = Line(grid=self.grid.dots)

    def step(self, action: np.ndarray) -> Tuple[observation_type, float, bool, Dict[str, int]]:
        """
        The environments' step function, each time this is called, the environment processes an action,
        and applies a reward. Each time it is called it is considered a time-step.

        Parameters
        ----------
        action: a numpy vector with values ranging: [0,36] containing a set of numbers selecting the dots
         (numbers must be in ascending order)

        Returns
        -------
        A tuple containing: observation, reward, done and info
        observation: the next state, an N*N matrix (N is grid size), showing the dots.
        reward: the reward for the step.
        done: whether the episode is done or not.
        info: a dict containing additional info: score, and turns left.

        """
        assert self.action_space.contains(
            action
        ), f"{action!r} ({type(action)}) invalid"

        if self.grid is None:
            self._create_grid()

        reward = self._get_reward(action)

        done: bool = not bool(self.grid.turns_left > 0)

        info: Dict[str, int] = {"score": self.grid.score, "turns_left": self.grid.turns_left}

        return self._get_obs, reward, done, info

    @property
    def _get_obs(self) -> observation_type:
        """
        Get the observation
        Returns
        -------
        The observation:
            The next state, an N*N matrix (N is grid size), showing the dots.
        """
        return self.grid.dots

    def reset(self,
              return_info: bool = False,
              initial_turns: Optional[int] = None) \
            -> observation_type | Tuple[observation_type, Dict[str, int]]:
        """
        Resets the environment when the episode is finished.
        Parameters
        ----------
        return_info: if true the reset method returns info (turns left and score)
        initial_turns: ability to set the amount of initial turns.

        Returns
        -------
        The initial observation: the next state, an N*N matrix (N is grid size), showing the dots.
        If initial_turns is true: returns info as well, a dict containing additional info: score, and turns left.

        """
        if initial_turns is None:
            initial_turns = self.default_initial_turns
        self._create_grid(initial_turns)

        if return_info:
            return self._get_obs, {"score": 0, "turns_left": 30}
        else:
            return self._get_obs

    def render(self, mode: str = "human"):
        return NotImplementedError

    def __repr__(self) -> str:
        out: List[str] = ["Dots environment;"]

        grid_size = self.grid.grid_size if self.grid is not None else self.default_grid_size
        turns = self.grid.turns_left if self.grid is not None else self.default_initial_turns
        out += [f"Grid Size: {grid_size} - Initial Turns: {turns}"]
        out += [f"Action Space: {self.action_space}"]
        out += [f"Observation Space: {self.observation_space}"]
        return "\n".join(out)

    def __str__(self) -> str:
        return self.__repr__()

    def parse_action(self, action: np.ndarray) -> 'Dots.PossibleActions':
        """
        Parses the action given in the step.
        Basically reshapes the vector and set the values to ints,
         and then applies different logics to returns the action type.
        Parameters
        ----------
        action: an (N*N,) vector containing values [0,N*N], with the action taken.

        Returns
        -------
        An enum of the action type made.
        """

        def manhattan(tuple1: node_type, tuple2: node_type) -> float:
            # Returns the Manhattan distance between two tuples.
            return abs(tuple1[0] - tuple2[0]) + abs(tuple1[1] - tuple2[1])

        def line_is_closable(last_node: node_type) -> bool:
            # Determines whether the line can be a closed loop
            for node in self.line.nodes[-2:]:
                if manhattan(last_node, node) == 1:
                    return True
            return False

        # Reshape the action
        action = action.reshape((6, 6)).astype(int)

        # If there is only one value then the line is too short
        if action.astype(bool).sum() <= 1:
            return self.PossibleActions.LineTooShort

        nodes = []
        end = int(np.max(action) + 1)
        # For every dot selected
        for i in range(1, end):
            # Check which dot has been selected
            x_ind, y_ind = np.where(action == i)

            # If there is no such node, then there is a gap in the numbering
            if len(x_ind) == 0:
                return self.PossibleActions.GapInNodes
            # If there is more than one selected node then there is a repeated point.
            elif len(x_ind) > 1:
                return self.PossibleActions.RepeatedPoints
            # Otherwise, we append it to the interim list
            else:
                nodes.append((x_ind[0], y_ind[0]))

        # If all nodes in the interim list are appended to the line
        if all([self.line.append(node) for node in nodes]):
            # If the length of the line is bigger than 4 we check if its closable
            if (len(self.line) > 4) and line_is_closable(nodes[-1]):
                # If it is, then we close it
                self.line.closed = True
            else:
                # Otherwise, we leave it open
                self.line.closed = False
            # Return a proper-line value because the nodes were appended successfully
            return self.PossibleActions.ProperLine

        # If the nodes are incorrect then  the line is invalid.
        return self.PossibleActions.LineInvalid

    def _get_reward(self, action: np.ndarray) -> float:
        """
        Given an action calculate the reward.
        Parameters
        ----------
        action: an (N*N,) vector containing values [0,N*N], with the action taken.

        Returns
        -------
        The reward for doing such action.
        """
        reward: float = 0.0
        action_type: 'Dots.PossibleActions' = self.parse_action(action)

        if action_type is self.PossibleActions.LineTooShort:
            reward = -10

        if action_type is self.PossibleActions.ProperLine:
            reward = self.grid.update(self.line)
            self.line = Line(grid=self.grid.dots)

        if action_type is self.PossibleActions.RepeatedPoints:
            reward = -5.0

        if action_type is self.PossibleActions.GapInNodes:
            reward = -2.5

        if action_type is self.PossibleActions.LineInvalid:
            reward = -20.0

        return reward
