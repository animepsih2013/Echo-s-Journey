import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Получение текущего разрешения экрана
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Создание полноэкранного окна
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Echo's Journey")

# Загрузка изображения фона
background_image = pygame.image.load("textures/forest_background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Загрузка текстуры травы
grass_image = pygame.image.load("textures/grass.png")
grass_width, grass_height = grass_image.get_width(), grass_image.get_height()

# Глобальные параметры
player_speed = 7
jump_height = 20
gravity = 1

# Класс травы (нижней платформы)
class Grass(pygame.sprite.Sprite):
    def __init__(self, pos, texture):
        super().__init__(platforms, all_sprites)
        self.image = pygame.transform.scale(texture, (screen_width, texture.get_height()))  # Масштабируем траву по ширине экрана
        self.rect = self.image.get_rect(topleft=pos)

class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = -random.randint(4, 5)
        self.vy = random.randrange(3, 8)
        self.y_velocity = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        collision = pygame.sprite.spritecollideany(self, platforms)
        if collision:
            # Если герой падает вниз и касается платформы
            if self.rect.bottom <= collision.rect.bottom:
                self.rect.bottom = collision.rect.top  # Останавливаем персонажа на платформе
                self.y_velocity = 0

        # Ограничение движения по вертикали (не падаем ниже экрана)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.y_velocity = 0


# Класс травы (нижней платформы)
class Grass(pygame.sprite.Sprite):
    def __init__(self, pos, texture):
        super().__init__(platforms, all_sprites)
        self.image = pygame.transform.scale(texture, (screen_width, texture.get_height()))
        self.rect = self.image.get_rect(topleft=pos)

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture=None):
        super().__init__()
        if texture:  # Если текстура задана
            self.image = pygame.image.load(texture).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))  # Масштабируем платформу
        else:  # Если текстура не задана, используем стандартное заполнение цветом
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect(topleft=(x, y))


# Класс персонажа
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_x = 0  # Скорость по оси X
        self.velocity_y = 0  # Скорость по оси Y
        self.is_jumping = False

    def update(self):
        # Гравитация
        self.velocity_y += gravity
        if self.velocity_y > 10:  # Ограничиваем максимальную скорость падения
            self.velocity_y = 10

        # Горизонтальное движение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Движение влево
            self.velocity_x = -player_speed
        elif keys[pygame.K_d]:  # Движение вправо
            self.velocity_x = player_speed
        else:
            self.velocity_x = 0

        # Прыжок
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = -jump_height
            self.is_jumping = True

        # Обновление позиции
        self.rect.x += self.velocity_x
        self.handle_collision_x()  # Проверка столкновений по X

        self.rect.y += self.velocity_y
        self.handle_collision_y()  # Проверка столкновений по Y

    def handle_collision_x(self):
        # Проверяем столкновения по оси X
        collided_platforms = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collided_platforms:
            if self.velocity_x > 0:  # Движение вправо
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  # Движение влево
                self.rect.left = platform.rect.right

    def handle_collision_y(self):
        # Проверяем столкновения по оси Y
        collided_platforms = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collided_platforms:
            if self.velocity_y > 0:  # Падение вниз
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            elif self.velocity_y < 0:  # Прыжок вверх
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0


# Словарь для размеров платформ
platform_sizes = {
    '1': (0.1, 0.015),  # Маленькая платформа (10% ширины экрана, 2% высоты экрана)
    '2': (0.2, 0.025),  # Средняя платформа (20% ширины экрана, 5% высоты экрана)
    '3': (0.3, 0.035),  # Большая платформа (30% ширины экрана, 7% высоты экрана)
}

# Загрузка карты и инициализация объектов с учетом точек
def load_map_from_file(filename, air_size=(0, 0)):
    try:
        with open(filename, 'r') as file:
            map_data = [line.strip() for line in file]

            # Распаковываем размеры пустоты (air_size)
            air_width_percent, air_height_percent = air_size
            global player
            for y, row in enumerate(map_data):
                for x, cell in enumerate(row):
                    # Масштабируем координаты с учетом размера экрана и промежутков
                    world_x = int(x * (screen_width / len(row)) + air_width_percent * screen_width)
                    world_y = int(y * (screen_height / len(map_data)) + air_height_percent * screen_height)

                    # Создаем объекты карты
                    if cell in platform_sizes:
                        width_percent, height_percent = platform_sizes[cell]
                        platform_width = int(screen_width * width_percent)
                        platform_height = int(screen_height * height_percent)
                        platform = Platform(world_x, world_y, platform_width, platform_height)
                        platforms.add(platform)
                        all_sprites.add(platform)


                    elif cell == '@':  # Игрок
                        # Фиксированное место спавна игрока
                        spawn_x = int(screen_width * 0.1)  # Например, 10% от ширины экрана
                        spawn_y = int(screen_height * 0.8)  # Например, 80% от высоты экрана
                        player = Hero(spawn_x, spawn_y)
                        all_sprites.add(player)

        return map_data
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        sys.exit()

map_file = "map.map"
map_data = load_map_from_file(map_file, air_size=(-0.09, 0.05))  # Смещение 2% по ширине и 3% по высоте



# Создаём травяной слой внизу окна
grass = Grass((0, screen_height - grass_height), grass_image)

wolf = Wolf((screen_width, screen_height - 50))

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
