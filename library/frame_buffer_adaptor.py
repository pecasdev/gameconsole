# this is only used for blitting sprites
from screen_adaptor import ScreenAdaptor


class FrameBufferAdaptor:
    def __init__(self, width, height, screen_adaptor: ScreenAdaptor) -> None:
        self.screen_adaptor = screen_adaptor
        self.width = width
        self.height = height

    def blit_to_screen(self, x: int, y: int):
        self.screen_adaptor.blit(x, y, self)

    def draw_pixel(self, x: int, y: int):
        raise NotImplementedError

    def load_bitmap(self, bitmap):
        lit_pixels = [seek for (seek, bit) in enumerate(bitmap) if bit == "1"]

        for seek in lit_pixels:
            x = seek % self.width
            y = seek // self.width

            self.draw_pixel(x, y)
