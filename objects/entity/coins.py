import pygame

from settings import all_sprites


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_width, coin_height, texture=None, damage=0):
        super().__init__()
        if texture:
            try:
                self.image = pygame.image.load(texture)
            except pygame.error as e:
                print(f"Unable to load texture: {texture}. Error: {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(pygame.Color('orange'))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(pygame.Color('orange'))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player):
        if self.rect.colliderect(player.rect):
            print("Coin collected!")
            self.kill()