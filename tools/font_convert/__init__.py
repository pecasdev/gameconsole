import os
from PIL import Image

import font
import font.persist as font_persist
from sprite import Sprite
from sprite_convert import filename_without_extension, parse_image_to_sprite

def character_dimensions_from_filename(filename: str) -> tuple[int, int]:
    # possibly sus we are using the filename to store information
    start = filename.rfind("_") + 1
    end = filename.find(".png")
    dimensions = [int(num) for num in filename[start:end].split("x")]
    return (dimensions[0], dimensions[1])


def parse_file(current_dir: str, filename: str):
    input_dir = f"{current_dir}/input"
    output_dir = f"{current_dir}/output"
    
    [char_w, char_h] = character_dimensions_from_filename(f"{input_dir}/{filename}")
    image = Image.open(f"{input_dir}/{filename}").convert("RGB")

    charmap: dict[str, Sprite] = {}
    for seek in range(len(font.Font.available_characters)):
        character = font.Font.available_characters[seek]
        sprite = parse_image_to_sprite(
            image, seek % 6 * (char_w + 1), seek // 6 * (char_h + 1), char_w, char_h
        )
        charmap[character] = sprite

    image.close()
    
    font_name = filename_without_extension(filename)
    font_persist.dump(font.Font(font_name, charmap), output_dir)


def font_convert():
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(f"{current_dir}/input"):
        parse_file(current_dir, filename)
