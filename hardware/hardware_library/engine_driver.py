from engine import Engine
from hardware_button_driver import (
    create_debounce_generator,
    HardwareButtonPin,
    create_hardware_listener_thread,
)
from hardware_state import ButtonState, HardwareState
from now import now

class EngineDriver:
    DEBUG_PRINT_TPS_COUNT = False
    DEBUG_PRINT_HW_STATE = True
    
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
            self._create_hardware_state_handler(name, create_debounce_generator(pin))
            for (name, pin) in button_name_to_hardware_button_pin.items()
        ]

        self.previous_internal_hardware_state = HardwareState.as_dict()
        self.internal_hardware_state_queue = []

        self.running = True

    def _create_hardware_state_handler(self, button_name, debounce_generator):
        def handle() -> tuple[str, ButtonState]:
            value = next(debounce_generator)
            button_state = ButtonState(value)
            return (button_name, button_state)

        return handle

    def update_internal_hardware_state(self):
        state = self._hardware_state_dict_from_prop()
        new_hardware_state = {
            k: v
            for k, v in state.items()
            if v.is_pressed != self.previous_internal_hardware_state[k].is_pressed
        }

        if len(new_hardware_state) > 0 and len(self.internal_hardware_state_queue) < 10:
            self.internal_hardware_state_queue.append(new_hardware_state)
            self.previous_internal_hardware_state.update(new_hardware_state)

    def update_engine_hardware_state(self):
        if len(self.internal_hardware_state_queue) > 0:
            Engine.update_hardware_state(self.internal_hardware_state_queue.pop(0))

    def _hardware_state_dict_from_prop(self) -> dict[str, ButtonState]:
        return dict([handle() for handle in self.button_handlers])

    def runloop(self):
        create_hardware_listener_thread(self)
        
        if EngineDriver.DEBUG_PRINT_HW_STATE:
            debug_print_hardware_state = handle_debug_print_hardware_state()

        if EngineDriver.DEBUG_PRINT_TPS_COUNT:
            ticks_since_last_stamp = 0
            last_stamp = now()
            
        while self.running:
            try:
                self.update_engine_hardware_state()
                
                if EngineDriver.DEBUG_PRINT_HW_STATE:
                    debug_print_hardware_state()

                Engine.tick()
                HardwareState.ack_button_states()
                
                if EngineDriver.DEBUG_PRINT_TPS_COUNT:
                    if now() - last_stamp > 1000:
                        print("ENGINE TPS:", ticks_since_last_stamp)
                        last_stamp = now()
                        ticks_since_last_stamp = 0
                    else:
                        ticks_since_last_stamp += 1

            except KeyboardInterrupt:
                self.running = False
            
            except BaseException as e:
                self.running = False
                print("exception: runloop")
                print(e)

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
