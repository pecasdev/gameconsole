from engine import Object, Engine
from font import Font


class Score(Object):
    score = 0

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def step(self):
        Font.set_current_font("small")

        Engine.screen.draw_text(self.x, self.y, str(Score.score))
