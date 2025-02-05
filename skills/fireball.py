import pygame
from settings import enemy_sprites, fireballs
from objects.entity.owl import Owl
from objects.entity.wolf import Wolf

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.fireball_animations = {
            'fly': [
                pygame.transform.scale(pygame.image.load(f'textures/fireball_{i}.png').convert_alpha(), (50, 50))
                for i in range(1, 5)
            ] * 2,  # Повторяем кадры
            'boom': [
                pygame.transform.scale(pygame.image.load('textures/boom.png').convert_alpha(), (100, 100))
                for _ in range(3)
            ]
        }

        self.current_animation = 'fly'
        self.frame_index = 0
        self.animation_speed = 90
        self.last_update = pygame.time.get_ticks()

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
        self.update_animation()

    def update(self, player):
        if not self.exploding:
            self.rect.x += self.velocity_x  # Двигаем фаербол
            enemy_collide = pygame.sprite.spritecollide(self, enemy_sprites, False)

            for enemy in enemy_collide:
                if isinstance(enemy, (Wolf, Owl)):
                    self.explode()  # Начинаем взрыв
                    enemy.kill()

        self.update_animation()  # Всегда обновляем анимацию
