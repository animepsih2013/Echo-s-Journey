import pygame
import random
pygame.init()


class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("grey"))
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(0, 0)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


all_sprites = pygame.sprite.Group()