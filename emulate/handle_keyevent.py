from typing import Any, Callable

from keybind import Keybind
from props.button_prop import Direction


def handle_keyevent(
    keybind: Keybind,
    key: Any,
    on_direction: Callable[[Direction], None],
    on_selection: Callable[[str], None],
):
    direction = keybind.keybind_to_direction(key)
    selection = keybind.keybind_to_selection(key)

    if direction is not None:
        on_direction(direction)

    if selection is not None:
        on_selection(selection)
