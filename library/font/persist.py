import json
import font


def character_dimensions_from_filename(filename: str) -> tuple[int, int]:
    # possibly sus we are using the filename to store information
    start = filename.rfind("_") + 1
    end = filename.find(".png")
    dimensions = [int(num) for num in filename[start:end].split("x")]
    return (dimensions[0], dimensions[1])


def load(filename: str):
    with open(filename) as f:
        from_dump = json.load(f)

    return font.Font(
        from_dump["name"],
        from_dump["char_w"],
        from_dump["char_h"],
        from_dump["charmap"],
    )


def dump(font, dirname: str):
    to_dump = {
        "name": font.name,
        "char_w": font.char_w,
        "char_h": font.char_h,
        "charmap": font.charmap,
    }

    with open(f"{dirname}/dump_{font.char_w}x{font.char_h}.font", "w") as f:
        json.dump(to_dump, f)
