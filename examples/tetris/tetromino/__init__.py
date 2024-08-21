# there is only one tetromino on screen at a time, spawning from the far left
# the only player controlled object
# it moves to the right automatically and can be sped up or moved up/down
# pressing A rotates it, B to swap the held piece
# when the tetromino collides with the stack, it is transferred to the stack and a new tetromino spawns
# as world levels progress, pieces move faster
import random

from .I_tetromino import I_Tetromino
from .J_tetromino import J_Tetromino
from .L_tetromino import L_Tetromino
from .O_tetromino import O_Tetromino
from .S_tetromino import S_Tetromino
from .T_tetromino import T_Tetromino
from .Z_tetromino import Z_Tetromino

known_tetrominos = {
    "I": I_Tetromino,
    "J": J_Tetromino,
    "L": L_Tetromino,
    "O": O_Tetromino,
    "S": S_Tetromino,
    "T": T_Tetromino,
    "Z": Z_Tetromino,
}


def random_tetromino():
    return random.choice(list(known_tetrominos.values()))
