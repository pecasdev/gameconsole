import pygame
from props.button_prop import ButtonProp, Direction
from hardware_state import ButtonState, HardwareState
from pygame_driver import PygameDriver
from pygame_screen_adaptor import PygameScreenAdaptor
from engine import Engine
from props.hardware_prop import HardwareProp
from keybind import Keybind
from handle_keyevent import handle_keyevent
from typing import Callable


class Emulator:
    def __init__(
        self,
        engine: Engine,
        engine_psa: PygameScreenAdaptor,
        pygame_driver: PygameDriver,
    ):
        self.engine = engine
        self.engine_psa = engine_psa
        self.pygame_driver = pygame_driver

        self.keybind = Keybind()
        self.keybind.read_from_config()

        self.hardware_prop = HardwareProp(0, 0)

        dpad_buttons = self.hardware_prop.dpad_prop.buttons
        sbut_buttons = self.hardware_prop.sbut_prop.buttons

        self.button_handlers: list[Callable[[], tuple[str, ButtonState]]] = [
            self.__create_button_state_handler("LEFT", dpad_buttons[Direction.LEFT]),
            self.__create_button_state_handler("RIGHT", dpad_buttons[Direction.RIGHT]),
            self.__create_button_state_handler("UP", dpad_buttons[Direction.UP]),
            self.__create_button_state_handler("DOWN", dpad_buttons[Direction.DOWN]),
            self.__create_button_state_handler("ALPHA", sbut_buttons["ALPHA"]),
            self.__create_button_state_handler("BETA", sbut_buttons["BETA"]),
        ]

    def handle_pygame_events(self):
        sbut = self.hardware_prop.sbut_prop
        dpad = self.hardware_prop.dpad_prop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.engine.kill()

            if event.type == pygame.KEYDOWN:
                handle_keyevent(
                    self.keybind,
                    event.key,
                    lambda d: dpad.press_button(d),
                    lambda s: sbut.press_button(s),
                )

            if event.type == pygame.KEYUP:
                handle_keyevent(
                    self.keybind,
                    event.key,
                    lambda d: dpad.release_button(d),
                    lambda s: sbut.release_button(s),
                )

    def __create_button_state_handler(
        self, button_name: str, button_prop: ButtonProp
    ) -> Callable[[], tuple[str, ButtonState]]:
        def generator():
            while True:
                yield button_prop.pressed_down

        gen = generator()
        previous_button_is_pressed = False

        def handle() -> tuple[str, ButtonState]:
            nonlocal previous_button_is_pressed
            button_is_pressed = next(gen)

            previous_button_is_pressed = button_is_pressed

            return (
                button_name,
                ButtonState(button_is_pressed),
            )

        return handle

    def __hardware_state_dict_from_prop(self) -> dict[str, ButtonState]:
        return dict([handle() for handle in self.button_handlers])

    def runloop(self):
        self.running = True
        while self.running:
            self.handle_pygame_events()

            # debug clear
            self.pygame_driver.clear(pygame.Color("red"))

            # init drawlayer
            drawlayer = self.pygame_driver.copy_surface()

            # draw hardware prop
            self.hardware_prop.blit_to_surface(drawlayer)

            # draw engine tick
            self.engine.update_hardware_state(self.__hardware_state_dict_from_prop())
            self.engine.tick()
            oled_prop = self.hardware_prop.oled_prop
            self.engine_psa.blit_to_surface(drawlayer, (oled_prop.x, oled_prop.y))

            # blit drawlayer and flip
            self.pygame_driver.blit(drawlayer, (0, 0))
            self.pygame_driver.flip()

            # acknowledge buttons
            HardwareState.ack_button_states()