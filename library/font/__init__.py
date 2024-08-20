import font.persist as font_persist

class Font:
    known_fonts = []
    font_selection_index: int = 0

    available_characters = (
        [chr(ord("A") + i) for i in range(26)]
        + [str(i) for i in range(10)]
        + [c for c in "><!?:-"]
    )

    @staticmethod
    def set_current_font(name: str):
        try:
            current_font = next(filter(lambda f: f.name == name, Font.known_fonts))
            current_font.load()
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

    def __init__(self, name: str, character_sprites):
        self.name = name
        self.character_sprites = character_sprites
        self.char_w = character_sprites["A"].width
        self.char_h = character_sprites["A"].height

    def load(self):
        for sprite in self.character_sprites.values():
            sprite.load()
        
    def draw_text(self, x: int, y: int, text: str):
        lines = text.split("\n")
        for y_offset, line in enumerate(lines):
            for x_offset, char in enumerate(line):
                self.__draw_character(
                    x + x_offset * (self.char_w + 1),
                    y + y_offset * (self.char_h + 2),
                    char,
                )

    def __draw_character(self, x: int, y: int, character: str):
        if character == " ":
            return

        upper_character = character.upper()
        if upper_character not in self.character_sprites:
            raise RuntimeError(f"Font has not been defined for '{upper_character}'")

        sprite = self.character_sprites[character.upper()]
        sprite.blit(x, y)
