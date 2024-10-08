# type: ignore

from machine import Pin
import time
from now import now


class HardwareButtonPin:
    # general purpose pins
    BETA = Pin(16, Pin.IN, Pin.PULL_DOWN)
    ALPHA = Pin(17, Pin.IN, Pin.PULL_DOWN)

    UP = Pin(18, Pin.IN, Pin.PULL_DOWN)
    RIGHT = Pin(19, Pin.IN, Pin.PULL_DOWN)
    DOWN = Pin(20, Pin.IN, Pin.PULL_DOWN)
    LEFT = Pin(21, Pin.IN, Pin.PULL_DOWN)


DEBOUNCE_POLL_COUNT = 1
DEBOUNCE_POLL_WAIT_MS = 5


def create_debounce_generator(pin: HardwareButtonPin):
    previous_value = False

    def generator():
        nonlocal previous_value

        while True:
            values = []
            for i in range(DEBOUNCE_POLL_COUNT):
                if i != 0:
                    time.sleep(DEBOUNCE_POLL_WAIT_MS / 1000)
                values.append(pin.value())

            new_value = (
                False
                if True not in values
                else (True if False not in values else previous_value)
            )

            yield new_value
            previous_value = new_value

    return generator()


def create_hardware_listener_thread(engine_driver):
    import _thread

    def hardware_loop(engine_driver):
        if engine_driver.DEBUG_PRINT_TPS_COUNT:
            ticks_since_last_stamp = 0
            last_stamp = now()
            
        while engine_driver.running:
            engine_driver.update_internal_hardware_state()
            
            if engine_driver.DEBUG_PRINT_TPS_COUNT:
                if now() - last_stamp > 1000:
                    print("HWL TPS:", ticks_since_last_stamp)
                    last_stamp = now()
                    ticks_since_last_stamp = 0
                else:
                    ticks_since_last_stamp += 1

    _thread.start_new_thread(hardware_loop, [engine_driver])
