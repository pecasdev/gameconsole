class ButtonState:

    def __init__(self, is_pressed: bool):
        self.just_happened = True
        self.is_pressed = is_pressed

    def ack_just(self):
        self.just_happened = False

    def just_pressed(self):
        return self.just_happened and self.is_pressed

    def just_released(self):
        return self.just_happened and not self.is_pressed

    def __str__(self):
        exclaim = "!" if self.just_happened else ""
        return exclaim + "_" if self.is_pressed else "^" + exclaim

    def update(self, other):
        if self.is_pressed != other.is_pressed:
            print("updating", self, "to", other)
            self.is_pressed = other.is_pressed
            self.just_happened = other.just_happened

    def __repr__(self):
        return str(self)


class HardwareState:
    LEFT: ButtonState = ButtonState(
        False,
    )
    RIGHT: ButtonState = ButtonState(False)
    UP: ButtonState = ButtonState(False)
    DOWN: ButtonState = ButtonState(
        False,
    )
    ALPHA: ButtonState = ButtonState(
        False,
    )
    BETA: ButtonState = ButtonState(
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
    def ack_button_states():
        print("acknowledged button states")
        HardwareState.LEFT.ack_just()
        HardwareState.RIGHT.ack_just()
        HardwareState.UP.ack_just()
        HardwareState.DOWN.ack_just()
        HardwareState.ALPHA.ack_just()
        HardwareState.BETA.ack_just()
