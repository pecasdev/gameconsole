import pygame

from .selection_button import SelectionButtons
from .directional_button import DirectionalPad
from .arrange_config import CASE, DPAD, OLED, SBUT
from .case_prop import CaseProp
from .oled_prop import OledProp
from .prop import Prop


class HardwareProp(Prop):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

        self.case_prop = CaseProp(self.x, self.y)
        self.oled_prop = OledProp(
            self.x + CASE["WIDTH"] / 2 - OLED["WIDTH"] / 2,
            self.y + OLED["CASE_Y_OFF"],
        )
        self.dpad_prop = DirectionalPad(
            self.x + DPAD["CASE_LEFT_X_OFF"], self.y + DPAD["CASE_Y_OFF"]
        )
        self.sbut_prop = SelectionButtons(
            self.x + CASE["WIDTH"] - SBUT["CASE_RIGHT_X_OFF"],
            self.y + DPAD["CASE_Y_OFF"],
        )

    def blit_to_surface(self, surface: pygame.Surface):
        self.case_prop.draw(surface)
        self.oled_prop.draw(surface)
        self.dpad_prop.draw(surface)
        self.sbut_prop.draw(surface)
