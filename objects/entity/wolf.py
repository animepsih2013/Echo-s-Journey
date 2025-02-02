import pygame
from settings import gravity
from settings import all_sprites
from settings import platforms_sprites

wolf_speed = 22

class Wolf(pygame.sprite.Sprite):
    def __init__(self, x, y, wolf_width, wolf_height, texture, damage):
        super().__init__(all_sprites)
        if texture:
            self.image = pygame.image.load(texture)
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color('red'))
        self.velocity_x = 0
        self.velocity_y = 0
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = damage

    def update(self):
        self.velocity_y += gravity
        if self.velocity_y > 10:  # Ограничиваем максимальную скорость падения
            self.velocity_y = 10
        self.velocity_x = -wolf_speed
        self.rect.x += self.velocity_x

        self.rect.y += self.velocity_y
        self.handle_collision_y()

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
