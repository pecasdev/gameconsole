# type: ignore

from machine import Pin
import time


class HardwareButtonPin:
    # general purpose pins

    LEFT = Pin(18, Pin.IN, Pin.PULL_DOWN)
    DOWN = Pin(19, Pin.IN, Pin.PULL_DOWN)
    RIGHT = Pin(20, Pin.IN, Pin.PULL_DOWN)
    UP = Pin(21, Pin.IN, Pin.PULL_DOWN)

    ALPHA = Pin(16, Pin.IN, Pin.PULL_DOWN)
    BETA = Pin(17, Pin.IN, Pin.PULL_DOWN)


DEBOUNCE_POLL_REPEAT = 1
DEBOUNCE_POLL_WAIT_MS = 5


def create_debounce_generator(pin: HardwareButtonPin, DEBUG_name: str):
    previous_value = False

    def generator():
        nonlocal previous_value

        DEBUG_prev_line = ""
        while True:
            values = []
            for i in range(DEBOUNCE_POLL_REPEAT):
                if i != 0:
                    time.sleep(DEBOUNCE_POLL_WAIT_MS / 1000)
                values.append(pin.value())

            new_value = (
                False
                if True not in values
                else (True if False not in values else previous_value)
            )

            DEBUG_line = f"{DEBUG_name}: {previous_value} {new_value} {str(values)}"
            if DEBUG_prev_line != DEBUG_line:
                print(DEBUG_line)
                DEBUG_prev_line = DEBUG_line

            yield new_value
            previous_value = new_value

    return generator()


def create_hardware_listener_thread(engine_driver):
    import _thread

    def hardware_loop(engine_driver):
        while engine_driver.running:
            engine_driver.update_internal_hardware_state()

    _thread.start_new_thread(hardware_loop, [engine_driver])
