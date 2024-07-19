from screen_adaptor.screen_adaptor import ScreenAdaptor
import font


class Screen:
    def __init__(self, adaptor: ScreenAdaptor):
        self.adaptor = adaptor
        self.width = adaptor.width
        self.height = adaptor.height

    def clear(self):
        self.adaptor.clear()

    def flush(self):
        self.adaptor.flush()

    # todo - add limitations on pixel position depending on width/height
    def draw_pixel(self, x: int, y: int):
        self.adaptor.draw_pixel(x, y)

    def draw_rect(self, left: int, top: int, width: int, height: int):
        for w in range(width):
            for h in range(height):
                self.draw_pixel(left + w, top + h)

    def draw_text(self, x: int, y: int, text: str):
        self.adaptor.draw_text(x, y, text, font.Font.current_font())

    def kill(self):
        self.adaptor.kill()
