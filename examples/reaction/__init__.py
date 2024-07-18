from screen import Screen
from engine import Engine
from .light import Light


def main():
    light = Light(20, 20)

    Engine.create_object(light)
