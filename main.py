import pygame
import sys
import subprocess

from settings import all_sprites, platforms_sprites

from settings import screen_height, screen_width

from map_loader import load_map_from_file, Camera

def start_game():
    subprocess.run(['python', 'settings.py'])


# Инициализация Pygame
pygame.init()

# Запуск настроек игры
start_game()

# Создание полноэкранного окна
screen = pygame.display.set_mode((5000, 5000), pygame.FULLSCREEN)
pygame.display.set_caption("Echo's Journey")

# Загрузка изображения фона
background_image = pygame.image.load("textures/forest_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Загружаем карту
map_file = "LvL1.map"
map_data, player = load_map_from_file(map_file)

if map_data is None or player is None:
    print("Ошибка: Карта не загружена или не найден игрок!")
    sys.exit()


# Главный игровой цикл
clock = pygame.time.Clock()
running = True
camera = Camera()

# Главный игровой цикл
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:  # Закрываем игру нажатием escape
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновляем камеру относительно игрока
    camera.update(player)

    # Отображение изображения на экране
    screen.blit(background_image, (0, 0))  # Рисуем фон

    # Применяем камеру ко всем спрайтам
    for sprite in all_sprites:
        camera.apply(sprite)

    # Обновляем и рисуем все спрайты
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(70)
