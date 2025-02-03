import pygame

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Размер фаербола
        self.image.fill(pygame.Color('red'))  # Цвет фаербола
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 10 * direction  # Устанавливаем скорость в зависимости от направления

    def update(self):
        self.rect.x += self.velocity_x  # Двигаем фаербол
        # Здесь можно добавить логику для уничтожения фаербола при столкновении с врагами или выходе за границы экрана