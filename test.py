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
platforms_sprites = pygame.sprite.Group()

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
        super().__init__(platforms_sprites, all_sprites)
        self.image = pygame.transform.scale(texture,
                                            (screen_width, texture.get_height()))  # Масштабируем траву по ширине экрана
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
        collision = pygame.sprite.spritecollideany(self, platforms_sprites)
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
        super().__init__(platforms_sprites, all_sprites)
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

class Platform_ver(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture=None):
        super().__init__()
        if texture:  # Если текстура задана
            self.image = pygame.image.load(texture).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))  # Масштабируем платформу
        else:  # Если текстура не задана, используем стандартное заполнение цветом
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color('red'))
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
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_x > 0:  # Движение вправо
                self.rect.right = platform.rect.left
            elif self.velocity_x < 0:  # Движение влево
                self.rect.left = platform.rect.right

    def handle_collision_y(self):
        # Проверяем столкновения по оси Y
        collided_platforms_sprites = pygame.sprite.spritecollide(self, platforms_sprites, False)
        for platform in collided_platforms_sprites:
            if self.velocity_y > 0:  # Падение вниз
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False
            elif self.velocity_y < 0:  # Прыжок вверх
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0


all_platforms = {}

# Словарь для размеров платформ
platform_sizes = {
    's': (0.1, 0.02),  # Маленькая платформа (длинна платформы, толщина платформы)
    'm': (0.2, 0.021),  # Средняя платформа (длинна платформы, толщина платформы)
    'b': (0.3, 0.02),  # Большая платформа (длинна платформы, толщина платформы)
}

ver_platform_sizes = {
    'v': (0.2, 0.02),  # Маленькая платформа (длинна платформы, толщина платформы)
}

def load_map_from_file(filename):
    try:
        with open(filename, 'r') as file:
            map_data = [line.strip() for line in file]

            # Определяем размеры одной ячейки карты в пикселях
            cell_width = screen_width / len(map_data[0])  # Ширина одной ячейки

            vertical_spacing = -0.01
            platform_count = 0  # Счетчик для уникальных имен платформ

            for y, row in enumerate(map_data):
                for x, cell in enumerate(row):
                    # Вычисляем координаты верхнего левого угла ячейки
                    world_x = x * cell_width

                    if cell in platform_sizes:
                        width_percent, height_percent = platform_sizes[cell]
                        platform_width = int(screen_width * width_percent)
                        platform_height = int(screen_height * height_percent)

                        # Добавляем контролируемый отступ между строками
                        world_y = y * (platform_height + vertical_spacing)

                        platform = Platform(world_x, world_y, platform_width, platform_height)
                        platforms_sprites.add(platform)
                        all_sprites.add(platform)

                        # Генерируем уникальное имя для платформы
                        platform_type = cell
                        platform_name = f"{platform_type}_platform_{platform_count}"
                        platform_count += 1

                        # Добавляем платформу в словарь с её координатами
                        all_platforms[platform_name] = (world_x, world_y)

                    if cell in ver_platform_sizes:
                        width_percent, height_percent = ver_platform_sizes[cell]
                        platform_width = int(screen_width * width_percent)
                        platform_height = int(screen_height * height_percent)

                        # Добавляем контролируемый отступ между строками
                        world_y = y * (platform_height + vertical_spacing)

                        ver_platform = Platform_ver(world_x, world_y, platform_height, platform_width)
                        platforms_sprites.add(ver_platform)
                        all_sprites.add(ver_platform)

                        # Генерируем уникальное имя для платформы
                        platform_type = cell
                        platform_name = f"{platform_type}_platform_{platform_count}"
                        platform_count += 1

                        # Добавляем платформу в словарь с её координатами
                        all_platforms[platform_name] = (world_x, world_y)

                    elif cell == '@':  # Игрок
                        player = Hero(world_x, world_y)
                        all_sprites.add(player)

        return map_data
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        sys.exit()


# Загружаем карту
map_file = "map.map"
map_data = load_map_from_file(map_file)

# Вывод платформ после загрузки
print(f"Всего платформ: {len(all_platforms)}")

# Создаём травяной слой внизу окна
grass = Grass((0, screen_height - grass_height * 0.5), grass_image)

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
