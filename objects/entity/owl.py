import pygame
from settings import all_sprites
from settings import screen_width

owl_speed = 10


class Owl(pygame.sprite.Sprite):
    def __init__(self, x, y, owl_width, owl_height, texture, damage):
        super().__init__(all_sprites)
        # Загружаем анимации сразу и изменяем их размер
        self.bat_animation = [
            pygame.transform.scale(pygame.image.load('textures/bat_1.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_2.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_3.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_4.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_5.png').convert_alpha(), (150, 130)),
            pygame.transform.scale(pygame.image.load('textures/bat_6.png').convert_alpha(), (150, 130))
        ]

        self.frame_index = 0
        self.animation_speed = 120 # Скорость смены кадров (мс)
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления кадра

        self.image = self.bat_animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.damage = damage

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.bat_animation)
            self.image = self.bat_animation[self.frame_index]

    def update(self, *args):
        self.update_animation()
        self.velocity_x = -owl_speed
        self.rect.x += self.velocity_x
