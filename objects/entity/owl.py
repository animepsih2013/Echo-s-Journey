import pygame
import math
from settings import all_sprites

owl_speed = 3  # Уменьшим скорость для плавного движения
detection_radius = 200


class Owl(pygame.sprite.Sprite):
    def __init__(self, x, y, owl_width, owl_height, texture, damage):
        super().__init__(all_sprites)

        self.bat_animation = [
            pygame.transform.scale(pygame.image.load('textures/bat_1.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_2.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_3.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_4.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_5.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_6.png').convert_alpha(), (150, 130))
        ]

        self.frame_index = 0
        self.animation_speed = 120
        self.last_update = pygame.time.get_ticks()

        self.image = self.bat_animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.damage = damage
        self.state = 'sitting'  # Изначально сидит
        self.target_position = None

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.bat_animation)
            self.image = self.bat_animation[self.frame_index]

    def fly_to_player(self):
        if self.target_position:
            # Вектор движения
            dx = self.target_position[0] - self.rect.centerx
            dy = self.target_position[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > owl_speed:  # Если не достиг игрока
                angle = math.atan2(dy, dx)
                move_x = owl_speed * math.cos(angle)
                move_y = owl_speed * math.sin(angle)
                self.rect.x += int(move_x)
                self.rect.y += int(move_y)
            else:
                self.rect.center = self.target_position  # Остановка у игрока

    # Пример исправления, если игрок — это объект Hero, и его позиция хранится в rect
    def check_player_distance(self, player):
        # Получаем позицию игрока из его rect
        player_position = (player.rect.centerx, player.rect.centery)

        distance = math.sqrt(
            (self.rect.centerx - player_position[0]) ** 2 + (self.rect.centery - player_position[1]) ** 2)

        if distance < detection_radius:
            self.state = 'flying'
            self.target_position = player_position  # Устанавливаем цель

    def update(self, player_position):
        self.update_animation()
        self.check_player_distance(player_position)  # Проверяем расстояние до игрока

        if self.state == 'flying':
            self.fly_to_player()  # Летим к игроку
