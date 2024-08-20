from typing import Callable

from engine import Engine
from font import Font
from screen import Screen

from .emulator import Emulator
from .props.arrange_config import CASE, OLED
from .pygame_driver import PygameDriver
from .pygame_screen_adaptor import PygameScreenAdaptor


def create_emulator(program_main):
    pygame_driver = PygameDriver()
    pygame_driver.init_driver(CASE["WIDTH"], CASE["HEIGHT"])

    engine_psa = PygameScreenAdaptor(OLED["WIDTH"], OLED["HEIGHT"], pygame_driver)
    Engine.set_screen(Screen(engine_psa))

    # import default fonts
    Font.import_font("library/font/default_fonts/small.font")
    Font.set_current_font("small")

    # run injection setup
    program_main()

    # return emulator
    emulator = Emulator(engine_psa, pygame_driver)
    return emulator
