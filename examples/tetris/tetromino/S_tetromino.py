from .tetromino import Tetromino


class S_Tetromino(Tetromino):
    letter = "S"
    rotation_shapes = [
        [" XX", "XX "],
        ["X ", "XX", " X"],
        [" XX", "XX "],
        ["X ", "XX", " X"],
    ]

    def __init__(self, x, y, world):
        super().__init__(x, y, S_Tetromino.rotation_shapes, world)
