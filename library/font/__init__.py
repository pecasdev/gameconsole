from engine import Engine
import font.persist as font_persist
from sprite import Sprite


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
        try:
            current_font = next(filter(lambda f: f.name == name, Font.known_fonts))
        except:
            raise RuntimeError(f"Font {name} is not known")

        Font.font_selection_index = Font.known_fonts.index(current_font)

    @staticmethod
    def current_font():
        return Font.known_fonts[Font.font_selection_index]

    @staticmethod
    def import_font(filename: str):
        font = font_persist.load(filename)
        Font.known_fonts.append(font)

    def __init__(self, name: str, character_sprites: dict[str, Sprite]):
        self.name = name
        self.character_sprites = character_sprites
        self.char_w = character_sprites["A"].width
        self.char_h = character_sprites["A"].height

    def draw_text(self, x: int, y: int, text: str):
        for index, char in enumerate(text):
            self.__draw_character(x + index * (self.char_w + 1), y, char)

    def __draw_character(self, x: int, y: int, character: str):
        if character == " ":
            return

        sprite = self.character_sprites[character.upper()]
        sprite.draw(x, y)
