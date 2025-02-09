import pygame
from settings import enemy_sprites, fireballs
from skills.score import get_score

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.fireball_animations = {
            'fly': [
                pygame.transform.scale(pygame.image.load(f'textures/fireball_{i}.png').convert_alpha(), (65, 65))
                for i in range(1, 5)
            ] * 2,  # Повторяем кадры
            'boom': [
                pygame.transform.scale(pygame.image.load(f'textures/boom_{i}.png').convert_alpha(), (250, 350))
                for i in range(1, 12)
            ]
        }
        self.owl_reward = 150

        self.current_animation = 'fly'
        self.frame_index = 0
        self.animation_speed = 90
        self.last_update = pygame.time.get_ticks()
        self.burn_zone = 350 # Радиус уничтожения врагов

        self.velocity_x = 10 * direction

        self.image = self.fireball_animations[self.current_animation][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.exploding = False  # Флаг, обозначающий, что фаербол взрывается

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index += 1

            # Если анимация "boom" закончилась, удаляем фаербол
            if self.exploding and self.frame_index >= len(self.fireball_animations['boom']):
                self.kill()
                return

            # Обычная смена кадров анимации
            self.frame_index %= len(self.fireball_animations[self.current_animation])
            self.image = self.fireball_animations[self.current_animation][self.frame_index]

    def explode(self):
        self.current_animation = 'boom'
        self.frame_index = 0
        self.exploding = True  # Устанавливаем флаг, что фаербол взрывается
        self.velocity_x = 0  # Останавливаем движение

        # Уничтожаем всех врагов в радиусе взрыва
        for enemy in enemy_sprites:
            if abs(self.rect.centerx - enemy.rect.centerx) < self.burn_zone and \
               abs(self.rect.centery - enemy.rect.centery) < self.burn_zone:
                enemy.kill()  # Просто удаляем врагов
                get_score(self.owl_reward)

    def update(self, player):
        if not self.exploding:
            self.rect.x += self.velocity_x  # Двигаем фаербол
            enemy_collide = pygame.sprite.spritecollide(self, enemy_sprites, False)

            if enemy_collide:  # Если фаербол сталкивается с врагами
                self.explode()  # Начинаем взрыв

        self.update_animation()  # Всегда обновляем анимацию
