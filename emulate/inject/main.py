from screen import Screen
from engine import Engine
from .light import Light


def main(screen: Screen) -> Engine:
    light = Light(20, 20)
    
    engine = Engine(screen)
    engine.create_object(light)
    
    return engine
