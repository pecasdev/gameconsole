from engine import Engine, Object
from hardware_state import ButtonState, HardwareState

from .border import Border
from .fruit import Fruit


class Velocity:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    NONE = (0, 0)


velocity_opposites: dict[tuple[int, int], tuple[int, int]] = {
    Velocity.LEFT: Velocity.RIGHT,
    Velocity.RIGHT: Velocity.LEFT,
    Velocity.DOWN: Velocity.UP,
    Velocity.UP: Velocity.DOWN,
}


def button_to_velocity() -> dict[ButtonState, tuple[int, int]]:
    return {
        HardwareState.LEFT: Velocity.LEFT,
        HardwareState.RIGHT: Velocity.RIGHT,
        HardwareState.UP: Velocity.UP,
        HardwareState.DOWN: Velocity.DOWN,
    }


class Snake(Object):
    thickness = 3

    def __init__(self, x: int, y: int, world):
        super().__init__(x, y)
        self.world = world
        self.body = [(x, y)]

        self.actual_velocity = Velocity.NONE
        self.proposed_velocity_buffer = []

        self.growth_left = 0
        self.is_dead = False

    def draw_body(self):
        for x, y in self.body:
            Engine.screen.draw_rect(x, y, self.thickness, self.thickness)

    def handle_growth(self):
        self.body.insert(0, (self.x, self.y))

        if self.growth_left == 0:
            self.body.pop(-1)
        else:
            self.growth_left -= 1

    def next_position(self):
        return [
            self.x + self.actual_velocity[0] * self.thickness,
            self.y + self.actual_velocity[1] * self.thickness,
        ]

    def update_velocity(self):
        while len(self.proposed_velocity_buffer) > 0:
            proposed_velocity = self.proposed_velocity_buffer.pop(0)

            # don't let player switch from left to right immediately (they would instantly die)
            if self.actual_velocity != velocity_opposites[proposed_velocity]:
                self.actual_velocity = proposed_velocity
                return

    def handle_movement(self):
        self.update_velocity()
        self.handle_collision()

        if not self.is_dead:
            [self.x, self.y] = self.next_position()
            self.handle_growth()

    def handle_collision(self):
        # don't check for collisions if not moving (start of game)
        if self.actual_velocity == Velocity.NONE:
            return

        [next_x, next_y] = self.next_position()

        # border collision
        t = Border.thickness
        if (
            next_x < t
            or next_y < t
            or next_x > t + Border.width - Snake.thickness
            or next_y > t + Border.height - Snake.thickness
        ):
            self.is_dead = True

        # self collision
        if (next_x, next_y) in self.body:
            self.is_dead = True

    def handle_fruit_collection(self):
        for fruit in Engine.objects_of_class(Fruit):
            if [self.x, self.y] == [fruit.x, fruit.y]:
                fruit.kill()
                self.growth_left += 1
                self.world.spawn_fruit()
                self.world.score.score += 1

    def handle_proposed_movement(self):
        pressed_this_tick = []
        for button, new_velocity in button_to_velocity().items():
            if button.just_pressed():
                pressed_this_tick.append((button, new_velocity))

        pressed_this_tick.sort(key=lambda pair: pair[0].event_timestamp)
        time_sorted_velocities = map(lambda pair: pair[1], pressed_this_tick)

        self.proposed_velocity_buffer.extend(time_sorted_velocities)
        self.proposed_velocity_buffer = self.proposed_velocity_buffer[:3]  # :3

    def step(self):
        if not self.is_dead:
            self.handle_proposed_movement()
            self.handle_movement()
            self.handle_fruit_collection()

        self.draw_body()
