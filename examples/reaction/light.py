from random import randrange
from engine import Object
from screen import Screen
from hardware_state import HardwareState
from engine import now
from .light_state import LightState
from engine import Engine
from font import Font


class Light(Object):
    state: LightState

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.state = LightState()

    def prestep(self):
        if HardwareState.ALPHA.just_pressed():
            self.state.handle_alpha_press()

            if self.state.ready_to_capture_end:
                self.state.reaction_stamp_end = now()
                self.state.ready_to_capture_end = False

    def step(self):
        self.state.handle_deadline()

        self.state.calculate_reaction_time()
        reaction_duration = self.state.reaction_duration

        Font.set_current_font("small")
        if reaction_duration is not None:
            if reaction_duration == -1:
                Engine.screen.draw_string(self.x, self.y + 20, "too soon")
            else:
                Engine.screen.draw_string(
                    self.x, self.y + 20, f"{reaction_duration} ms"
                )

        Engine.screen.draw_string(self.x, self.y, self.state.state)

    def poststep(self):
        if self.state.ready_to_capture_start:
            self.state.reaction_stamp_start = now()
            self.state.ready_to_capture_start = False
