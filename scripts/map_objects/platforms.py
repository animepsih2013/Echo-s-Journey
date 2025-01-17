import pygame

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture=None):
        super().__init__()
        if texture:  # Если текстура задана
            self.image = pygame.image.load(texture)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:  # Если текстура не задана, используем стандартное заполнение цветом
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect(topleft=(x, y))