from pygame_driver import PygameDriver
from props.arrange_config import OLED, CASE
from emulator import Emulator
from inject.main import main
from screen import Screen
from pygame_screen_adaptor import PygameScreenAdaptor

pygame_driver = PygameDriver()
pygame_driver.init_driver(CASE["WIDTH"], CASE["HEIGHT"])

engine_psa = PygameScreenAdaptor(OLED["WIDTH"], OLED["HEIGHT"], pygame_driver)
engine = main(Screen(engine_psa))
emulator = Emulator(engine, engine_psa, pygame_driver)

emulator.runloop()
