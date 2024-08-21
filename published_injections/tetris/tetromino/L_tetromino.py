from .tetromino import Tetromino


class L_Tetromino(Tetromino):
    letter = "L"
    rotation_shapes = [
        ["XXX", "X  "],
        ["X ", "X ", "XX"],
        ["  X", "XXX"],
        ["XX", " X", " X"],
    ]

    def __init__(self, x, y, world):
        super().__init__(x, y, L_Tetromino.rotation_shapes, world)
