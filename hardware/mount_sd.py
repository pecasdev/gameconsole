# type: ignore
import os, sdcard
from font.font_small import font_small
from machine import SPI, Pin


def mount_sd(screen):
    try:
        spi = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        sd = sdcard.SDCard(spi, Pin(5))
        os.mount(sd, "/sd")
    except Exception as e:
        print(e)
        font_small.set_screen(screen)
        font_small.draw_string(10, 10, "SD CARD ERROR")
        screen.flush()

        import sys

        sys.exit()
