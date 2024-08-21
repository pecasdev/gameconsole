# it's basically just tetris but the blocks moves sideways
# playable area is entire width of screen and from the top to 50 pixels down (10 blocks per column)

# tetrominos have a thickness of 5, standard shapes as in the game
# collision detection with other tetrominos
# movement is up/down and to the right, automatic movement to the right every second
# when it touches a block or the boundary, block is frozen in place and next block spawns (if up/down is pressed, timer is reset)
# shit becomes faster, y'know?

from .tetromino import random_tetromino
from engine import Engine
from .world import World


def main():
    World.restart()


# -----------------------------------------------
# add debug printing system to objects (sidetrack)
# add counter system to objects (sidetrack)
# add functionality to adjust screen brightness