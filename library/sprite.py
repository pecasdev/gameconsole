from engine import Engine
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

    def draw(self, x, y):
        for seek in range(self.width * self.height):
            if self.bitmap[seek] == "1":
                draw_x = x + seek % self.width
                draw_y = y + seek // self.width

                Engine.screen.draw_pixel(draw_x, draw_y)
