from hardware_state import ButtonState, HardwareState
from screen import Screen
import time


class Object:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def create(self, screen: Screen):
        pass

    def step(self, screen: Screen):
        pass


def now() -> int:
    if hasattr(time, "ticks_ms"):
        return int(time.ticks_ms())  # type: ignore
    else:
        return int(time.time() * 1000)


class Engine:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.objects: list[Object] = []

    def create_object(self, obj: Object):
        self.objects.append(obj)
        obj.create(self.screen)

    def update_hardware_state(self, hardware_state_dict: dict[str, ButtonState]):
        HardwareState.update_from_dict(hardware_state_dict)

    def tick(self):
        self.screen.clear()
        for obj in self.objects:
            obj.step(self.screen)
        self.screen.flush()

    def kill(self):
        self.running = False
        self.screen.kill()
