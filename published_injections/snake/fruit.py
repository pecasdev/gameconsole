from engine import Engine, Object


class Fruit(Object):
    thickness = 3

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.animation_frame = 0
        self.pixels_to_remove_by_frame = [0, 1, 2, 5, 8, 7, 6, 3]

    # some kind of rotating donut animation idk lol
    def draw_rotation_animation(self):
        draw_pixels = [1, 1, 1, 1, 0, 1, 1, 1, 1]

        draw_pixels[self.pixels_to_remove_by_frame[self.animation_frame]] = 0

        for y in range(3):
            for x in range(3):
                if draw_pixels.pop():
                    Engine.screen.draw_pixel(self.x + x, self.y + y)

    def step(self):
        self.draw_rotation_animation()
        if self.animation_frame == 7:
            self.animation_frame = 0
        else:
            self.animation_frame += 1
