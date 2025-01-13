import pygame
import sys

# Инициализация Pygame
pygame.init()

# Получение текущего разрешения экрана
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Создание полноэкранного окна
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Echo's Journey")

# Загрузка изображения фона
background_image = pygame.image.load("textures/font.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Настройки земли
ground_y = screen_height - 65  # Короче координата земли, переделай так чтоб вместо координат границей была текстурка

# Игрок
player_size = 50
player_pos = [100, ground_y - player_size]  # Позиция игрока поверх земли
player_speed = 7

# Прыжок
is_jumping = False
jump_height = 10
gravity = 0.5
y_velocity = jump_height

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Основные механики передвижения
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] = max(player_pos[0] - player_speed, 0)  # Ограничение по левому краю
    if keys[pygame.K_d]:
        player_pos[0] = min(player_pos[0] + player_speed, screen_width - player_size)  # Ограничение по правому краю

    # Прыжок
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            y_velocity = jump_height  # Начальная скорость прыжка
    else:
        # Обработка прыжка
        player_pos[1] -= y_velocity
        y_velocity -= gravity

        # Проверка на приземление
        if player_pos[1] >= ground_y - player_size:
            player_pos[1] = ground_y - player_size
            is_jumping = False

    # Отображение изображения на экране
    screen.blit(background_image, (0, 0))  # Рисуем фон

    # Рисуем игрока поверх фона
    pygame.draw.rect(screen, (0, 0, 0), (*player_pos, player_size, player_size))  # Черный квадрат

    # Обновляем экран
    pygame.display.flip()
    pygame.time.Clock().tick(30)
