from .tetromino import Tetromino


class I_Tetromino(Tetromino):
    letter = "I"
    rotation_shapes = [["XXXX"], ["X", "X", "X", "X"], ["XXXX"], ["X", "X", "X", "X"]]

    def __init__(self, x, y, world):
        super().__init__(x, y, I_Tetromino.rotation_shapes, world)
