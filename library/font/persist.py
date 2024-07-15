import json


def character_dimensions_from_filename(filename: str) -> tuple[int, int]:
    # possibly sus we are using the filename to store information
    start = filename.rfind("_") + 1
    end = filename.find(".png")
    dimensions = [int(num) for num in filename[start:end].split("x")]
    return (dimensions[0], dimensions[1])


def load(filename: str):
    file = open(filename)
    charmap = json.load(file)
    [char_w, char_h] = character_dimensions_from_filename(filename)
    file.close()
    return (char_w, char_h, charmap)


def dump(font, dirname: str):
    with open(f"{dirname}/font_dump_{font.char_w}x{font.char_h}.font", "w") as f:
        json.dump(font.charmap, f)
