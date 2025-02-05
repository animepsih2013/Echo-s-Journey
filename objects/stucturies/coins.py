import pygame
from settings import coin_value, score

font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)

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

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.coin_animation)
            self.image = self.coin_animation[self.frame_index]

    def update(self, player):
        global score  # Убедитесь, что мы используем глобальную переменную score
        self.update_animation()
        if self.rect.colliderect(player.rect):
            print("Coin collected!")
            self.kill()  # Удаляем монету
            score += coin_value  # Обновляем счет

def draw_score(surface):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый цвет текста
    surface.blit(score_text, (10, 10))
