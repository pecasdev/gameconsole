from engine import Object, Engine
from screen import Screen


class Border(Object):
    def __init__(self):
        super().__init__(0, 0)

    def __draw_border(self):
        # top/bottom
        for x in range(128):
            Engine.screen.draw_pixel(x, 0)
            Engine.screen.draw_pixel(x, 63)

        # left/divider/right
        for y in range(64):
            Engine.screen.draw_pixel(0, y)
            Engine.screen.draw_pixel(101, y)
            Engine.screen.draw_pixel(127, y)

    def step(self):
        self.__draw_border()
