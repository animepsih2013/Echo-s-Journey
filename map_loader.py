import pygame
import sys
import random

from settings import all_sprites, platforms_sprites
from settings import screen_height, screen_width
from settings import platform_sizes, ver_platform_sizes, ground_sizes, entity_sizes

from objects.entity.hero import Hero
from objects.entity.wolf import Wolf
from objects.entity.owl import Owl

from objects.stucturies.platforms import Platform
from objects.stucturies.platforms import Platform_ver
from objects.stucturies.ground import Ground

ground_count = 0  # Счетчик для загрузки рандомных спрайтов земли
ground_random_textures = []
cell_width = 64
cell_height = 64

# Текстуры земли
ground_textures = ["textures/ground_1.png", "textures/ground_2.png", "textures/ground_3.png"]

# Предполагается, что platform_sizes и другие необходимые словари определены ранее в коде

def load_map_from_file(filename):
    try:
        with open(filename, 'r') as file:
            map_data = [line.strip() for line in file]

        player = None  # Указатель на игрока

        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                world_x = x * cell_width  # Базовая сетка, размеры объектов меняем отдельно
                world_y = y * cell_height

                if cell in platform_sizes:  # Горизонтальные платформы
                    try:
                        width_percent, height_percent, platform_texture = platform_sizes[cell]
                        platform_width = int(cell_width * width_percent)
                        platform_height = int(cell_height * height_percent)
                        print(platform_width, platform_height)
                        platform = Platform(world_x, world_y, platform_width, platform_height, platform_texture)
                        platforms_sprites.add(platform)
                        all_sprites.add(platform)
                    except Exception as e:
                        print(f"Ошибка при создании платформы: {e}")

                elif cell == 'g':  # Земля
                    ground_texture = random.choice(ground_textures)
                    ground_width, ground_height = ground_sizes.get(cell, (cell_width, cell_height))  # Получаем размеры земли с значениями по умолчанию
                    ground = Ground((world_x, world_y), pygame.image.load(ground_texture), ground_width, ground_height)
                    all_sprites.add(ground)

                elif cell in ver_platform_sizes:  # Вертикальные платформы
                    width_percent, height_percent = ver_platform_sizes[cell]
                    platform_width = int(cell_width * width_percent)
                    platform_height = int(cell_height * height_percent)

                    ver_platform = Platform_ver(world_x, world_y, platform_height, platform_width)
                    all_sprites.add(ver_platform)

                elif cell == '@':  # Игрок
                    player_width, player_height = entity_sizes['@']  # Размеры игрока
                    player = Hero(world_x, world_y, player_width, player_height, "textures/player.png")
                    all_sprites.add(player)

                elif cell == 'w':  # Волк
                    wolf_width, wolf_height = entity_sizes['w']  # Размеры волка
                    wolf = Wolf(world_x, world_y, wolf_width, wolf_height)
                    all_sprites.add(wolf)

                elif cell == 'o':  # Сова
                    owl_width, owl_height = entity_sizes['o']  # Размеры совы
                    owl = Owl(world_x, world_y, owl_width, owl_height)
                    all_sprites.add(owl)

        # Проверяем, найден ли игрок
        if player is None:
            raise ValueError("Ошибка: В файле карты отсутствует символ '@' для игрока!")

        return map_data, player

    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return None, None


class Camera:
    def __init__(self):
        self.dx = 0  # Горизонтальное смещение
        self.dy = 0  # Вертикальное смещение

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.centerx - screen_width // 2)
