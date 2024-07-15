import pygame

from props.button_prop import Direction


# choose "common name" keybind from: http://cs.roanoke.edu/Fall2013/CPSC120A/pygame-1.9.1-docs-html/ref/key.html
class Keybind:
    UP = None
    DOWN = None
    LEFT = None
    RIGHT = None
    ALPHA = None
    BETA = None

    def read_from_config(self):
        with open("./emulate/keybind.config") as f:
            lines = f.readlines()
            for line in filter(lambda x: len(x) > 0, lines):
                [action, keybind] = [x.strip() for x in line.split("=")]
                keybind = pygame.key.key_code(keybind)

                match action:
                    case "UP":
                        Keybind.UP = keybind
                    case "DOWN":
                        Keybind.DOWN = keybind
                    case "LEFT":
                        Keybind.LEFT = keybind
                    case "RIGHT":
                        Keybind.RIGHT = keybind
                    case "ALPHA":
                        Keybind.ALPHA = keybind
                    case "BETA":
                        Keybind.BETA = keybind
                    case _:
                        raise Exception("Parse error when reading keybind.config")

    @staticmethod
    def keybind_to_direction(key: str) -> Direction | None:
        match key:
            case Keybind.LEFT:
                return Direction.LEFT
            case Keybind.RIGHT:
                return Direction.RIGHT
            case Keybind.UP:
                return Direction.UP
            case Keybind.DOWN:
                return Direction.DOWN
            case _:
                return None

    @staticmethod
    def keybind_to_selection(key: str) -> str | None:
        match key:
            case Keybind.ALPHA:
                return "ALPHA"
            case Keybind.BETA:
                return "BETA"
            case _:
                return None
