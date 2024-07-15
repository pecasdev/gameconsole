from screen import Screen
import font.persist


class Font:
    available_characters = [chr(ord("A") + i) for i in range(26)] + [
        str(i) for i in range(10)
    ]

    def __init__(self, char_w: int, char_h: int, charmap: dict[str, list[bool]]):
        self.charmap = charmap
        self.char_w = char_w
        self.char_h = char_h
        self.screen = None

    def set_screen(self, screen: Screen):
        self.screen = screen

    def draw_string(self, x: int, y: int, text: str):
        for index, char in enumerate(text):
            self.draw_character(x + index * (self.char_w + 1), y, char)

    def draw_character(self, x: int, y: int, character: str):
        if self.screen is None:
            raise RuntimeError("Screen is None, did you run Font.set_screen?")

        if character == " ":
            return

        bitmap = self.charmap[character.upper()]

        for seek in range(self.char_w * self.char_h):
            if bitmap[seek]:
                self.screen.draw_pixel(x + seek % self.char_w, y + seek // self.char_w)

    def dump_to_font_file(self, dirname: str):
        font.persist.dump(self, dirname)

    @staticmethod
    def from_font_file(filename: str):
        [char_w, char_h, charmap] = font.persist.load(filename)
        return Font(char_w, char_h, charmap)
