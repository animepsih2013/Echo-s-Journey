import pygame
from settings import gravity
from settings import all_sprites
from settings import platforms_sprites

class Owl(pygame.sprite.Sprite):
    def __init__(self, x, y, owl_width, owl_height, texture, damage):
        super().__init__(all_sprites)
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color('yellow'))
        self.velocity_x = 0
        self.velocity_y = 0
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage

    def update(self):
        pass