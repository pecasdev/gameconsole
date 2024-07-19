from engine import Object, Engine
from .score import Score
from screen import Screen
from hardware_state import HardwareState
from .fruit import Fruit, spawn_fruit


class Velocity:
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]


class Snake(Object):
    thickness = 2
    tail: list[tuple[int, int]]

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.tail = [(x, y)]
        self.velocity = [0, 0]
        self.growth_left = 0
        self.is_dead = False

    def draw(self):
        for x, y in self.tail:
            Engine.screen.draw_rect(x, y, self.thickness, self.thickness)

    def handle_tail_growth(self):
        self.tail.insert(0, (self.x, self.y))

        if self.growth_left == 0:
            self.tail.pop(-1)
        else:
            self.growth_left -= 1

    def next_position(self):
        return [
            self.x + self.velocity[0] * self.thickness,
            self.y + self.velocity[1] * self.thickness,
        ]

    def handle_movement(self):
        if self.velocity != Velocity.RIGHT and HardwareState.LEFT.is_pressed:
            self.velocity = Velocity.LEFT

        if self.velocity != Velocity.LEFT and HardwareState.RIGHT.is_pressed:
            self.velocity = Velocity.RIGHT

        if self.velocity != Velocity.DOWN and HardwareState.UP.is_pressed:
            self.velocity = Velocity.UP

        if self.velocity != Velocity.UP and HardwareState.DOWN.is_pressed:
            self.velocity = Velocity.DOWN

        self.handle_collision()

        if not self.is_dead:
            [self.x, self.y] = self.next_position()
            self.handle_tail_growth()

    def handle_collision(self):
        # exit if not moving (start of game)
        if self.velocity == [0, 0]:
            return

        [next_x, next_y] = self.next_position()

        # border collision
        if next_x <= 1 or next_x >= 127 or next_y <= 1 or next_y >= 63:
            self.is_dead = True

        # self collision
        if (next_x, next_y) in self.tail[1:]:
            self.is_dead = True

    def handle_fruit_collection(self):
        fruits = filter(lambda x: isinstance(x, Fruit), Engine.objects)
        for fruit in fruits:
            if [self.x, self.y] == [fruit.x, fruit.y]:
                fruit.kill()
                self.growth_left += 1
                spawn_fruit(snake=self)
                Score.score += 1

    def step(self):
        if not self.is_dead:
            self.handle_movement()
            self.handle_fruit_collection()

        self.draw()
