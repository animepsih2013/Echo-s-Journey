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
background_image = pygame.image.load("textures/forest_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Загрузка текстуры травы
grass_image = pygame.image.load("textures/grass.png")
grass_image = pygame.transform.scale(grass_image, (200, 90))  # Масштабируем текстуру травы под размер платформы

# Глобальные параметры
player_speed = 7
jump_height = 15
gravity = 1

# Спрайт платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size, texture=None):
        super().__init__(platforms, all_sprites)
        if texture:
            self.image = pygame.transform.scale(texture, size)
        else:
            self.image = pygame.Surface(size)
            self.image.fill(pygame.Color("gray"))
        self.rect = pygame.Rect(pos, size)


# Спрайт персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("blue"))
        self.rect = self.image.get_rect(topleft=pos)
        self.y_velocity = 0
        self.is_jumping = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Горизонтальное движение
        if keys[pygame.K_a]:
            self.rect.x -= player_speed
        if keys[pygame.K_d]:
            self.rect.x += player_speed

        # Прыжок
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.y_velocity = -jump_height

        # Применение гравитации
        self.y_velocity += gravity
        self.rect.y += self.y_velocity

        # Проверка на платформы
        if pygame.sprite.spritecollideany(self, platforms):
            self.rect.y -= self.y_velocity  # Отмена падения
            self.y_velocity = 0
            self.is_jumping = False

        # Ограничение движения по вертикали (не падаем ниже экрана)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.is_jumping = False
            self.y_velocity = 0


# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
grass_sprite = pygame.sprite.Group()

# Создаём платформы и траву
Platform((100, screen_height - 100), (300, 20))  # Серая платформа
Platform((500, screen_height - 200), (200, 20))  # Серая платформа
Platform((800, screen_height - 300), (300, 20))  # Серая платформа



# Главный игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Отображение изображения на экране
    screen.blit(background_image, (0, 0))  # Рисуем фон

    # Обновляем и рисуем все спрайты
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)