import pygame

from settings import platforms_sprites, all_sprites
from settings import screen_width

# Класс травы (нижней платформы)
class Grass(pygame.sprite.Sprite):
    def __init__(self, pos, texture):
        super().__init__(platforms_sprites, all_sprites)
        self.image = pygame.transform.scale(texture, (screen_width, texture.get_height()))
        self.rect = self.image.get_rect(topleft=pos)