# type: ignore
import sys
sys.path.insert(0, "library")

from machine import Pin, I2C, SPI
import ssd1306
from screen import Screen
from inject.main import main
from engine_driver import EngineDriver
from oled_screen_adaptor import OledScreenAdaptor

"""
# todo - sd card stuff
spi = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
sd = sdcard.SDCard(spi, Pin(5))

os.mount(sd, "/sd")

with open("/sd/test.txt") as f:
    content = f.read()

"""


# display stuff
ssd1306_driver = ssd1306.SSD1306_I2C(128, 64, I2C(1, scl=Pin(3), sda=Pin(2)))
screen_adaptor = OledScreenAdaptor(ssd1306_driver)
engine = main(Screen(screen_adaptor))

engine_driver = EngineDriver(engine)
engine_driver.runloop()
