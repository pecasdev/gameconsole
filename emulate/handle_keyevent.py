from typing import Any, Callable

from .keybind import Keybind
from .props.button_prop import Direction
from .props.directional_button import DirectionalPad
from .props.selection_button import SelectionButtons
import pygame


def handle_keys_pressed(
    keys_pressed: pygame.key.ScancodeWrapper,
    dpad: DirectionalPad,
    sbut: SelectionButtons,
):
    for keybind in [Keybind.LEFT, Keybind.RIGHT, Keybind.UP, Keybind.DOWN]:
        direction = Keybind.keybind_to_direction(keybind)
        if keybind and direction:
            if keys_pressed[keybind]:
                dpad.press_button(direction)
            else:
                dpad.release_button(direction)

    for keybind in [Keybind.ALPHA, Keybind.BETA]:
        selection = Keybind.keybind_to_selection(keybind)
        if keybind and selection:
            if keys_pressed[keybind]:
                sbut.press_button(selection)
            else:
                sbut.release_button(selection)
