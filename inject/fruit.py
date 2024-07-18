from random import randrange
from engine import Object, Engine
from screen import Screen


class Fruit(Object):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.animation_frame = 0

    def draw_rotation_animation(self):
        draw_pixels = [1, 1, 1, 1]

        draw_pixels[self.animation_frame] = 0

        for x in range(2):
            for y in range(2):
                if draw_pixels.pop():
                    Engine.screen.draw_pixel(self.x + x, self.y + y)

    def step(self):
        self.draw_rotation_animation()
        if self.animation_frame == 3:
            self.animation_frame = 0
        else:
            self.animation_frame += 1


def spawn_fruit(snake):
    while True:
        [randx, randy] = [randrange(2, 99), randrange(2, 60)]
        [x, y] = [randx - randx % 2, randy - randy % 2]
        if [x, y] not in snake.tail:
            break
    Engine.create_object(Fruit(x, y))
