import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, coin_width, coin_height, texture=None, damage=0):
        super().__init__()
        if texture:
            try:
                self.image = pygame.image.load(texture)
            except pygame.error as e:
                print(f"Unable to load texture: {texture}. Error: {e}")
                self.image = pygame.Surface((30, 30))
                self.image.fill(pygame.Color('red'))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(pygame.Color('red'))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()  # Удаляем монетку при сборе


# В основном цикле игры
coins = pygame.sprite.Group()

# Пример добавления монетки
if cell == 'c':
    coin = Coin(world_x, world_y, entity_width, entity_height, entity_texture)
    coins.add(coin)

# Отрисовка монеток на экране
screen.fill((0, 0, 0))  # Очистка экрана
coins.draw(screen)  # Отрисовка монеток
pygame.display.flip()