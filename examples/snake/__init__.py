from screen import Screen
from engine import Engine
from .border import Border
from .snake import Snake
from .score import Score
from .fruit import spawn_fruit


def main():
    border = Border()
    score = Score(110, 10)
    snake = Snake(10, 10)

    Engine.set_tick_cap(20)
    Engine.create_object(border)
    Engine.create_object(score)
    Engine.create_object(snake)

    spawn_fruit(snake=snake)
