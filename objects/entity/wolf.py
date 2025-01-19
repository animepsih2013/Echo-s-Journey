import pygame
import random

from settings import all_sprites

class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = -random.randint(4, 5)
        self.vy = random.randrange(3, 8)
        self.y_velocity = 0