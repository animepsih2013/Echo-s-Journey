import pygame

from settings import all_sprites

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_width, coin_height, texture, damage):
        super().__init__()
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()  # Удаляем монетку при сборе