import pygame
from skills.score import score
from skills.score import get_score

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_width, coin_height, texture=None):
        super().__init__()

        # Загружаем анимации сразу
        self.coin_animation = [
            pygame.image.load('textures/coin_1.png').convert_alpha(),
            pygame.image.load('textures/coin_2.png').convert_alpha(),
            pygame.image.load('textures/coin_3.png').convert_alpha(),
            pygame.image.load('textures/coin_4.png').convert_alpha(),
            pygame.image.load('textures/coin_5.png').convert_alpha(),
            pygame.image.load('textures/coin_6.png').convert_alpha(),
        ]

        self.frame_index = 0
        self.animation_speed = 160  # Скорость смены кадров (мс)
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления кадра

        self.image = self.coin_animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.coin_value = 100

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.coin_animation)
            self.image = self.coin_animation[self.frame_index]

    def update(self, player):
        self.update_animation()
        if self.rect.colliderect(player.rect):
            self.kill()  # Удаляем монету
            get_score(self.coin_value)

