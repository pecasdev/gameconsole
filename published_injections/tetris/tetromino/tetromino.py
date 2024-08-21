from engine import Object, Engine
from hardware_state import HardwareState
from ..constants import TETROMINO_THICKNESS, STACK_ROW_COUNT
from util import create_debug_print_handler
from alarm import Alarm
from sprite import Sprite


# todo - remove cell and row if not being used by anyone
def shape_iterate(shape, cell_func):
    results = []
    t = TETROMINO_THICKNESS
    for y, row in enumerate(shape):
        cy = y * t
        for x, cell in enumerate(row):
            cx = x * t
            if cell == "X":
                results.append(cell_func(cx, cy, cell, row))
    return results


class Tetromino(Object):
    letter: str
    move_right_delay_initial = 15
    tile_sprite: Sprite

    def __init__(self, x, y, rotation_shapes, world):
        super().__init__(x, y)
        self.rotation_shapes = rotation_shapes
        self.rotation_index = 0
        self.shape = rotation_shapes[0]
        self.world = world

        self.debug_fits_results = create_debug_print_handler()
        self.debug_position = create_debug_print_handler()

        self.h_speed = 0
        self.v_speed = 0

        self.move_right_delay_counter = self.move_right_delay_initial

        self.already_held = False
        self.ready_to_merge = False

    def rotate(self):
        next_rotation_index = (self.rotation_index + 1) % 4
        next_shape = self.rotation_shapes[next_rotation_index]

        if not self.fits_when(shape=next_shape):
            return

        self.rotation_index = next_rotation_index
        self.shape = next_shape

    def fits_when(self, x=None, y=None, shape=None):
        if shape is None:
            shape = self.shape

        if x is None:
            x = self.x

        if y is None:
            y = self.y

        def fits(cx, cy):
            def not_passing_right_edge():
                return (x + cx) < 127

            def not_colliding_stack():
                return not self.world.stack.is_occupied_at(x + cx, y + cy)

            return not_passing_right_edge() and not_colliding_stack()

        results = shape_iterate(
            shape,
            lambda cx, cy, cell, row: fits(cx, cy),
        )
        return all(results)

    def does_cell_offset_fit(self, cell_h_offset=0, cell_v_offset=0):
        x = self.x + cell_h_offset * TETROMINO_THICKNESS
        y = self.y + cell_v_offset * TETROMINO_THICKNESS

        return self.fits_when(x, y)

    def clamp_vertical_movement(self):
        t = TETROMINO_THICKNESS
        max_h = max(shape_iterate(self.shape, lambda cx, cy, cell, row: cy)) + t

        self.y = max(self.y, 0)
        self.y = min(self.y, t * STACK_ROW_COUNT - max_h)

    def auto_move_right(self):
        if self.move_right_delay_counter <= 0:
            self.h_speed += 1
            self.move_right_delay_counter = self.move_right_delay_initial
            self.ready_to_merge = True
        else:
            self.ready_to_merge = False
            self.move_right_delay_counter -= 1

    def handle_movement(self):
        # don't check cell offset until we pass the border (todo - fix magic number)
        past_stack_border = self.x > 29

        # restrict speeds based on collision
        if past_stack_border and not self.does_cell_offset_fit(
            cell_v_offset=self.v_speed
        ):
            self.v_speed = 0

        # check merge potential
        if not self.does_cell_offset_fit(cell_h_offset=1) and self.ready_to_merge:
            self.world.merge_to_stack(self)
            return

        while (
            past_stack_border
            and self.h_speed > 0
            and not self.does_cell_offset_fit(cell_h_offset=self.h_speed)
        ):
            self.h_speed -= 1

        # apply speeds
        self.x += self.h_speed * TETROMINO_THICKNESS
        self.y += self.v_speed * TETROMINO_THICKNESS

        self.h_speed = 0
        self.v_speed = 0

        self.clamp_vertical_movement()

    def draw(self):
        # todo - replace with shape_iterate
        t = TETROMINO_THICKNESS
        for y, row in enumerate(self.shape):
            cy = y * t
            for x, cell in enumerate(row):
                cx = x * t
                if cell == "X":
                    Tetromino.tile_sprite.blit(self.x + cx, self.y + cy)
                    # Engine.screen.draw_rect(self.x + cx, self.y + cy, t, t)

    def handle_inputs(self):
        if HardwareState.ALPHA.just_pressed():
            self.rotate()

        if not self.already_held and HardwareState.BETA.just_pressed():
            self.world.hold_piece(self)

        if HardwareState.RIGHT.is_pressed:
            self.move_right_delay_counter -= 7

        self.v_speed += (
            HardwareState.DOWN.just_pressed() - HardwareState.UP.just_pressed()
        )

    def step(self):
        if not self.world.game_over:
            self.handle_inputs()
            self.auto_move_right()
            self.handle_movement()
        self.draw()
