# stack represents the boundary of placed pieces
# a tetromino can be added to the stack
# once a full column appears, it is cleared and the columns to the left of it move to the right
# if stack reaches far left, game over

from engine import Object, Engine
from .tetromino.tetromino import Tetromino
from .constants import TETROMINO_THICKNESS

STACK_ROW_COUNT = 10
STACK_COL_COUNT = 20


class Row:
    def __init__(self):
        self.occupied = [0] * STACK_COL_COUNT

    def is_far_left_occupied(self):
        return self.occupied[0]

    def set_occupied(self, index):
        self.occupied[index] = 1

    def is_occupied_at(self, index):
        return self.occupied[index]


def to_row_col(x, y):
    x = max(x, 0)
    y = max(y, 0)
    return (y // TETROMINO_THICKNESS, x // TETROMINO_THICKNESS)


class Stack(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rows = [Row() for _ in range(STACK_COL_COUNT)]
        #self.debug_fill()

    def debug_fill(self):
        for col in range(16):
            for row in range(9):
                self.rows[row].set_occupied(19 - col)

    def set_occupied(self, x, y):
        (row, col) = to_row_col(x - self.x, y - self.y)
        self.rows[row].set_occupied(col)

    def is_occupied_at(self, x, y):
        (row, col) = to_row_col(x - self.x, y - self.y)
        return self.rows[row].is_occupied_at(col)

    def is_far_left_occupied(self):
        return any(row.is_far_left_occupied() for row in self.rows)

    def draw(self):
        t = TETROMINO_THICKNESS
        for y, row in enumerate(self.rows):
            for x, occupied in enumerate(row.occupied):
                if occupied:
                    Tetromino.tile_sprite.blit(self.x + x * t, self.y + y * t)
                    #Engine.screen.draw_rect(self.x + x * t, self.y + y * t, t, t)

    def clear_full_columns(self):
        col_indices_to_clear = []
        for col_index in range(STACK_COL_COUNT):
            if all(
                self.rows[row_index].occupied[col_index]
                for row_index in range(STACK_ROW_COUNT)
            ):
                col_indices_to_clear.append(col_index)

        for col_index in col_indices_to_clear:
            for row in self.rows:
                row.occupied.pop(col_index)
                row.occupied.insert(0, 0)

        return len(col_indices_to_clear)

    def step(self):
        self.draw()
