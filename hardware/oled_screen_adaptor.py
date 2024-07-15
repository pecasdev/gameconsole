# type: ignore
from screen_adaptor.screen_adaptor import ScreenAdaptor


class OledScreenAdaptor(ScreenAdaptor):
    width = 128
    height = 64

    def __init__(self, ssd1306_driver):
        super().__init__(128, 64)
        self.driver = ssd1306_driver

    def draw_pixel(self, x: int, y: int):
        self.driver.pixel(x, y, 1)

    def clear(self):
        self.driver.fill(0)

    def flush(self):
        self.driver.show()

    def kill(self):
        self.driver.poweroff()
