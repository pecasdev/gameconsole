# type: ignore
from screen_adaptor import ScreenAdaptor
from hardware_frame_buffer_adaptor import HardwareFrameBufferAdaptor


class OledScreenAdaptor(ScreenAdaptor):
    width = 128
    height = 64

    def __init__(self, ssd1306_driver):
        super().__init__(128, 64)
        self.driver = ssd1306_driver

    def draw_pixel(self, x: int, y: int):
        self.driver.pixel(x, y, 1)
    
    def clear_pixel(self, x:int, y:int):
        self.driver.pixel(x, y, 0)

    def clear(self):
        self.driver.fill(0)

    def fill(self):
        self.driver.fill(1)

    def new_frame_buffer(self, width: int, height: int) -> HardwareFrameBufferAdaptor:
        return HardwareFrameBufferAdaptor(width, height, self)

    def blit(self, x: int, y: int, frame_buffer: HardwareFrameBufferAdaptor):
        self.driver.blit(frame_buffer.buffer, x, y, 0)

    def flush(self):
        self.driver.show()

    def kill(self):
        self.driver.poweroff()
