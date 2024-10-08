import json
import font
import sprite


def load(filename: str):
    with open(filename) as f:
        from_dump = json.load(f)

    char_w = from_dump["char_w"]
    char_h = from_dump["char_h"]

    character_sprites = {
        k: sprite.Sprite(char_w, char_h, bitmap)
        for k, bitmap in from_dump["character_bitmaps"].items()
    }

    return font.Font(from_dump["name"], character_sprites)


def dump(font: "font.Font", dirname: str):
    without_width_and_height = {
        k: v.to_dict()["bitmap"] for k, v in font.character_sprites.items()
    }

    to_dump = {
        "name": font.name,
        "char_w": font.char_w,
        "char_h": font.char_h,
        "character_bitmaps": without_width_and_height,
    }

    with open(f"{dirname}/{font.name}.font", "w") as f:
        json.dump(to_dump, f)
