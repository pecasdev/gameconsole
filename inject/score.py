from engine import Object, Engine
from screen import Screen
from font.font_small import font_small


class Score(Object):
    score = 0

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def step(self):
        font_small.set_screen(Engine.screen)

        font_small.draw_string(self.x, self.y, str(Score.score))
