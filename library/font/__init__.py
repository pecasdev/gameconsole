import sprite


# todo - add 2 more fonts: medium and big
class Font:
    available_characters = (
        [chr(ord("A") + i) for i in range(26)]
        + [str(i) for i in range(10)]
        + [c for c in "><!?:-"]
        + [c for c in "()%+=#"]
    )

    def __init__(self, name: str, character_sprites: dict[str, "sprite.Sprite"]):
        self.name = name
        self.character_sprites = character_sprites
        self.char_w = character_sprites["A"].width
        self.char_h = character_sprites["A"].height

    def _load(self):
        for sprite in self.character_sprites.values():
            sprite.load()

    def _draw_text(self, x: int, y: int, text: str):
        lines = text.split("\n")
        for y_offset, line in enumerate(lines):
            for x_offset, char in enumerate(line):
                self._draw_character(
                    x + x_offset * (self.char_w + 1),
                    y + y_offset * (self.char_h + 2),
                    char,
                )

    def _draw_character(self, x: int, y: int, character: str):
        if character == " ":
            return

        upper_character = character.upper()
        if upper_character not in self.character_sprites:
            raise RuntimeError(f"Font has not been defined for '{upper_character}'")

        sprite = self.character_sprites[character.upper()]
        sprite.blit(x, y)
