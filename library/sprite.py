import engine
import json


class Sprite:
    @staticmethod
    def load_from_file(filename):
        with open(f"inject/{filename}") as f:
            from_dump = json.load(f)

        return Sprite(from_dump["width"], from_dump["height"], from_dump["bitmap"])

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "bitmap": self.bitmap,
        }

    def __init__(self, width: int, height: int, bitmap: str):
        self.bitmap = bitmap
        self.width = width
        self.height = height

    def load(self):
        self.__frame_buf = engine.Engine.screen.new_frame_buffer(
            self.width, self.height
        )
        self.__frame_buf.load_bitmap(self.bitmap)

    def blit(self, x, y):
        self.__frame_buf.blit_to_screen(x, y)
