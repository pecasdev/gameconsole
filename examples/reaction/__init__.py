from engine import Engine
from sprite import Sprite
from .ralph import Ralph
from .world import World


def main():
    ralph_sleep = Sprite.load_from_file("sprites/ralph_sleep.sprite")
    ralph_wait = Sprite.load_from_file("sprites/ralph_wait.sprite")
    ralph_go = Sprite.load_from_file("sprites/ralph_go.sprite")
    ralph_thumb_up = Sprite.load_from_file("sprites/ralph_thumb_up.sprite")

    ralph = Ralph(
        {
            "sleep": ralph_sleep,
            "wait": ralph_wait,
            "go": ralph_go,
            "thumb_up": ralph_thumb_up,
        },
    )

    world = World(ralph=ralph)

    Engine.create_object(world)
