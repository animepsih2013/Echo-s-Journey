import pygame
from pygame import Surface

from settings import gravity, player_speed, jump_height
from settings import platforms_sprites

# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height, texture):
        super().__init__()
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color('blue'))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 0  # Скорость по оси X
        self.velocity_y = 0  # Скорость по оси Y
        self.is_jumping = False

    def update(self):
        # Гравитация
        self.velocity_y += gravity
        if self.velocity_y > 10:  # Ограничиваем максимальную скорость падения
            self.velocity_y = 10

        # Горизонтальное движение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Движение влево
            self.velocity_x = -player_speed
        elif keys[pygame.K_d]:  # Движение вправо
            self.velocity_x = player_speed
        else:
            self.velocity_x = 0

        # Прыжок
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = -jump_height
            self.is_jumping = True

        # Обновление позиции
        self.rect.x += self.velocity_x
        self.handle_collision_x()  # Проверка столкновений по X

        self.rect.y += self.velocity_y
        self.handle_collision_y()  # Проверка столкновений по Y

    def handle_collision_x(self):
        # Проверяем столкновения по оси X
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_x > 0:  # Движение вправо
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  # Движение влево
                self.rect.left = platform.rect.right

    def handle_collision_y(self):
        # Проверяем столкновения по оси Y
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_y > 0:  # Падение вниз
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            elif self.velocity_y < 0:  # Прыжок вверх
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0