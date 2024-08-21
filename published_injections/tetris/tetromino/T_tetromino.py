from .tetromino import Tetromino


class T_Tetromino(Tetromino):
    letter = "T"
    rotation_shapes = [
        ["XXX", " X "],
        [" X", "XX", " X"],
        [" X ", "XXX"],
        ["X ", "XX", "X "],
    ]

    def __init__(self, x, y, world):
        super().__init__(x, y, T_Tetromino.rotation_shapes, world)
