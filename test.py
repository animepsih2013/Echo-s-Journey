import pygame
from objects.entity.hero import Hero
from objects.entity.wolf import Wolf

# Инициализация Pygame
pygame.init()

# Определение цвета
GREEN = (0, 255, 0)

# Определение размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Определение класса для сердечек
class Heart(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

def draw_health(player):
    heart_full = pygame.image.load('textures/heart_full.png').convert_alpha()  # Полное сердечко
    heart_half = pygame.image.load('textures/heart_half.png').convert_alpha()  # Половинка сердечка
    heart_empty = pygame.image.load('textures/heart_empty.png').convert_alpha()  # Пустое сердечко

    hearts = []
    total_hearts = player.max_health // 100
    current_hearts = player.health // 100
    half_heart = (player.health % 100) >= 50

    # Добавление полных сердечек
    for _ in range(current_hearts):
        hearts.append(Heart(heart_full, (20 + len(hearts) * 40, 20)))

    # Добавление половинки сердечка
    if half_heart:
        hearts.append(Heart(heart_half, (20 + len(hearts) * 40, 20)))

    # Добавление пустых сердечек
    empty_hearts_count = total_hearts - len(hearts)
    for _ in range(empty_hearts_count):
        hearts.append(Heart(heart_empty, (20 + len(hearts) * 40, 20)))

    return hearts

# Основной игровой цикл
running = True
player = Hero(x=100, y=100, player_width=50, player_height=50, texture=None)  # Передаем параметры в Hero

# Создание группы волков для примера
wolf_group = pygame.sprite.Group()
wolf_group.add(Wolf(x=400, y=100, wolf_width=50, wolf_height=50, texture=None, damage=10))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заполнение экрана белым цветом
    screen.fill((255, 255, 255))

    # Обновляем игрока и волков
    player.update()
    wolf_group.update()

    # Проверка столкновений с волками и обновление здоровья игрока
    player.HP()

    # Рисуем здоровье на экране
    health_hearts = draw_health(player)
    for heart in health_hearts:
        screen.blit(heart.image, heart.rect.topleft)

    # Рисуем игрока и волков на экране (не забудьте добавить методы для их отрисовки)
    screen.blit(player.image, player.rect.topleft)
    for wolf in wolf_group:
        screen.blit(wolf.image, wolf.rect.topleft)

    # Обновляем экран
    pygame.display.flip()

pygame.quit()
