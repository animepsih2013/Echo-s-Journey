import pygame
import sys
import subprocess
import time

from settings import coins

from settings import all_sprites

from settings import screen_height, screen_width

from map_loader import load_map_from_file, Camera

from skills.heart import draw_health



def start_game():
    subprocess.run(['python', 'settings.py'])

record_time = ''
font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)
start_time = time.time()  # Время начала игры
score = 0  # Инициализация переменной score

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

def terminate():
    pygame.quit()
    sys.exit()

if len(sys.argv) > 1:
    argument = sys.argv[1]  # Первый аргумент после имени скрипта
    if argument == 'Easy':
        map_data = 'Easy.map'
    else:
        map_data = 'Nightmare.map'

    # Теперь передаем правильное имя файла в функцию
    map_data, player, owl = load_map_from_file(map_data)
    print(f"Переданный аргумент: {argument}")
else:
    print("Ошибка: Карта не загружена или не найден игрок!")
    sys.exit()

def get_score(value):
    global score
    score += value
    if score >= 1000:
        subprocess.run(['python', 'win_win.py'])
        terminate()

def draw_score(surface):
    global start_time
    current_time = time.time() - start_time  # Вычисляем прошедшее время
    total_time = int(current_time)  # Приводим к целому числу для отображения

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый цвет текста
    total_time_text = font.render(f"Current time: {total_time}", True, (255, 255, 255))

    surface.blit(score_text, (200, 20))
    surface.blit(total_time_text, (700, 20))

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
