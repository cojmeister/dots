from app.entities.colors import BaseColorTheme


class Dot:
    def __init__(self, ind_x: int, ind_y: int, color: BaseColorTheme, selected: bool = False, radius: int = 10,
                 render: bool = True):
        """
        Constructor
        """
        self.ind_x: int = ind_x
        self.ind_y: int = ind_y
        self.selected: bool = selected
        self.color: BaseColorTheme = color
        self.radius: int = radius
        self.render: bool = render

    def select(self):
        if self.render:
            pass
        self.selected = True
