import pygame
import cv2

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("zxc GAme")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)

# Загрузка изображения сломанного автомата
arcade_machine_image = pygame.image.load('auto.png')  # Убедитесь, что путь к изображению правильный
arcade_machine_image = pygame.transform.scale(arcade_machine_image, (150, 250))  # Измените размер изображения при необходимости
arcade_machine_rect = pygame.Rect(300, 200, 150, 250)  # Прямоугольник для коллизий автомата

# Объекты окружения
walls = [
    pygame.Rect(50, 50, 700, 10),  # Верхняя стена
    pygame.Rect(50, 50, 10, 500),  # Левая стена
    pygame.Rect(740, 50, 10, 500),  # Правая стена
    pygame.Rect(50, 540, 700, 10),  # Нижняя стена
]

# Загрузка видео с помощью OpenCV
video_capture = cv2.VideoCapture('uuu.mp4')  # Укажите путь к вашему видео

# Персонаж
player = {
    "rect": pygame.Rect(100, 100, 90, 90),  # Прямоугольник для коллизий
    "speed": 5
}

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player["rect"].left > 0:
        player["rect"].move_ip(-player["speed"], 0)
    if keys[pygame.K_RIGHT] and player["rect"].right < WIDTH:
        player["rect"].move_ip(player["speed"], 0)
    if keys[pygame.K_UP] and player["rect"].top > 0:
        player["rect"].move_ip(0, -player["speed"])
    if keys[pygame.K_DOWN] and player["rect"].bottom < HEIGHT:
        player["rect"].move_ip(0, player["speed"])

    # Отрисовка окружения
    for wall in walls:
        pygame.draw.rect(screen, NEON_BLUE, wall)  # Стены

    # Отрисовка сломанного автомата
    screen.blit(arcade_machine_image, arcade_machine_rect)  # Отрисовка изображения автомата

    # Чтение кадра из видео
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Преобразование цвета из BGR в RGB
        frame = cv2.resize(frame, (90, 90))  # Изменение размера кадра под размер персонажа

        # Поворот кадра на 90 градусов по часовой стрелке
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        frame_surface = pygame.surfarray.make_surface(frame)  # Создание поверхности Pygame из массива NumPy
        screen.blit(frame_surface, player["rect"].topleft)  # Отрисовка видео на экран в позиции персонажа

    else:
        # Если кадры закончились, сбрасываем индекс на начало и перезапускаем видео
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Проверка взаимодействия с автоматом
    if player["rect"].colliderect(arcade_machine_rect):
        print("Вы нашли сломанный автомат!")

    pygame.display.flip()
    clock.tick(60)

# Освобождение ресурсов и выход
video_capture.release()
pygame.quit()
