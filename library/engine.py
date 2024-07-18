from hardware_state import ButtonState, HardwareState
from screen import Screen
import time


class Object:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def create(self):
        pass

    def prestep(self):
        pass

    def step(self):
        pass

    def kill(self):
        Engine.remove_object(self)

    def poststep(self):
        pass


def now() -> int:
    if hasattr(time, "ticks_ms"):
        return int(time.ticks_ms())  # type: ignore
    else:
        return int(time.time() * 1000)


class Engine:
    objects = []
    tick_cap = 100

    @staticmethod
    def set_tick_cap(tick_cap: int):
        Engine.tick_cap = tick_cap

    @staticmethod
    def set_screen(screen: Screen):
        Engine.screen = screen

    @staticmethod
    def create_object(obj: Object):
        Engine.objects.append(obj)
        obj.create()
    
    @staticmethod
    def remove_object(obj: Object):
        Engine.objects.remove(obj)

    @staticmethod
    def update_hardware_state(hardware_state_dict: dict[str, ButtonState]):
        HardwareState.update_from_dict(hardware_state_dict)

    @staticmethod
    def __tick_sleep(start, end):
        surplus_time = (1000 / Engine.tick_cap) - (end - start)

        if surplus_time > 0:
            time.sleep(surplus_time / 1000)

    @staticmethod
    def __process_objects():
        for obj in Engine.objects:
            obj.prestep()

        Engine.screen.clear()

        for obj in Engine.objects:
            obj.step()

        Engine.screen.flush()

        for obj in Engine.objects:
            obj.poststep()

    @staticmethod
    def tick():
        tick_started = now()
        Engine.__process_objects()
        tick_ended = now()

        Engine.__tick_sleep(tick_started, tick_ended)
