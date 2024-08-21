# displays next piece
# displays held piece
# displays score
# displays current level
from engine import Object, Engine
from .tetromino.tetromino import TETROMINO_THICKNESS, Tetromino
from .tetromino import known_tetrominos
from .stack import STACK_COL_COUNT, STACK_ROW_COUNT
from util import zfill

class Hud(Object):
    held_tetromino: Tetromino | None
    next_tetromino: Tetromino | None
    recently_created_position: str | None
    score: int

    def __init__(self, world):
        super().__init__(0, 0)
        self.held_tetromino = None
        self.next_tetromino = None
        self.world = world
        self.recently_created_position = None
        self.score = 0
        self.level = 0

    def set_held_tetromino(self, letter):
        x = self.world.stack.x - 5 * TETROMINO_THICKNESS
        y = self.world.stack.y + 1 * TETROMINO_THICKNESS
        self.held_tetromino = known_tetrominos[letter](x, y, None)

    def set_next_tetromino(self, letter):
        x = self.world.stack.x - 5 * TETROMINO_THICKNESS
        y = self.world.stack.y + 6 * TETROMINO_THICKNESS
        self.next_tetromino = known_tetrominos[letter](x, y, None)

    def step(self):
        self.draw()

    def draw(self):
        # (level + score) border
        stack_height = STACK_ROW_COUNT * TETROMINO_THICKNESS
        Engine.screen.draw_rect(0, stack_height, 128, 1)

        # stack border
        for y in range(0, stack_height, 2):
            Engine.screen.draw_pixel(27, y)

        if self.world.is_title_screen:
            Engine.screen.draw_text(60, 20, "TETRIS")
            Engine.screen.draw_text(55, 27, "BY:PECAS")
            Engine.screen.draw_text(3, stack_height + 5, "A TO SPIN  B TO HOLD")

        else:
            # level
            Engine.screen.draw_text(3, stack_height + 5, f"LVL:{zfill(self.level, 2)}")

            # score
            Engine.screen.draw_text(
                50, stack_height + 5, f"SCORE:{zfill(self.score, 7)}"
            )

        # dont draw next/held pieces if game is over (confusing)
        if self.world.game_over:
            Engine.screen.clear_rect(50, 18, 64, 16)
            Engine.screen.draw_text(55, 20, "GAME OVER")
            Engine.screen.draw_text(52, 27, "A TO RESET")
            return

        # held piece
        if self.held_tetromino is not None:
            recently_created = self.recently_created_position == "held"
            past_border = self.world.active_tetromino.x > 27
            if past_border or not recently_created:
                self.held_tetromino.draw()

            Engine.screen.draw_text(2, 17, "HELD")

        # next piece
        if self.next_tetromino is not None:
            recently_created = self.recently_created_position == "next"
            past_border = self.world.active_tetromino.x > 27
            if past_border or not recently_created:
                self.next_tetromino.draw()
            Engine.screen.draw_text(2, 42, "NEXT")
