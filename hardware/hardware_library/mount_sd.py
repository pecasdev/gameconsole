# type: ignore
import os, sdcard
from machine import SPI, Pin
from engine import Engine


def mount_sd():
    try:
        spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
        cs = Pin(13)
        sd = sdcard.SDCard(spi, cs)
        os.mount(sd, "/sd")
    except Exception as e:
        print(e)
        Engine.screen.draw_text(10, 10, "SD CARD ERROR")
        Engine.screen.flush()

        import sys

        sys.exit()
