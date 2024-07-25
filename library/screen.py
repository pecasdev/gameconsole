from frame_buffer_adaptor import FrameBufferAdaptor
import screen_adaptor
import font


# frame buffer adaptor is packaged inside screenadaptor


class Screen:
    def __init__(self, screen_adaptor: screen_adaptor.ScreenAdaptor):
        self.screen_adaptor = screen_adaptor
        self.width = screen_adaptor.width
        self.height = screen_adaptor.height

    def clear(self):
        self.screen_adaptor.clear()

    def fill(self):
        self.screen_adaptor.fill()

    def flush(self):
        self.screen_adaptor.flush()

    def new_frame_buffer(self, width, height) -> FrameBufferAdaptor:
        return self.screen_adaptor.new_frame_buffer(width, height)

    def blit(self, x: int, y: int, frame_buffer_adaptor: FrameBufferAdaptor):
        self.screen_adaptor.blit(x, y, frame_buffer_adaptor)

    # todo - add limitations on pixel position depending on width/height
    def draw_pixel(self, x: int, y: int):
        self.screen_adaptor.draw_pixel(x, y)

    def draw_rect(self, left: int, top: int, width: int, height: int):
        for w in range(width):
            for h in range(height):
                self.draw_pixel(left + w, top + h)

    def draw_text(self, x: int, y: int, text: str):
        self.screen_adaptor.draw_text(x, y, text, font.Font.current_font())

    def kill(self):
        self.screen_adaptor.kill()
