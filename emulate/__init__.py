from typing import Callable
from engine import Engine
from .pygame_driver import PygameDriver
from .props.arrange_config import OLED, CASE
from .emulator import Emulator
from screen import Screen
from .pygame_screen_adaptor import PygameScreenAdaptor
from font import Font

def create_emulator(program_main):
    pygame_driver = PygameDriver()
    pygame_driver.init_driver(CASE["WIDTH"], CASE["HEIGHT"])

    engine_psa = PygameScreenAdaptor(OLED["WIDTH"], OLED["HEIGHT"], pygame_driver)
    Engine.set_screen(Screen(engine_psa))
    
    # import default fonts
    Font.import_font("library/font/default_fonts/small.font")
    
    # run injection setup
    program_main()
    
    # return emulator
    emulator = Emulator(engine_psa, pygame_driver)
    return emulator
