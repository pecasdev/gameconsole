import pygame


class Prop:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, surface: pygame.Surface):
        raise NotImplementedError
