import pygame
import random

from settings import gravity, player_speed, jump_height, enemy_sprites
from settings import platforms_sprites, ver_platform_sprites
from objects.entity.wolf import Wolf
from objects.entity.owl import Owl


# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height, texture):
        super().__init__()
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color('blue'))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 0  # Скорость по оси X
        self.velocity_y = 0  # Скорость по оси Y
        self.is_jumping = False
        self.is_hanging = False
        self.max_health = 300
        self.health = self.max_health
        self.invulnerable = False  # Неуязвимость
        self.invulnerable_time = 1500  # Время неуязвимости в миллисекундах
        self.last_hit_time = 0

    def take_damage(self, amount):
        if not self.invulnerable:
            self.health -= amount
            if self.health < 0:
                self.health = 0  # Не допускаем отрицательного здоровья

            # Отскок при получении урона
            self.bounce_back(20)  # Вы можете настроить силу отскока здесь

            self.invulnerable = True
            self.last_hit_time = pygame.time.get_ticks()  # Запоминаем время удара

    def bounce_back(self, force):
        direction = random.choice(["left", "right", "up", "down"])  # Случайное направление
        if direction == "left":
            self.rect.x += force  # Отпрыгнуть вправо
        elif direction == "right":
            self.rect.x -= force  # Отпрыгнуть влево
        elif direction == "up":
            self.rect.y += force  # Отпрыгнуть вниз
        elif direction == "down":
            self.rect.y -= force  # Отпрыгнуть вверх

    def update(self):
        # Проверка времени неуязвимости
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time > self.invulnerable_time:
                self.invulnerable = False

        # Гравитация
        if not self.is_hanging:
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
        if keys[pygame.K_SPACE] and not self.is_jumping and not self.is_hanging:
            self.velocity_y = -jump_height
            self.is_jumping = True

        # Обновление позиции по X
        self.rect.x += self.velocity_x
        self.handle_collision_x()  # Проверка столкновений по X

        # Проверка столкновений с вертикальными платформами
        self.handle_vertical_platforms()

        # Обновление позиции по Y, если не висящий
        if not self.is_hanging:
            self.rect.y += self.velocity_y
            self.handle_collision_y()  # Проверка столкновений по Y

    def HP(self):
        enemy_collide = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for enemy in enemy_collide:
            if isinstance(enemy, Wolf):  # Проверяем, является ли враг волком
                self.take_damage(enemy.damage)  # Наносим урон герою
                print(f'Hero damaged! Current health: {self.health}')  # Для отладки

        for enemy in enemy_collide:
            if isinstance(enemy, Owl):  # Проверяем, является ли враг волком
                self.take_damage(enemy.damage)  # Наносим урон герою
                print(f'Hero damaged! Current health: {self.health}')  # Для отладки

    def handle_vertical_platforms(self):
        collided_vertical_platforms = pygame.sprite.spritecollide(self, ver_platform_sprites, False)

        if collided_vertical_platforms:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:  # Движение вверх по лестнице
                self.is_hanging = True
                self.velocity_y = -player_speed  # Ползание вверх по лестнице
            elif keys[pygame.K_s]:  # Движение вниз по лестнице
                self.is_hanging = True
                self.velocity_y = player_speed  # Ползание вниз по лестнице
            else:
                self.is_hanging = False

            # Обновление позиции по Y при ползании
            if self.is_hanging:
                self.rect.y += self.velocity_y

        else:
            # Если не на лестнице, то сбрасываем состояние "висящий"
            self.is_hanging = False

    def handle_collision_x(self):
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_x > 0:  # Движение вправо
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  # Движение влево
                self.rect.left = platform.rect.right

    def handle_collision_y(self):
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_y > 0:  # Падение вниз
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            elif self.velocity_y < 0:  # Прыжок вверх
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

