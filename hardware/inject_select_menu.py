from engine import Engine
from font.font_small import font_small
from hardware_state import HardwareState
from engine_driver import EngineDriver
from engine import Object


class InjectSelectMenu(Object):
    def __init__(self, engine_driver) -> None:
        super().__init__(0, 0)
        self.choices = self.__read_from_sd_dir()
        self.selection_index = len(self.choices) // 2
        self.engine_driver = engine_driver

    def __read_from_sd_dir(self):
        choices = []
        f = open("/sd/gamelist")
        choices = [line.strip() for line in f.readlines() if len(line.strip()) != 0]
        print(choices)
        f.close()
        return choices

    choice_vision_range = 2

    def draw_choices(self):
        current_selection = self.choices[self.selection_index]

        # draw current selection
        font_small.draw_string(10, 30, "> " + current_selection)

        def draw_if_exists(x, y, choice_index):
            if choice_index < 0 or choice_index > len(self.choices) - 1:
                return

            font_small.draw_string(x, y, self.choices[choice_index])

        # draw choices around current selection
        for i in range(1, InjectSelectMenu.choice_vision_range + 1):
            draw_if_exists(10, 30 + i * 10, self.selection_index + i)
            draw_if_exists(10, 30 - i * 10, self.selection_index - i)

    def handle_inputs(self):
        if HardwareState.UP.just_pressed():
            self.selection_index -= 1

        if HardwareState.DOWN.just_pressed():
            self.selection_index += 1

        if self.selection_index == -1:
            self.selection_index = len(self.choices) - 1

        if self.selection_index == len(self.choices):
            self.selection_index = 0

        if HardwareState.ALPHA.just_pressed():
            self.engine_driver.running = False

    def selection(self):
        return self.choices[self.selection_index]

    def step(self):
        font_small.set_screen(Engine.screen)

        if len(self.choices) == 0:
            font_small.draw_string(10, 10, "NO GAMES FOUND")
            Engine.screen.flush()

            import sys

            sys.exit()

        self.handle_inputs()
        self.draw_choices()


def block_and_return_inject_selection():
    engine_driver = EngineDriver()

    # very cursed but it works i guess
    inject_select_menu = InjectSelectMenu(engine_driver)
    Engine.create_object(inject_select_menu)

    engine_driver.runloop()

    return inject_select_menu.selection()


# we have an sd card containing folders containing injections
# we mount the sd card and pass it to the inject select menu
# we grab the folder names in the sd card
# we use keyboard pressed to cycle an internal state buffer frame thing
# when user hits ALPHA, we return a filename to main, which then does the whole engine stuff
# we have some options
# if user presses select button (new button btw), kill yourself so that thonny works and stuff
