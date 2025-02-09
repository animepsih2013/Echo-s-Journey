import pygame
import random

from settings import all_sprites, platforms_sprites, ver_platform_sprites, enemy_sprites, coins
from settings import screen_width, screen_height
from settings import platform_sizes, ver_platform_sizes, ground_sizes, entity_sizes

from objects.entity.hero import Hero
from objects.entity.wolf import Wolf
from objects.entity.owl import Owl
from objects.stucturies.coins import Coin

from objects.stucturies.platforms import Platform
from objects.stucturies.platforms import Platform_ver
from objects.stucturies.ground import Ground

from settings import screen_height

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
        owl = None

        for y, row in enumerate(map_data):
            for x, cell in enumerate(row):
                world_x = x * cell_width  # Базовая сетка, размеры объектов меняем отдельно
                world_y = y * cell_height
                # if world_y != screen_height:
                #     while True:
                #         if world_y == screen_height:
                #             break
                #         else:
                #             file = open("Easy.map", 'r+')
                #             l = len(file.readline())
                #             string = '.' * l
                #             file.write(string)
                #     file.close()
                if cell in platform_sizes:  # Вертикальные платформы
                    try:
                        width_percent, height_percent, platform_texture = platform_sizes[cell]
                        platform_width = int(cell_width * width_percent)
                        platform_height = int(cell_height * height_percent)
                        platform = Platform(world_x, world_y, platform_width, platform_height, platform_texture)
                        platforms_sprites.add(platform)
                        all_sprites.add(platform)
                    except Exception as e:
                        print(f"Ошибка при создании платформы: {e}")

                elif cell in ver_platform_sizes:  # Горизонтальные платформы
                    try:
                        width_percent, height_percent, ver_platform_texture = ver_platform_sizes[cell]
                        ver_platform_width = int(cell_width * width_percent)
                        ver_platform_height = int(cell_height * height_percent)
                        ver_platform = Platform_ver(world_x, world_y, ver_platform_height, ver_platform_width,
                                                    ver_platform_texture)
                        ver_platform_sprites.add(ver_platform)
                        all_sprites.add(ver_platform)
                    except Exception as e:
                        print(f"Ошибка при создании платформы: {e}")

                elif cell == 'g':  # Земля
                    ground_texture = random.choice(ground_textures)
                    ground_width, ground_height = ground_sizes.get(cell, (
                        cell_width, cell_height))
                    ground = Ground((world_x, screen_height - 50), pygame.image.load(ground_texture), ground_width, ground_height)
                    all_sprites.add(ground)

                elif cell in entity_sizes:
                    if cell in entity_sizes:
                        entity_width, entity_height, entity_texture = entity_sizes[cell]

                        # Создание существа в зависимости от типа
                        if cell == '@':  # Игрок
                            player = Hero(world_x, world_y, entity_width, entity_height)
                            all_sprites.add(player)

                        elif cell == 'w':  # Волк
                            wolf = Wolf(world_x, world_y, entity_width, entity_height, entity_texture, damage=200)
                            all_sprites.add(wolf)
                            enemy_sprites.add(wolf)

                        elif cell == 'o':  # Сова
                            owl = Owl(world_x, world_y, entity_width, entity_height, entity_texture, damage=150)
                            all_sprites.add(owl)
                            enemy_sprites.add(owl)

                        elif cell == 'c':
                            # print(f"Creating Coin at ({world_x}, {world_y}) with texture: {entity_texture}")
                            coin = Coin(world_x, world_y, entity_width, entity_height, entity_texture)
                            coins.add(coin)
                            all_sprites.add(coin)

        # Проверяем, найден ли игрок
        if player is None:
            raise ValueError("Ошибка: В файле карты отсутствует символ '@' для игрока!")

        if owl is None:
            raise ValueError("Ошибка: В файле карты отсутствует символ '@' для игрока!")

        return map_data, player, owl

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
