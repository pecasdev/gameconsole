# every X columns cleared, raises the level
# spawns new tetrominos
# allows player to hold a piece or swap out a held piece
# title screen: explain rules and buttons
from random import randrange

from hardware_state import HardwareState
from util import create_debug_print_handler
from engine import Engine, Object
from .tetromino import random_tetromino, known_tetrominos
from .tetromino.tetromino import Tetromino, TETROMINO_THICKNESS, shape_iterate
from sprite import Sprite
from .stack import Stack, STACK_ROW_COUNT
from .hud import Hud


class World(Object):
    def __init__(self) -> None:
        super().__init__(0, 0)
        self.stack: Stack = Engine.create_object(Stack(28, 0))  # type: ignore
        self.hud: Hud = Engine.create_object(Hud(self))  # type: ignore

        self.debug_print = create_debug_print_handler()

        self.held_tetromino_letter: str | None = None
        self.next_tetromino_letter = random_tetromino().letter
        self.hud.set_next_tetromino(self.next_tetromino_letter)
        self.create_next_tetromino()

        self.game_over = False
        self.is_title_screen = True
        
        tetrimino_tile = Sprite.load_from_file("tetromino_tile.sprite")
        tetrimino_tile.load()
        Tetromino.tile_sprite = tetrimino_tile
    
    @staticmethod
    def restart():
        Engine.reset()
        Engine.set_tick_cap(15)
        Engine.create_object(World())

    def create_tetromino(self, x, y, letter):
        self.active_tetromino: Tetromino = Engine.create_object(
            known_tetrominos[letter](x, y, self)
        )  # type:ignore

    def create_next_tetromino(self):
        if self.hud.next_tetromino is not None:
            x = self.hud.next_tetromino.x
            y = self.hud.next_tetromino.y
            self.create_tetromino(x, y, self.next_tetromino_letter)

            self.next_tetromino_letter: str = random_tetromino().letter
            self.hud.set_next_tetromino(self.next_tetromino_letter)
            self.hud.recently_created_position = "next"

    def create_held_tetromino(self):
        if self.hud.held_tetromino is not None:
            x = self.hud.held_tetromino.x
            y = self.hud.held_tetromino.y
            self.create_tetromino(x, y, self.held_tetromino_letter)
            self.hud.recently_created_position = "held"

    @staticmethod
    def score_for_columns_cleared(columns_cleared) -> int:
        if columns_cleared == 0:
            return 0
        if columns_cleared == 1:
            return 1000
        if columns_cleared == 2:
            return 2500
        if columns_cleared == 3:
            return 4000
        if columns_cleared == 4:
            return 5500
        return 0

    def set_level(self, current_score):
        self.level = current_score // 5000
        Tetromino.move_right_delay_initial = max(0, (15 - self.level))
        self.hud.level = self.level

    def merge_to_stack(self, tetromino: Tetromino):
        if tetromino.x < 29:
            self.game_over = True
            return

        def merge(cx, cy, cell, row):
            self.stack.set_occupied(tetromino.x + cx, tetromino.y + cy)

        shape_iterate(tetromino.shape, merge)
        tetromino.kill()
        columns_cleared = self.stack.clear_full_columns()
        self.hud.score += World.score_for_columns_cleared(columns_cleared)
        self.set_level(self.hud.score)
        self.create_next_tetromino()

    def hold_piece(self, tetromino: Tetromino):
        tetromino.kill()

        if self.held_tetromino_letter is not None:
            self.create_held_tetromino()
        else:
            self.create_next_tetromino()

        self.active_tetromino.already_held = True

        self.held_tetromino_letter = tetromino.letter
        self.hud.set_held_tetromino(self.held_tetromino_letter)

    def step(self):
        if self.stack.is_far_left_occupied():
            self.game_over = True
            # todo - add death logic
        
        if self.game_over and HardwareState.ALPHA.just_pressed():
            World.restart()
        
        if self.is_title_screen and self.active_tetromino.x > 27:
            self.is_title_screen = False
