from engine import Object, Engine


class Border(Object):
    thickness = 2
    width = 90
    height = 60

    def __init__(self):
        super().__init__(0, 0)
        self.is_title_screen = True

    def draw(self):
        w = Border.width
        t = Border.thickness
        h = Border.height

        # top/bottom (don't overlap with left/right)
        Engine.screen.draw_rect(t, 0, t + w, t)
        Engine.screen.draw_rect(t, t + h, t + w, t)

        # left/right
        Engine.screen.draw_rect(0, 0, t, t + h + t)
        Engine.screen.draw_rect(t + w, 0, t, t + h + t)

    def step(self):
        self.draw()
