import pygame

pygame.init()
# Получение текущего разрешения экрана
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Создание полноэкранного окна
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Echo's Journey")

# Загрузка изображения фона
background_image = pygame.image.load("textures/font.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Масштабируем фон под экран

# Настройки земли
ground_y = screen_height - 65  # Короче координата земли, переделай так чтоб вместо координат границей была текстурка

# Игрок
# player_size = 50
# player_pos = [100, ground_y - player_size]  # Позиция игрока поверх земли
# player_speed = 7

# Прыжок
is_jumping = False
jump_height = 10
gravity = 0.5
y_velocity = jump_height

clock = pygame.time.Clock()


class Platform(pygame.sprite.Sprite):
    size = (100, 10)

    def __init__(self, pos):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(all_sprites)
        # добавляем в группу платформ
        self.add(platforms)
        self.image = pygame.Surface(Platform.size)
        self.image.fill(pygame.Color("gray"))
        self.rect = (pos, Platform.size)


class Ladder(pygame.sprite.Sprite):
    size = (10, 100)

    def __init__(self, pos):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(all_sprites)
        # добавляем в группу платформ
        self.add(ladders)
        self.image = pygame.Surface(Ladder.size)
        self.image.fill(pygame.Color("red"))
        self.rect = (pos, Ladder.size)


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(all_sprites)
        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color("blue"))
        self.rect = pygame.Rect(pos, (20, 20))

    def update(self):
        if pygame.sprite.spritecollideany(self, platforms) is None and pygame.sprite.spritecollideany(self,
                                                                                                      ladders) is None:
            self.rect.top += 1


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

# группа, содержащая все платформы
platforms = pygame.sprite.Group()

# группа, содержащая все лесенки
ladders = pygame.sprite.Group()

hero = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Ladder(event.pos)
                else:
                    Platform(event.pos)
            if event.button == 3:
                if hero is None:
                    hero = Hero(event.pos)
                else:
                    hero.rect.topleft = event.pos
                    # если персонаж создан
        if hero is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.rect.left -= 10
                if event.key == pygame.K_d:
                    hero.rect.left += 10
                if pygame.sprite.spritecollideany(hero, ladders) is not None:
                    if event.key == pygame.K_w:
                        hero.rect.top -= 10
                    if event.key == pygame.K_s:
                        hero.rect.bottom += 10
                if not is_jumping:
                    if event.key == pygame.K_SPACE:
                        is_jumping = True
                        y_velocity = jump_height  # Начальная скорость прыжка
                else:
                    # Обработка прыжка
                    hero.rect.top -= y_velocity
                    y_velocity -= gravity

                    # Проверка на приземление
                    if hero.rect.bottom >= ground_y - hero.rect.size[1]:
                        hero.rect.bottom = ground_y - hero.rect.size[1]
                        is_jumping = False

        # Отображение изображения на экране
        screen.blit(background_image, (0, 0))  # Рисуем фон
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        pygame.time.Clock().tick(120)
