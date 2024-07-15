import pygame

from .prop import Prop
from .arrange_config import DPAD
from .button_prop import ButtonProp, Direction


class DirectionalButton(ButtonProp):
    pressed_down: bool

    # coordinates given with assumption: center of dpad
    def __init__(self, x: int, y: int, direction: Direction):
        super().__init__(x, y)
        self.direction = direction
        self.pressed_down = False

    def draw(self, surface: pygame.Surface):
        short = DPAD["SHORT_LENGTH"]
        long = DPAD["LONG_LENGTH"]
        off = DPAD["CENTER_OFFSET"]

        if self.direction == Direction.DOWN:
            rect = pygame.Rect(self.x - short / 2, self.y + off, short, long)
        if self.direction == Direction.LEFT:
            rect = pygame.Rect(self.x - long - off, self.y - short / 2, long, short)
        if self.direction == Direction.RIGHT:
            rect = pygame.Rect(self.x + off, self.y - short / 2, long, short)
        if self.direction == Direction.UP:
            rect = pygame.Rect(self.x - short / 2, self.y - off - long, short, long)

        color = DPAD["COLOR_DOWN"] if self.pressed_down else DPAD["COLOR_UP"]
        pygame.draw.rect(surface, color, rect)


class DirectionalPad(Prop):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.buttons = {
            Direction.LEFT: DirectionalButton(x, y, Direction.LEFT),
            Direction.RIGHT: DirectionalButton(x, y, Direction.RIGHT),
            Direction.UP: DirectionalButton(x, y, Direction.UP),
            Direction.DOWN: DirectionalButton(x, y, Direction.DOWN),
        }

    def press_button(self, direction: Direction):
        self.buttons[direction].pressed_down = True

    def release_button(self, direction: Direction):
        self.buttons[direction].pressed_down = False

    def draw(self, surface):
        # pygame.draw.rect(surface, pygame.Color("black"), [self.x - 1, self.y - 1, 2, 2])
        for button in self.buttons.values():
            button.draw(surface)