import pygame
from .props.button_prop import ButtonProp, Direction
from hardware_state import ButtonState, HardwareState
from .pygame_driver import PygameDriver
from .pygame_screen_adaptor import PygameScreenAdaptor
from engine import Engine
from .props.hardware_prop import HardwareProp
from .keybind import Keybind
from .handle_keyevent import handle_keys_pressed
from typing import Callable
import threading


class Emulator:
    def __init__(
        self,
        engine_psa: PygameScreenAdaptor,
        pygame_driver: PygameDriver,
    ):
        self.engine_psa = engine_psa
        self.pygame_driver = pygame_driver

        self.keybind = Keybind()
        self.keybind.read_from_config()

        self.hardware_prop = HardwareProp(0, 0)

        self.button_handlers: list[Callable[[], tuple[str, ButtonState]]] = [
            self._create_button_state_handler("LEFT", Keybind.LEFT),
            self._create_button_state_handler("RIGHT", Keybind.RIGHT),
            self._create_button_state_handler("UP", Keybind.UP),
            self._create_button_state_handler("DOWN", Keybind.DOWN),
            self._create_button_state_handler("ALPHA", Keybind.ALPHA),
            self._create_button_state_handler("BETA", Keybind.BETA),
        ]

        self.internal_hardware_state = HardwareState.as_dict()

    def handle_pygame_key_presses(self):
        sbut = self.hardware_prop.sbut_prop
        dpad = self.hardware_prop.dpad_prop

        pressed = pygame.key.get_pressed()
        handle_keys_pressed(pressed, dpad, sbut)

    def handle_pygame_events(self):
        self.handle_pygame_key_presses()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _create_button_state_handler(
        self, button_name: str, key: int
    ) -> Callable[[], tuple[str, ButtonState]]:
        def handle() -> tuple[str, ButtonState]:
            button_is_pressed = pygame.key.get_pressed()[key]

            return (
                button_name,
                ButtonState(button_is_pressed),
            )

        return handle

    def update_internal_hardware_state(self):
        self.internal_hardware_state = self._hardware_state_dict_from_prop()

    def update_engine_hardware_state(self):
        Engine.update_hardware_state(self.internal_hardware_state)

    def _hardware_state_dict_from_prop(self) -> dict[str, ButtonState]:
        return dict([handle() for handle in self.button_handlers])

    def _render_pygame_stuff(self):
        # init drawlayer
        drawlayer = self.pygame_driver.copy_surface()

        # draw hardware prop
        self.hardware_prop.blit_to_surface(drawlayer)

        # blit engine screen to drawlayer
        oled_prop = self.hardware_prop.oled_prop
        self.engine_psa.blit_to_surface(drawlayer, (oled_prop.x, oled_prop.y))

        # blit drawlayer and flip
        self.pygame_driver.blit(drawlayer, (0, 0))
        self.pygame_driver.flip()

    def runloop(self):
        self.running = True
        Engine.set_emulator_tick_override(True)
        while self.running:
            try:
                self.handle_pygame_events()
                self.update_internal_hardware_state()
                self.update_engine_hardware_state()

                Engine.tick()
                self._render_pygame_stuff()

                HardwareState.ack_button_states()

            except KeyboardInterrupt:
                self.running = False
