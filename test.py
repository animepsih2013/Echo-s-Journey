class Fireball:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, width, height)  # Пример создания прямоугольника
        self.fireball_animations = {0: animation_frame_1, 1: animation_frame_2}  # Пример анимаций
        self.frame_index = 0  # Начальный индекс

    def update(self):
        # Логика обновления фаербола
        self.frame_index = (self.frame_index + 1) % len(self.fireball_animations)
        try:
            self.image = self.fireball_animations[self.frame_index]
        except KeyError:
            print(f"Ошибка доступа к анимации: frame_index {self.frame_index} не существует.")
