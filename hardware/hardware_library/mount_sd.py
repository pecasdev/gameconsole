# type: ignore
import os, sdcard
from machine import SPI, Pin
from engine import Engine


def mount_sd():
    try:
        spi = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        sd = sdcard.SDCard(spi, Pin(5))
        os.mount(sd, "/sd")
    except Exception as e:
        print(e)
        Engine.screen.draw_text(10, 10, "SD CARD ERROR")
        Engine.screen.flush()

        import sys

        sys.exit()
