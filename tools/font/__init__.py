import os
from PIL import Image

from font.font import Font
import font.persist


def parse_file(current_dir: str, filename: str):
    [char_w, char_h] = font.persist.character_dimensions_from_filename(
        f"{current_dir}/{filename}"
    )
    image = Image.open(f"{current_dir}/{filename}").convert("RGB")

    def parse_character_bitmap(x: int, y: int):
        bitmap = []
        for seek in range(char_w * char_h):
            pixel = image.getpixel((x + (seek % char_w), y + (seek // char_w)))
            bitmap.append(pixel == (0, 0, 0))
        return bitmap

    charmap = {}
    for seek in range(6 * 6):
        character = Font.available_characters[seek]
        bitmap = parse_character_bitmap(
            seek % 6 * (char_w + 1), seek // 6 * (char_h + 1)
        )
        charmap[character] = bitmap

    image.close()
    Font(char_w, char_h, charmap).dump_to_font_file(f"{current_dir}/output")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(f"{current_dir}/input"):
        parse_file(current_dir, f"input/{filename}")
