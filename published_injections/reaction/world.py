from engine import Object, Engine
from hardware_state import HardwareState
from .state import State
from .reaction_record import ReactionRecord



class World(Object):
    def __init__(self, ralph):
        super().__init__(0, 0)

        self.ralph = ralph
        self.state = State()
        self.reaction_record = ReactionRecord()
        self.score_history = []

        self.is_title_screen = True

    def draw_score_history(self):
        if len(self.score_history) > 0:
            Engine.screen.draw_rect(80, 0, 1, 64)

        for i, score in enumerate(self.score_history):
            if score == -1:
                text = "early"
            else:
                text = f"{score} ms"

            if i == 0:
                # draw first score a bit above the to-be horizontal line
                Engine.screen.draw_text(85, 5, text)
            else:
                if i == 1:
                    # draw horizontal line if second score exist
                    Engine.screen.draw_rect(80, 13, 84, 1)

                Engine.screen.draw_text(85, 10 + 10 * i, text)

    def process_new_score(self):
        score = self.reaction_record.pop_score()
        if score is not None:
            self.score_history.insert(0, score)

        if len(self.score_history) > 5:
            self.score_history.pop(-1)

    # record reaction end as early as possible
    def prestep(self):
        if HardwareState.ALPHA.just_pressed():
            self.state.handle_alpha_press()

            if self.state.reaction_too_early:
                self.state.reaction_too_early = False
                self.reaction_record.record_too_early()

            if self.state.ready_to_capture_end:
                self.state.ready_to_capture_end = False
                self.reaction_record.record_end()

    def draw_title_screen(self):
        if HardwareState.ALPHA.just_released():
            self.is_title_screen = False

        self.ralph.draw_sprite()

        Engine.screen.draw_text(70, 40, "REACTION")
        Engine.screen.draw_text(70, 50, "by: pecas")

    def step(self):
        if self.is_title_screen:
            self.draw_title_screen()
            return

        self.ralph.set_current_sprite_name_from_state(self.state.get_state())
        self.ralph.draw_sprite()

        self.process_new_score()
        self.draw_score_history()

    # record reaction start as late as possible
    def poststep(self):
        if self.state.ready_to_capture_start:
            self.state.ready_to_capture_start = False
            self.reaction_record.record_start()
