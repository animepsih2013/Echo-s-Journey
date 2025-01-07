import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo's Journey")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Игрок
player_pos = [100, 500]
player_size = 50
player_speed = 5

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    # if keys[pygame.K_UP]:
    #     player_pos[1] -= player_speed
    # if keys[pygame.K_DOWN]:
    #     player_pos[1] += player_speed

    # Обновление экрана
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (*player_pos, player_size, player_size))
    pygame.display.flip()
    pygame.time.Clock().tick(30)
