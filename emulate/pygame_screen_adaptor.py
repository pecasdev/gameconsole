from font import Font
from .pygame_driver import PygameDriver
from screen_adaptor.screen_adaptor import ScreenAdaptor
import pygame


class PygameScreenAdaptor(ScreenAdaptor):
    pygame_driver: PygameDriver

    def __init__(self, width: int, height: int, pygame_driver: PygameDriver) -> None:
        super().__init__(width, height)
        self.pygame_driver = pygame_driver
        self.display = pygame.Surface((width, height))

    def clear(self):
        self.display.fill(pygame.Color("black"))

    def draw_pixel(self, x: int, y: int):
        self.display.set_at((x, y), pygame.Color("white"))

    def draw_text(self, x: int, y: int, text: str, font: Font):
        font.draw_text(x, y, text)
    
    def flush(self):
        self.pygame_driver.blit(self.display, (0, 0))

    def kill(self):
        self.pygame_driver.kill()

    def blit_to_surface(self, surface: pygame.Surface, dest: tuple[int, int]):
        surface.blit(self.display, dest)
