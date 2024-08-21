from engine import Engine, Object
from font import Font


class Score(Object):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # score is just the size of your snake, you start at size=1
        self.score = 1

    def step(self):
        Font.set_current_font("small")

        Engine.screen.draw_text(self.x, self.y, "SIZE")
        Engine.screen.draw_text(self.x, self.y + 10, str(self.score))
