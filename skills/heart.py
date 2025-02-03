import pygame

from objects.entity.hero import Hero

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