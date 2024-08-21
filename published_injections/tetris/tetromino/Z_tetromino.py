from .tetromino import Tetromino


class Z_Tetromino(Tetromino):
    letter = "Z"
    rotation_shapes = [
        ["XX ", " XX"],
        [" X", "XX", "X "],
        ["XX ", " XX"],
        [" X", "XX", "X "],
    ]

    def __init__(self, x, y, world):
        super().__init__(x, y, Z_Tetromino.rotation_shapes, world)
