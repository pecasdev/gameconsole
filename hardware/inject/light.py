from random import randrange
from engine import Object
from screen import Screen
from font.font_small import font_small
from hardware_state import HardwareState
from engine import now
from .light_state import LightState


class Light(Object):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.state = LightState()

    def step(self, screen: Screen):
        font_small.set_screen(screen)

        self.state.handle_deadline()

        if HardwareState.ALPHA.just_pressed():
            self.state.handle_alpha_press()

        reaction_duration = self.state.reaction_duration
        if reaction_duration is not None:
            if reaction_duration == -1:
                font_small.draw_string(self.x, self.y + 20, "too soon")
            else:
                font_small.draw_string(self.x, self.y + 20, f"{reaction_duration} ms")

        font_small.draw_string(self.x, self.y, self.state.state)
