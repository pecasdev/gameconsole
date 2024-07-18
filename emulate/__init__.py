from typing import Callable
from engine import Engine
from .pygame_driver import PygameDriver
from .props.arrange_config import OLED, CASE
from .emulator import Emulator
from screen import Screen
from .pygame_screen_adaptor import PygameScreenAdaptor


def create_emulator(program_main):
    pygame_driver = PygameDriver()
    pygame_driver.init_driver(CASE["WIDTH"], CASE["HEIGHT"])

    engine_psa = PygameScreenAdaptor(OLED["WIDTH"], OLED["HEIGHT"], pygame_driver)
    Engine.set_screen(Screen(engine_psa))
    program_main()
    emulator = Emulator(engine_psa, pygame_driver)
    return emulator
