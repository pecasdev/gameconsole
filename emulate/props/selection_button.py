import pygame

from .prop import Prop
from .arrange_config import SBUT
from .button_prop import ButtonProp


class SelectionButton(ButtonProp):
    pressed_down: bool

    def __init__(self, x: int, y: int, letter: str):
        super().__init__(x, y)
        self.letter = letter
        self.font = pygame.font.SysFont("Comic Sans MS", 19)

    def draw(self, surface: pygame.Surface):
        rect = pygame.Rect(
            self.x,
            self.y,
            SBUT["RADIUS"],
            SBUT["RADIUS"],
        )

        color = SBUT["COLOR_DOWN"] if self.pressed_down else SBUT["COLOR_UP"]
        pygame.draw.rect(surface, color, rect)
        text = self.font.render(self.letter, False, pygame.Color("black"))
        surface.blit(
            text,
            text.get_rect(
                center=(self.x + SBUT["RADIUS"] / 2, self.y + SBUT["RADIUS"] / 2)
            ),
        )


class SelectionButtons(Prop):
    # buttons look like:
    # |        B |
    # |      A   |

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        off = SBUT["CENTER_OFFSET"]
        self.buttons = {
            "ALPHA": SelectionButton(x - SBUT["RADIUS"] - off / 2, y + off / 2, "A"),
            "BETA": SelectionButton(
                x + off / 2 + SBUT["B_NUDGE"], y - SBUT["RADIUS"] - off / 2, "B"
            ),
        }

    def press_button(self, name: str):
        self.buttons[name].pressed_down = True

    def release_button(self, name: str):
        self.buttons[name].pressed_down = False

    def draw(self, surface):
        # pygame.draw.rect(surface, pygame.Color("black"), [self.x - 1, self.y - 1, 2, 2])
        for button in self.buttons.values():
            button.draw(surface)
