import pygame
import subprocess
import sys
from settings import screen_height, screen_width


screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)

screen.fill((0, 0, 0))  # Очистка экрана

# Отображение изображения или анимации победы
victory_text = font.render("You Win!", True, (255, 255, 255))
next_button_text = font.render("Next Level", True, (255, 255, 255))

screen.blit(victory_text, (350, 250))
screen.blit(next_button_text, (350, 350))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Обработка нажатия кнопки "Next"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 350 <= mouse_x <= 450 and 350 <= mouse_y <= 400:
            if event.type == pygame.MOUSEBUTTONDOWN:
                subprocess.run(['python', 'screen_load.py'])
        pygame.display.flip()  # Обновление экрана