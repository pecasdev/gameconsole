import pygame
from screen_adaptor import ScreenAdaptor
from frame_buffer_adaptor import FrameBufferAdaptor


class PygameFrameBufferAdaptor(FrameBufferAdaptor):
    def __init__(self, width, height, screen_adaptor: ScreenAdaptor) -> None:
        super().__init__(width, height, screen_adaptor)
        self.buffer = pygame.Surface((width, height))
    
    def draw_pixel(self, x, y):
        self.buffer.set_at((x, y), pygame.Color("white"))
