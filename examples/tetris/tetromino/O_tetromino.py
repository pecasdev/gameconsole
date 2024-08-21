from .tetromino import Tetromino


class O_Tetromino(Tetromino):
    letter = "O"
    rotation_shapes = [["XX", "XX"], ["XX", "XX"], ["XX", "XX"], ["XX", "XX"]]

    def __init__(self, x, y, world):
        super().__init__(x, y, O_Tetromino.rotation_shapes, world)
