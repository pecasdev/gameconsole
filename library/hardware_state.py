class ButtonState:
    def __init__(self, is_pressed: bool, just_happened: bool = True):
        self.__just_happened = just_happened
        self.is_pressed = is_pressed

    def ack_just(self):
        self.__just_happened = False

    def just_pressed(self):
        return self.__just_happened and self.is_pressed

    def just_released(self):
        return self.__just_happened and not self.is_pressed

    def __str__(self):
        exclaim = "!" if self.__just_happened else ""
        return exclaim + "_" if self.is_pressed else "^" + exclaim

    def update(self, other):
        if self.is_pressed != other.is_pressed:
            self.is_pressed = other.is_pressed
            self.__just_happened = other.__just_happened

    def __repr__(self):
        return str(self)


class HardwareState:
    LEFT: ButtonState = ButtonState(False, False)
    RIGHT: ButtonState = ButtonState(False, False)
    UP: ButtonState = ButtonState(False, False)
    DOWN: ButtonState = ButtonState(
        False,
        False,
    )
    ALPHA: ButtonState = ButtonState(
        False,
        False,
    )
    BETA: ButtonState = ButtonState(
        False,
        False,
    )

    @staticmethod
    def update_from_dict(dict: dict[str, ButtonState]):
        HardwareState.LEFT.update(dict["LEFT"])
        HardwareState.RIGHT.update(dict["RIGHT"])
        HardwareState.UP.update(dict["UP"])
        HardwareState.DOWN.update(dict["DOWN"])
        HardwareState.ALPHA.update(dict["ALPHA"])
        HardwareState.BETA.update(dict["BETA"])

    @staticmethod
    def as_dict():
        return {
            "LEFT": HardwareState.LEFT,
            "RIGHT": HardwareState.RIGHT,
            "UP": HardwareState.UP,
            "DOWN": HardwareState.DOWN,
            "ALPHA": HardwareState.ALPHA,
            "BETA": HardwareState.BETA,
        }

    @staticmethod
    def as_string():
        return " ".join(
            [
                "L" + str(HardwareState.LEFT),
                "R" + str(HardwareState.RIGHT),
                "U" + str(HardwareState.UP),
                "D" + str(HardwareState.DOWN),
                "A" + str(HardwareState.ALPHA),
                "B" + str(HardwareState.BETA),
            ]
        )

    @staticmethod
    def reset():
        HardwareState.LEFT = ButtonState(False, False)
        HardwareState.RIGHT = ButtonState(False, False)
        HardwareState.UP = ButtonState(False, False)
        HardwareState.DOWN = ButtonState(False, False)
        HardwareState.ALPHA = ButtonState(False, False)
        HardwareState.BETA = ButtonState(False, False)

    @staticmethod
    def ack_button_states():
        HardwareState.LEFT.ack_just()
        HardwareState.RIGHT.ack_just()
        HardwareState.UP.ack_just()
        HardwareState.DOWN.ack_just()
        HardwareState.ALPHA.ack_just()
        HardwareState.BETA.ack_just()
