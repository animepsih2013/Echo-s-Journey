import pygame
import sys

from settings import all_sprites, platforms_sprites
from settings import screen_height, screen_width

from objects.entity.hero import Hero
from objects.entity.wolf import Wolf

from objects.stucturies.platforms import Platform
from objects.stucturies.platforms import Platform_ver
from objects.stucturies.grass import Ground

# Загрузка текстуры травы
ground_image = pygame.image.load("textures/ground.png")

# Словарь для размеров платформ
platform_sizes = {
    's': (0.1, 0.02),  # Маленькая платформа (длинна платформы, толщина платформы)
    'm': (0.2, 0.021),  # Средняя платформа (длинна платформы, толщина платформы)
    'b': (0.3, 0.02),  # Большая платформа (длинна платформы, толщина платформы)
}

ver_platform_sizes = {
    'v': (0.06, 0.02),  # Маленькая платформа (длинна платформы, толщина платформы)
}


def load_map_from_file(filename):
    try:
        with open(filename, 'r') as file:
            global cell_width

            map_data = [line.strip() for line in file]

            # Определяем размеры одной ячейки карты в пикселях
            cell_width = screen_width / len(map_data[0])  # Ширина одной ячейки

            vertical_spacing = -0.01
            platform_count = 0  # Счетчик для уникальных имен платформ

            for y, row in enumerate(map_data):
                for x, cell in enumerate(row):
                    # Вычисляем координаты верхнего левого угла ячейки
                    world_x = x * cell_width

                    if cell == 'g':
                        ground = Ground((world_x, world_y), ground_image)
                        all_sprites.add(ground)

                    if cell in platform_sizes:
                        width_percent, height_percent = platform_sizes[cell]
                        platform_width = int(screen_width * width_percent)
                        platform_height = int(screen_height * height_percent)

                        # Добавляем контролируемый отступ между строками
                        world_y = y * (platform_height + vertical_spacing)

                        platform = Platform(world_x, world_y, platform_width, platform_height)
                        platforms_sprites.add(platform)
                        all_sprites.add(platform)

                        # Генерируем уникальное имя для платформы
                        platform_type = cell
                        platform_name = f"{platform_type}_platform_{platform_count}"
                        platform_count += 1

                    if cell in ver_platform_sizes:
                        width_percent, height_percent = ver_platform_sizes[cell]
                        platform_width = int(screen_width * width_percent)
                        platform_height = int(screen_height * height_percent)

                        # Добавляем контролируемый отступ между строками
                        world_y = y * (platform_height + vertical_spacing)

                        ver_platform = Platform_ver(world_x, world_y, platform_height, platform_width)
                        # platforms_sprites.add(ver_platform)
                        all_sprites.add(ver_platform)

                    elif cell == '@':  # Игрок
                        global player
                        player = Hero(world_x, world_y)
                        all_sprites.add(player)

                    elif cell == 'w':  # Волк
                        wolf = Wolf(world_x, world_y)
                        all_sprites.add(wolf)

        return map_data, player
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        sys.exit()


class Camera:
    def __init__(self):
        self.dx = 0  # Горизонтальное смещение
        self.dy = 0  # Вертикальное смещение

    def apply(self, obj):
        obj.rect.x += self.dx


    def update(self, target):
        self.dx = -(target.rect.centerx - screen_width // 2)