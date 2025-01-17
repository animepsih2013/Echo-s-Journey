import pygame

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
grass_image = pygame.image.load("textures/ground.png")
grass_width, grass_height = grass_image.get_width(), grass_image.get_height()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

def crate_objects():
    from scripts.entity.hero import Hero
    from scripts.entity.wolf import Wolf
    from scripts.map_objects.platforms import Platform


    # Создаём игрока
    player = Hero(200, 200)
    all_sprites.add(player)

    wolf = Wolf((screen_width, screen_height - grass_height - 50))
    all_sprites.add(wolf)

    platforms.add(platform1, platform2, platform3, ground)
    all_sprites.add(platform1, platform2, platform3, ground)

crate_objects()