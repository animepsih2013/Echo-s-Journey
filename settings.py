import pygame

pygame.init()

# Глобальные параметры
player_speed = 7
jump_height = 20
gravity = 1
INVINCIBLE_TIME = 2000

# Группы спрайтов
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
platforms_sprites = pygame.sprite.Group()
ver_platform_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
fireballs = pygame.sprite.Group()

def main():
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h

    print(f"Получено разрешение экрана: {screen_width}x{screen_height}")

    # Возвращаем значения для использования в других частях программы
    return screen_width, screen_height


screen_width, screen_height = main()



# Словарь для размеров платформ
platform_sizes = {
    's': (4, 0.3, "textures/s_platform.png"),  # Маленькая платформа (длинна платформы, толщина платформы)
    'm': (6.7, 0.3, "textures/m_platform.png"),  # Средняя платформа (длинна платформы, толщина платформы)
    'b': (9, 0.3, "textures/b_platform.png"),  # Большая платформа (длинна платформы, толщина платформы)
}

ver_platform_sizes = {
    'v': (9, 1.1, "textures/ledder.png"),
    'n': (4, 1.1, "textures/ledder.png"),
}
ground_sizes = {
    'g': (16, 16)  # Например, земля будет 128x64
}

entity_sizes = {
    '@': (200, 200, ""), # Игрок
    'w': (80, 64, "textures/wolf.png"), # Волк
    'o': (64, 64, "textures/owl.png"), # Сова
    'c': (30, 30, ""),
}
