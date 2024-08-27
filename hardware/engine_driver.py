from engine import Engine
from hardware_button_driver import (
    create_debounce_generator,
    HardwareButtonPin,
    create_hardware_listener_thread,
)
from hardware_state import ButtonState, HardwareState
from now import now

class EngineDriver:
    def __init__(self) -> None:
        button_name_to_hardware_button_pin = {
            "LEFT": HardwareButtonPin.LEFT,
            "RIGHT": HardwareButtonPin.RIGHT,
            "UP": HardwareButtonPin.UP,
            "DOWN": HardwareButtonPin.DOWN,
            "ALPHA": HardwareButtonPin.ALPHA,
            "BETA": HardwareButtonPin.BETA,
        }

        self.button_handlers = [
            self.__create_hardware_state_handler(name, create_debounce_generator(pin))
            for (name, pin) in button_name_to_hardware_button_pin.items()
        ]

        self.internal_hardware_state = HardwareState.as_dict()

        self.running = True

    def __create_hardware_state_handler(self, button_name, debounce_generator):
        def handle() -> tuple[str, ButtonState]:
            value = next(debounce_generator)
            button_state = ButtonState(value)
            return (button_name, button_state)

        return handle

    def update_internal_hardware_state(self):
        self.internal_hardware_state = self.__hardware_state_dict_from_prop()

    def update_engine_hardware_state(self):
        Engine.update_hardware_state(self.internal_hardware_state)

    def __hardware_state_dict_from_prop(self) -> dict[str, ButtonState]:
        return dict([handle() for handle in self.button_handlers])

    def runloop(self):
        create_hardware_listener_thread(self)
        # debug_print_hardware_state = handle_debug_print_hardware_state()

        while self.running:
            try:
                self.update_engine_hardware_state()
                # debug_print_hardware_state()

                Engine.tick()
                HardwareState.ack_button_states()

            except KeyboardInterrupt:
                self.running = False

        if not self.running:
            Engine.reset()
            HardwareState.reset()


# todo - replace with library debug function
def handle_debug_print_hardware_state():
    prev_line = ""

    def handle():
        nonlocal prev_line
        line = HardwareState.as_string()
        if line != prev_line:
            print(line)
            prev_line = line

    return handle
