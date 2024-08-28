# type: ignore
import sys

sys.path.insert(0, "library")
sys.path.insert(0, "hardware_library")

from machine import Pin, I2C
import ssd1306
from screen import Screen

from engine_driver import EngineDriver
from oled_screen_adaptor import OledScreenAdaptor
from engine import Engine
from mount_sd import mount_sd
from inject_select_menu import block_and_return_inject_selection
from copy_injection_from_sd import copy_injection_from_sd
from font.font_manager import FontManager
from now import now
from loadscreen import draw_loadscreen



ssd1306_driver = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(3), sda=Pin(2)))
screen_adaptor = OledScreenAdaptor(ssd1306_driver)
screen = Screen(screen_adaptor)
Engine.set_screen(screen)

mount_sd()

# import default fonts
FontManager.import_font("library/font/default_fonts/small.font")
FontManager.import_font("library/font/default_fonts/medium.font")
FontManager.import_font("library/font/default_fonts/large.font")
FontManager.set_current_font("small")


[inject_selection, inject_filecount] = block_and_return_inject_selection(ssd1306_driver)
copy_injection_from_sd(inject_selection, inject_filecount)

# run injection setup
from inject import main

try:
    draw_loadscreen(inject_selection)
    print("RUNNING INJECTION SETUP")
    main()
    print("DONE SETTING UP")
except BaseException as e:
    print("exception: injection setup")
    print(e)

engine_driver = EngineDriver()
engine_driver.runloop()
