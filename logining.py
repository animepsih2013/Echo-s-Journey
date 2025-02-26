import pygame
import subprocess
import sys

pygame.init()
FPS = 50
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

fon = pygame.transform.scale(pygame.image.load('textures/avt.png'), (800, 800))
def terminate():
    pygame.quit()
    sys.exit()

screen.blit(fon, (0, 0))
font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)

button_surface = pygame.Surface((250, 70))
text = font.render("Никнейм", True, (0, 0, 0))
text_rect = text.get_rect(
    center=(button_surface.get_width() /2,
            button_surface.get_height()/2))
button_rect = pygame.Rect(140, 400, 250, 70)

button_surface2 = pygame.Surface((250, 70))
text2 = font.render("Пароль", True, (0, 0, 0))
text_rect2 = text2.get_rect(
    center=(button_surface2.get_width() /2,
            button_surface2.get_height()/2))
button_rect2 = pygame.Rect(400, 400, 250, 70)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Вызовите функцию on_mouse_button_down()
            if button_rect.collidepoint(event.pos):
                print("Button clicked!")
                subprocess.run(['python', 'main.py'])
                terminate()
            if button_rect2.collidepoint(event.pos):
                print("Button clicked!")
                subprocess.run(['python', 'main.py'])
                terminate()

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_surface, (127, 255, 212), (1, 1, 248, 68))
    else:
        pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 250, 70))
        pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 248, 68))
        pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 248, 1), 2)
        pygame.draw.rect(button_surface, (0, 100, 0), (1, 68, 248, 10), 2)

    if button_rect2.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_surface2, (127, 255, 212), (1, 1, 248, 68))
    else:
        pygame.draw.rect(button_surface2, (0, 0, 0), (0, 0, 250, 70))
        pygame.draw.rect(button_surface2, (255, 255, 255), (1, 1, 248, 68))
        pygame.draw.rect(button_surface2, (0, 0, 0), (1, 1, 248, 1), 2)
        pygame.draw.rect(button_surface2, (0, 100, 0), (1, 68, 248, 10), 2)

        # Показать текст кнопки
    button_surface.blit(text, text_rect)
    button_surface2.blit(text2, text_rect2)

    # Нарисуйте кнопку на экране
    screen.blit(button_surface, (button_rect.x, button_rect.y))
    screen.blit(button_surface2, (button_rect2.x, button_rect2.y))
    # Обновить состояние
    pygame.display.update()
