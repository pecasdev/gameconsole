from engine import Engine
from alarm import Alarm
from random import randrange


class State:
    def __init__(self) -> None:
        self.__state = "idle"

        self.ready_to_capture_start = False
        self.ready_to_capture_end = False
        self.reaction_too_early = False

        self.current_alarm: Alarm | None = None

    def get_state(self):
        return self.__state

    def __new_alarm_change_to_go(self):
        def func():
            self.change_state_to("go")

        alarm = Alarm(func, randrange(2000, 3500))
        return alarm

    def change_state_to(self, new_state):
        if new_state == "wait":
            self.current_alarm = Engine.create_alarm(self.__new_alarm_change_to_go())
            self.ready_to_capture_end = False

        if new_state == "go":
            self.ready_to_capture_start = True
            self.ready_to_capture_end = True

        if new_state == "idle":
            if self.current_alarm is not None:
                self.current_alarm.stop()

        self.__state = new_state

    def handle_alpha_press(self):
        if self.__state == "idle":
            self.change_state_to("wait")
            return

        if self.__state == "wait":
            self.reaction_too_early = True
            self.change_state_to("idle")
            return

        if self.__state == "go":
            self.change_state_to("idle")
            return
