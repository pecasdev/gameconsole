# type: ignore
from engine import Engine
from hardware_state import HardwareState
from engine_driver import EngineDriver
from engine import Object
from util import zfill


def _process_choice_line(rawline: str) -> tuple[str, int]:
    [injection_name, rawcount] = rawline.strip().split(" ")
    return (injection_name, int(rawcount))

class InjectSelectMenu(Object):
    version = 1
    rows_per_screen = 6

    def _read_from_sd_dir(self):
        # list of tuple: ("injection_name", "file_count")
        choices: list[tuple[str, int]] = []
        f = open("/sd/gamelist")
        choices = [
            _process_choice_line(line)
            for line in f.readlines()
            if len(line.strip()) != 0
        ]
        print(choices)
        f.close()
        return choices



    def __init__(self, engine_driver, ssd1306_driver) -> None:
        super().__init__(0, 0)
        self.choices = self._read_from_sd_dir()
        self.choice_count = len(self.choices)
        self.selection_index = 0
        self.engine_driver = engine_driver

        self.ssd1306_driver = ssd1306_driver
        self.brightness = 3

    def draw(self):
        self.draw_choices()
        self.draw_choice_count()
        self.draw_version()
        self.draw_battery()
        self.draw_brightness_bar()
        self.draw_help_text()

    def draw_help_text(self):
        Engine.screen.draw_text(40, 55, "A:PLAY B:LIGHT")

    def draw_battery(self):
        Engine.screen.draw_text(47, 2, "PWR:34")

    def draw_brightness_bar(self):
        Engine.screen.draw_text(97, 2, "B")
        Engine.screen.draw_rect(104, 2, 23, 1)
        Engine.screen.draw_rect(104, 6, 23, 1)
        Engine.screen.draw_rect(126, 3, 1, 3)

        bar_width = self.brightness * 7
        Engine.screen.draw_rect(104, 3, 2 + bar_width, 3)

    def draw_version(self):
        Engine.screen.draw_text(1, 2, f"PES:V{self.version}")

    def draw_choice_count(self):
        Engine.screen.draw_rect(4, 53, 1, 7)
        Engine.screen.draw_rect(5, 60, 32, 1)
        Engine.screen.draw_rect(36, 53, 1, 7)
        Engine.screen.draw_text(
            7, 54, f"{zfill(self.selection_index,2)}:{zfill(self.choice_count-1,2)}"
        )

    def draw_choices(self):
        Engine.screen.draw_rect(4, 9, 117, 1)
        Engine.screen.draw_rect(4, 10, 1, 43)
        Engine.screen.draw_rect(5, 52, 116, 1)
        Engine.screen.draw_rect(120, 10, 1, 42)

        if self.selection_index <= 1:
            min_visible_choice_index = 0
            max_visible_choice_index = 5

        elif self.selection_index >= self.choice_count - 3:
            min_visible_choice_index = self.choice_count - 6
            max_visible_choice_index = self.choice_count - 1

        else:
            min_visible_choice_index = self.selection_index - 2
            max_visible_choice_index = self.selection_index + 3

        min_visible_choice_index = max(min_visible_choice_index, 0)
        max_visible_choice_index = min(max_visible_choice_index, self.choice_count - 1)

        for i, choice_index in enumerate(
            range(min_visible_choice_index, max_visible_choice_index + 1)
        ):
            text = self.choices[choice_index][0]

            if choice_index == self.selection_index:
                text = ">" + text

            Engine.screen.draw_text(6, 11 + 7 * i, text)

    def handle_inputs(self):
        if HardwareState.UP.just_pressed():
            self.selection_index -= 1

        if HardwareState.DOWN.just_pressed():
            self.selection_index += 1

        if self.selection_index == -1:
            self.selection_index = self.choice_count - 1

        if self.selection_index == self.choice_count:
            self.selection_index = 0

        if HardwareState.ALPHA.just_pressed():
            self.engine_driver.running = False

        if HardwareState.BETA.just_pressed():
            self.brightness = 1 + (self.brightness % 3)
            self.set_ssd1306_brightness()

    def set_ssd1306_brightness(self):
        if self.brightness == 1:
            self.ssd1306_driver.contrast(1)

        if self.brightness == 2:
            self.ssd1306_driver.contrast(50)

        if self.brightness == 3:
            self.ssd1306_driver.contrast(255)

    def selection(self):
        return self.choices[self.selection_index]

    def create(self):
        if len(self.choices) == 0:
            Engine.screen.draw_text(10, 10, "NO GAMES FOUND")
            Engine.screen.flush()

            import sys

            sys.exit()

    def step(self):
        self.handle_inputs()
        self.draw()


def block_and_return_inject_selection(ssd1306_driver):
    engine_driver = EngineDriver()

    # kinda cursed but it works i guess
    inject_select_menu = InjectSelectMenu(engine_driver, ssd1306_driver)
    Engine.create_object(inject_select_menu)

    engine_driver.runloop()

    return inject_select_menu.selection()
