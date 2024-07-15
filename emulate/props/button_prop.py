from enum import Enum
from .prop import Prop


class ButtonProp(Prop):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.pressed_down = False

    def draw(self):
        pass


class Direction(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

    def draw(self):
        pass
