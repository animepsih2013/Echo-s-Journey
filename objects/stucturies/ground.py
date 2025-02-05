import pygame
import random

from settings import platforms_sprites, all_sprites

# Класс травы (нижней платформы)
class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, texture, ground_width, ground_height):
        super().__init__(platforms_sprites, all_sprites)
        self.image = texture
        self.rect = self.image.get_rect(topleft=pos)

    def none(self, *args):
        pass