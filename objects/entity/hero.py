import pygame
import random

from settings import gravity, player_speed, jump_height
from settings import platforms_sprites, ver_platform_sprites, enemy_sprites, all_sprites, fireballs
from objects.entity.wolf import Wolf
from objects.entity.owl import Owl
from skills.fireball import Fireball

class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, player_width, player_height):
        super().__init__()

        # Загружаем анимации сразу
        self.echo_animations = {
            'idle': [
                pygame.image.load('textures/echo_idle1.png'),
                pygame.image.load('textures/echo_idle1.png'),
                pygame.image.load('textures/echo_idle3.png'),
                pygame.image.load('textures/echo_idle4.png'),
                pygame.image.load('textures/echo_idle5.png'),
                pygame.image.load('textures/echo_idle6.png'),
                pygame.image.load('textures/echo_idle7.png'),
                pygame.image.load('textures/echo_idle8.png'),
                pygame.image.load('textures/echo_idle9.png'),
                pygame.image.load('textures/echo_idle8.png'),
                pygame.image.load('textures/echo_idle7.png'),
                pygame.image.load('textures/echo_idle6.png'),
                pygame.image.load('textures/echo_idle5.png'),
                pygame.image.load('textures/echo_idle4.png'),
                pygame.image.load('textures/echo_idle3.png'),
                pygame.image.load('textures/echo_idle2.png'),
                pygame.image.load('textures/echo_idle1.png'),
            ]
        }

        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 75 # Скорость смены кадров (мс)
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления кадра

        self.image = self.echo_animations[self.current_animation][self.frame_index]

        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.is_hanging = False

        self.max_health = 300
        self.health = self.max_health

        self.invulnerable = False
        self.invulnerable_time = 1500
        self.last_hit_time = 0

        self.last_fireball_attack_time = 0
        self.fireball_cooldown = 2500

        self.facing_right = False

    def update(self, *args):
        # Атака
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:  # Если нажата клавиша "F"
            self.attack(skill_name='fireball')  # Вызываем метод атаки

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
            self.facing_right = True  # Персонаж смотрит влево
        elif keys[pygame.K_d]:  # Движение вправо
            self.velocity_x = player_speed
            self.facing_right = False  # Персонаж смотрит вправо
        else:
            self.velocity_x = 0

        # Переворачиваем изображение, если персонаж двигается в другую сторону
        if not self.facing_right:
            self.image = pygame.transform.flip(self.echo_animations[self.current_animation][self.frame_index], True,
                                               False)
        else:
            self.image = self.echo_animations[self.current_animation][self.frame_index]

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

    def attack(self, skill_name):
        if skill_name == 'fireball':
            current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
            if current_time - self.last_fireball_attack_time >= self.fireball_cooldown:  # Проверяем, прошло ли достаточно времени
                direction = -1 if self.facing_right else +1  # Определяем направление по направлению взгляда
                fireball = Fireball(self.rect.centerx, self.rect.centery, direction)  # Создаем фаербол
                all_sprites.add(fireball)  # Добавьте фаербол в группу всех спрайтов
                fireballs.add(fireball)  # Добавьте фаербол в отдельную группу для фаерболов
                self.last_fireball_attack_time = current_time  # Обновляем время последней атаки

    def update_animation(self):
        now = pygame.time.get_ticks()  # Текущее время
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.echo_animations[self.current_animation])
            self.image = self.echo_animations[self.current_animation][self.frame_index]  # Меняем кадр

    def bounce_back(self, force):
        direction = random.choice(["left", "right", "up", "down"])  # Случайное направление
        if direction == "left":
            self.rect.x += force  # Отпрыгнуть вправо
        elif direction == "right":
            self.rect.x -= force  # Отпрыгнуть влево
        elif direction == "down":
            self.rect.y -= force  # Отпрыгнуть вверх

    def take_damage(self, amount):
        if not self.invulnerable:
            self.health -= amount
            if self.health < 0:
                self.health = 0  # Не допускаем отрицательного здоровья

            # Отскок при получении урона
            self.bounce_back(30)  # Вы можете настроить силу отскока здесь

            self.invulnerable = True
            self.last_hit_time = pygame.time.get_ticks()  # Запоминаем время удара

    def HP(self):
        enemy_collide = pygame.sprite.spritecollide(self, enemy_sprites, False)
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

