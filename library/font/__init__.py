from engine import Engine
import font.persist as font_persist


class Font:
    known_fonts = []
    font_selection_index: int = 0

    available_characters = (
        [chr(ord("A") + i) for i in range(26)]
        + [str(i) for i in range(10)]
        + [c for c in "><!?:*"]
    )

    @staticmethod
    def set_current_font(name: str):
        current_font = next(filter(lambda f: f.name == name, Font.known_fonts))
        Font.font_selection_index = Font.known_fonts.index(current_font)

    @staticmethod
    def current_font():
        return Font.known_fonts[Font.font_selection_index]

    @staticmethod
    def import_font(filename: str):
        font = font_persist.load(filename)
        Font.known_fonts.append(font)

    def __init__(self, name: str, char_w: int, char_h: int, charmap: dict[str, str]):
        self.name = name
        self.charmap = charmap
        self.char_w = char_w
        self.char_h = char_h

    def draw_text(self, x: int, y: int, text: str):
        for index, char in enumerate(text):
            self.__draw_character(x + index * (self.char_w + 1), y, char)

    def __draw_character(self, x: int, y: int, character: str):
        if Engine.screen is None:
            raise RuntimeError("Screen is None, did you run Font.set_screen?")

        if character == " ":
            return

        bitmap = self.charmap[character.upper()]

        for seek in range(self.char_w * self.char_h):
            if bitmap[seek] == "1":
                Engine.screen.draw_pixel(
                    x + seek % self.char_w, y + seek // self.char_w
                )
