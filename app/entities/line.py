from typing import List, Optional, Tuple

from app.entities.dot import Dot


class Line:
    def __init__(self):
        self.value: Optional[int] = None
        self.color: Optional[Tuple[int, int, int]] = None
        self.nodes: List[Dot] = []

    def append(self, dot: Dot) -> bool:
        print(len(self.nodes))
        if self._check_values(dot):
            # dot.select()
            self.nodes.append(dot)
            return True
        return False

    def _check_indexes(self, dot: Dot) -> bool:
        last_dot = self.nodes[-1]
        if ((last_dot.x_ind + 1 == dot.x_ind) or (last_dot.x_ind - 1 == dot.x_ind)) and \
                ((last_dot.y_ind + 1 == dot.y_ind) or (last_dot.y_ind - 1 == dot.y_ind)):
            return True
        return False

    def _check_values(self, dot: Dot) -> bool:
        if not self.nodes:
            self.value = dot.value
            self.color = dot.color
            return True

        if self.value == dot.value:
            return self._check_indexes(dot)

        return False
