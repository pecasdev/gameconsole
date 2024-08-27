import font
import font.persist as font_persist


class FontManager:
    known_fonts: list["font.Font"] = []
    font_selection_index: int = 0

    @staticmethod
    def set_current_font(name: str):
        try:
            current_font = next(
                filter(lambda f: f.name == name, FontManager.known_fonts)
            )
            current_font.__load()
        except:
            raise RuntimeError(f"Font {name} is not known")

        FontManager.font_selection_index = FontManager.known_fonts.index(current_font)

    @staticmethod
    def __get_current_font():
        return FontManager.known_fonts[FontManager.font_selection_index]

    @staticmethod
    def import_font(filename: str):
        font = font_persist.load(filename)
        FontManager.known_fonts.append(font)
