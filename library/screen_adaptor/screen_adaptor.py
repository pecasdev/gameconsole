class ScreenAdaptor:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw_pixel(self, x: int, y: int):
        raise NotImplementedError

    def draw_text(self, x: int, y: int, text: str, font):
        font.draw_text(x, y, text)

    def clear(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def kill(self):
        raise NotImplementedError
