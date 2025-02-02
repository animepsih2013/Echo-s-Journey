import pygame

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture=None):
        super().__init__()
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect(topleft=(x, y))


class Platform_ver(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture=None):
        super().__init__()
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect(topleft=(x, y))
