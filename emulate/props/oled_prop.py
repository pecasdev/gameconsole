from .arrange_config import OLED
from .prop import Prop
import pygame


class OledProp(Prop):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def draw(self, surface: pygame.Surface):
        rect = pygame.Rect(self.x, self.y, OLED["WIDTH"], OLED["HEIGHT"])

        pygame.draw.rect(surface, OLED["COLOR"], rect)
