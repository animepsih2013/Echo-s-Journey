import pygame
import subprocess
import sys

pygame.init()
FPS = 50
screen = pygame.display.set_mode((950, 633))
clock = pygame.time.Clock()

fon = pygame.transform.scale(pygame.image.load('textures/sc.png'), (950, 633))
def terminate():
    pygame.quit()
    sys.exit()

screen.blit(fon, (0, 0))
intro_text = ["ЗАСТАВКА", "",
              "Правила игры",
              "Если в правилах несколько строк,",
              "приходится выводить их построчно"]

font = pygame.font.Font(None, 30)
text_coord = 50
for line in intro_text:
    string_rendered = font.render(line, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.top = text_coord
    intro_rect.x = 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            subprocess.run(['python', 'main.py'])

    pygame.display.flip()
    clock.tick(FPS)