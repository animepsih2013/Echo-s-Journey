import random
import pygame

pygame.init()

# Глобальные параметры
player_speed = 7
jump_height = 20
gravity = 1


# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms_sprites = pygame.sprite.Group()


def main():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    print(f"Получено разрешение экрана: {screen_width}x{screen_height}")

    # Возвращаем значения для использования в других частях программы
    return screen_width, screen_height


screen_width, screen_height = main()

# Словарь для размеров платформ
platform_sizes = {
    's': (4, 0.3, "textures/l_platform"),   # Маленькая платформа (длинна платформы, толщина платформы)
    'm': (7, 0.3, "textures/l_platform"),  # Средняя платформа (длинна платформы, толщина платформы)
    'b': (9, 0.3, "textures/l_platform"),  # Большая платформа (длинна платформы, толщина платформы)
}

ver_platform_sizes = {
    'v': (60, 0.3),  # Маленькая платформа (длинна платформы, толщина платформы)
}
ground_sizes = {
    'g': (128, 64)  # Например, земля будет 128x64
}

entity_sizes = {
    '@': (100, 100, "textures/player"),  # Игрок 48x64
    'w': (190, 180, "textures/player"),  # Волк 80x64
    'o': (64, 64, "textures/player")   # Сова 64x64
}
