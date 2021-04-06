import pygame
from Ball import Ball


class Door(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 50])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # self.color = color
        self.rect.topleft = initial_position
        self.display_width, self.display_height = pygame.display.get_surface().get_size()

