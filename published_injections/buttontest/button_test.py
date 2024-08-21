from engine import Object, Engine
from hardware_state import HardwareState


class ButtonTest(Object):
    def __init__(self):
        super().__init__(0, 0)
        self.clicks_registered = 0

    def step(self):
        if HardwareState.ALPHA.just_pressed():
            self.clicks_registered += 1

        Engine.screen.draw_text(20, 20, str(self.clicks_registered))
