import sys
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

