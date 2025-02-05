import pygame
import sys
import subprocess

from settings import coins, score

from settings import all_sprites

from settings import screen_height, screen_width

from map_loader import load_map_from_file, Camera

from skills.heart import draw_health
from objects.stucturies.coins import draw_score


def start_game():
    subprocess.run(['python', 'settings.py'])


# Инициализация Pygame
pygame.init()

# Запуск настроек игры
start_game()

# Создание полноэкранного окна
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Echo's Journey")

# Загрузка изображения фона
background_image = pygame.image.load("textures/forest_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Загружаем карту+
map_file = "LvL1.map"
map_data, player, owl = load_map_from_file(map_file)

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

    player_position = (player.rect.centerx, player.rect.centery)
    owl.update(player)

    # Обновляем камеру относительно игрока
    camera.update(player)

    coins.update(player)
    coins.draw(screen)

    # Отображение изображения на экране
    screen.blit(background_image, (0, 0))  # Рисуем фон

    # Применяем камеру ко всем спрайтам
    for sprite in all_sprites:
        camera.apply(sprite)

    # Обновляем и рисуем все спрайты
    all_sprites.update(player)
    all_sprites.draw(screen)

    player.HP()
    player.update_animation()

    score_counter = draw_score(screen)

    # Рисуем здоровье на экране
    health_hearts = draw_health(player)
    for heart in health_hearts:
        screen.blit(heart.image, heart.rect.topleft)

    pygame.display.flip()
    clock.tick(70)
