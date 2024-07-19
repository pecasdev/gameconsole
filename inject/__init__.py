from screen import Screen
from engine import Engine
from .light import Light
from sprite import Sprite
import sys

def main():
    stop_sprite = Sprite.load_from_file("stop_sign.sprite")
    
    light = Light(20, 20, stop_sprite)
    
    Engine.create_object(light)
