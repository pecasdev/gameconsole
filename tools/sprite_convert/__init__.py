import os
import sprite
from PIL import Image
import json


def parse_image_to_sprite(image, x, y, width, height):
    bitmap = ""
    for seek in range(width * height):
        pixel = image.getpixel((x + (seek % width), y + (seek // width)))
        bitmap += "1" if pixel == (255, 255, 255) else "0"
    return sprite.Sprite(width, height, bitmap)


def filename_without_extension(filename: str):
    index = filename.rfind(".")
    return filename[:index]


def parse_file(input_dir: str, output_dir: str, filename: str):
    image = Image.open(f"{input_dir}/{filename}").convert("RGB")
    sprite = parse_image_to_sprite(image, 0, 0, image.width, image.height)

    image.close()

    with open(f"{output_dir}/{filename_without_extension(filename)}.sprite", "w") as f:
        json.dump(sprite.to_dict(), f)


def sprite_convert():
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(f"{current_dir}/input"):
        parse_file(f"{current_dir}/input", f"{current_dir}/output", filename)
