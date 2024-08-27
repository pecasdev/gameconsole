from engine import Engine
from .world import World

def main():
    world = World()
    Engine.create_object(world)
    Engine.set_tick_cap(6)

# todo - add "time survived" stat to gui