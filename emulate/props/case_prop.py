from .arrange_config import CASE
from .prop import Prop
import pygame


class CaseProp(Prop):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def draw(self, surface):
        rect = pygame.Rect(
            self.x,
            self.y,
            CASE["WIDTH"],
            CASE["HEIGHT"],
        )

        pygame.draw.rect(surface, CASE["COLOR"], rect)
