import hardware_state
import alarm
import time
import screen as libscreen
from now import now

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


# todo - add debug printing system to objects (sidetrack)

class Engine:
    objects = []
    alarms = []
    tick_cap = 100
    emulator_tick_override = False

    @staticmethod
    def set_tick_cap(tick_cap: int):
        Engine.tick_cap = tick_cap

    @staticmethod
    def set_screen(screen: "libscreen.Screen"):
        Engine.screen = screen

    @staticmethod
    def set_emulator_tick_override(emulator_tick_override):
        Engine.emulator_tick_override = emulator_tick_override

        if emulator_tick_override:
            import pygame

            Engine.clock = pygame.time.Clock()

    @staticmethod
    def objects_of_class(clazz):
        return filter(lambda x: isinstance(x, clazz), Engine.objects)

    @staticmethod
    def reset():
        Engine.objects = []
        Engine.alarms = []
        Engine.tick_cap = 100

    @staticmethod
    def create_object[O: Object](obj: O) -> O:
        Engine.objects.append(obj)
        obj.create()
        return obj

    @staticmethod
    def create_alarm(alarm: "alarm.Alarm"):
        Engine.alarms.append(alarm)
        alarm.start()
        return alarm

    @staticmethod
    def remove_object(obj: Object):
        Engine.objects.remove(obj)

    @staticmethod
    def update_hardware_state(
        hardware_state_dict: dict[str, "hardware_state.ButtonState"]
    ):
        hardware_state.HardwareState.update_from_dict(hardware_state_dict)

    @staticmethod
    def _tick_sleep(start, end):
        if Engine.emulator_tick_override:
            Engine.clock.tick(Engine.tick_cap)

        else:
            surplus_time = (1000 / Engine.tick_cap) - (end - start)

            if surplus_time > 0:
                time.sleep(surplus_time / 1000)

    @staticmethod
    def _process_alarms():
        to_remove = []
        for alarm in Engine.alarms:
            if alarm.handle():
                to_remove.append(alarm)

        for alarm in to_remove:
            Engine.alarms.remove(alarm)

    @staticmethod
    def _process_objects():
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
        Engine._process_alarms()
        Engine._process_objects()
        tick_ended = now()

        Engine._tick_sleep(tick_started, tick_ended)
