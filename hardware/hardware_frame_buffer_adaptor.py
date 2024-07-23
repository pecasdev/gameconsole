# type:ignore
from frame_buffer_adaptor import FrameBufferAdaptor
from screen_adaptor import ScreenAdaptor
import framebuf


class HardwareFrameBufferAdaptor(FrameBufferAdaptor):
    def __init__(self, width, height, screen_adaptor: ScreenAdaptor) -> None:
        super().__init__(width, height, screen_adaptor)
        self.buffer = framebuf.FrameBuffer(
            bytearray(width * height), width, height, framebuf.MONO_VLSB
        )
    
    def draw_pixel(self, x, y):
        self.buffer.pixel(x, y, 1)
