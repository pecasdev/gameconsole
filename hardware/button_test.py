# type: ignore
from hardware_button_driver import create_debounce_handler, HardwarePin

beta_debounce = create_debounce_handler(HardwarePin.BETA)

prev_was_pressed = False
press_count = 0
while True:
    is_pressed = next(beta_debounce)

    if not prev_was_pressed and is_pressed:
        press_count += 1
        print("Presses:", press_count)

    prev_was_pressed = is_pressed
