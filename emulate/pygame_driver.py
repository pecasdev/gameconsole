import sys
import pygame


class PygameDriver:
    framerate = 30
    display_scale = 3
    display: pygame.Surface

    def init_driver(self, display_width: int, display_height: int):
        pygame.init()
        pygame.font.init()

        self.display = pygame.display.set_mode(
            [
                display_width * PygameDriver.display_scale,
                display_height * PygameDriver.display_scale,
            ]
        )

        self.clock = pygame.time.Clock()

    def copy_surface(self):
        return self.display.copy()

    def kill(self):
        pygame.quit()
        sys.exit()

    def clear(self, color: pygame.Color = pygame.Color("black")):
        self.display.fill(color)

    def blit(self, surface: pygame.Surface, dest: tuple[int, int]):
        scaled_surface = pygame.transform.scale_by(surface, PygameDriver.display_scale)
        self.display.blit(scaled_surface, dest)

    def flip(self):
        self.__tick()
        pygame.display.flip()

    def __tick(self):
        self.clock.tick(PygameDriver.framerate)
