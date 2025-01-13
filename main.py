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

tree_texture = pygame.image.load('data/tree.png')
tree_rect = tree_texture.get_rect()  # Получаем прямоугольник текстуры
tree_rect.topleft = (200, 400)  # Устанавливаем позицию дерева на карте

# Игрок
player_pos = [100, 500]
player_size = 50
player_speed = 7
is_jumping = False  # Состояние персонажа. False - в покое, True - в прыжке
jump_height = 10  # Максимальная высота прыжка
gravity = 0.5  # Сила тяжести
y_velocity = jump_height  # Начальная вертикальная скорость

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Основные механики передвижения
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    # if keys[pygame.K_UP]:
    #     player_pos[1] -= player_speed
    # if keys[pygame.K_DOWN]:
    #     player_pos[1] += player_speed

    # Прыжок
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            y_velocity = jump_height  # Начальная скорость прыжка
    else:
        # Обработка прыжка
        player_pos[1] -= y_velocity
        y_velocity -= gravity  # Применение силы тяжести

        # Проверка на приземление
        if player_pos[1] >= 500:  # Предполагаемая высота земли
            player_pos[1] = 500  # Приземляем персонажа на землю
            is_jumping = False  # Завершаем прыжок

    # Обновление экрана
    screen.fill((255, 255, 255))  # Заполняем экран белым цветом
    pygame.draw.rect(screen, (0, 0, 0), (*player_pos, player_size, player_size))  # Рисуем игрока

    # Отрисовка текстуры дерева
    screen.blit(tree_texture, tree_rect)  # Рисуем текстуру дерева на экране

    pygame.display.flip()
    pygame.time.Clock().tick(30)
