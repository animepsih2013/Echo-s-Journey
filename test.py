import pygame
from pygame.locals import QUIT

# Инициализация Pygame
pygame.init()

# Создаем экран
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

# Настройка шрифта
font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)

def draw_score(surface, score):
    # Создаем текстовую поверхность
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый цвет текста
    # Рисуем текст на переданной поверхности
    surface.blit(score_text, (10, 10))  # Здесь surface - это объект pygame.Surface

# Переменная для счета
score = 0

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Обновление логики игры здесь...
    score += 1  # Для примера увеличиваем счет каждую итерацию

    # Заполнение экрана черным цветом
    screen.fill((0, 0, 0))

    # Вызов функции для рисования счета
    draw_score(screen, score)  # Передаем экран как поверхность

    # Обновляем экран
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
