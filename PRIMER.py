import pygame

# Инициализация Pygame
pygame.init()

# Размер окна
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пример фона с изображением")

# Загрузка изображения фона
background_image = pygame.image.load("data/font.png")

# Масштабирование изображения под размер экрана (если необходимо)
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображение изображения на экране
    screen.blit(background_image, (0, 0))

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
