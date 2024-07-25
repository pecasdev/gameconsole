from random import randrange
from engine import Engine, Object
from hardware_state import HardwareState

from .fruit import Fruit
from .score import Score
from .snake import Snake, Velocity
from .border import Border


class World(Object):
    def __init__(self):
        self.reset_game(kill_previous=False)

        self.is_title_screen = True

    def reset_game(self, kill_previous: bool):
        if kill_previous:
            for fruit in Engine.objects_of_class(Fruit):
                fruit.kill()

            for obj in [self.score, self.border, self.snake]:
                obj.kill()

        self.score = Score(100, 10)
        self.border = Border()
        self.snake = Snake(11, 11, world=self)
        for obj in [self.score, self.border, self.snake]:
            Engine.create_object(obj)

        self.spawn_fruit(self.snake.x + self.snake.thickness * 5, self.snake.y)

    def __random_free_coordinates_within_border(self) -> tuple[int, int]:
        t = Border.thickness
        x_max = Border.width - t - Fruit.thickness
        y_max = Border.height - t - Fruit.thickness

        # not particularly effective but it does the trick and
        # i don't really want to implement a better algorithm
        while True:
            [randx, randy] = [randrange(0, x_max), randrange(0, y_max)]
            [x, y] = [t + randx - randx % 3, t + randy - randy % 3]
            if (x, y) not in self.snake.body:
                break

        return (x, y)

    def spawn_fruit(self, x_override: int | None = None, y_override: int | None = None):
        if x_override is None or y_override is None:
            [x, y] = self.__random_free_coordinates_within_border()
        else:
            [x, y] = [x_override, y_override]

        Engine.create_object(Fruit(x, y))

    def draw_title_screen(self):
        if self.snake.velocity != Velocity.NONE:
            self.is_title_screen = False

        Engine.screen.draw_text(10, 30, "SNAKE\nBY: PECAS")

    def draw_death_text(self):
        if HardwareState.ALPHA.just_pressed():
            self.reset_game(kill_previous=True)

        Engine.screen.draw_text(97, 40, "PRESS\nA TO\nRESET")

    def step(self):
        if self.is_title_screen:
            self.draw_title_screen()

        if self.snake.is_dead:
            self.draw_death_text()
