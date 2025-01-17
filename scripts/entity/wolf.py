import pygame
import random

# Класс реализующий волка
class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = -random.randint(4, 5)
        self.vy = random.randrange(3, 8)
        self.y_velocity = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        collision = pygame.sprite.spritecollideany(self, platforms)
        if collision:
            # Если герой падает вниз и касается платформы
            if self.rect.bottom <= collision.rect.bottom:
                self.rect.bottom = collision.rect.top  # Останавливаем персонажа на платформе
                self.y_velocity = 0

        # Ограничение движения по вертикали (не падаем ниже экрана)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_velocity = 0