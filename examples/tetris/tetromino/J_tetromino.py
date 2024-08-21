from .tetromino import Tetromino


class J_Tetromino(Tetromino):
    letter = "J"
    rotation_shapes = [
        ["XXX", "  X"],
        ["XX", "X ", "X "],
        ["X  ", "XXX"],
        [" X", " X", "XX"],
    ]

    def __init__(self, x, y, world):
        super().__init__(x, y, J_Tetromino.rotation_shapes, world)
