import pygame
import random

ground_textures = ["textures/ground_1.png", "textures/ground_2.png", "textures/ground_3.png"]
ground_random_choice = random.choice(ground_textures)
ground_image = pygame.image.load(ground_random_choice)

from settings import platforms_sprites, all_sprites
from settings import screen_width

# Класс травы (нижней платформы)
class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, texture, ground_width, ground_height):
        super().__init__(platforms_sprites, all_sprites)
        self.image = ground_image
        self.rect = self.image.get_rect(topleft=pos)