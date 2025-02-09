import sys
import sqlite3 as sq
import pygame
import subprocess
import os
from line_edit import LineEdit
from text import Text

db = sq.connect(os.path.abspath('bd/login.db'))
cur = db.cursor()

pygame.init()
FPS = 50
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

fon = pygame.transform.scale(pygame.image.load('textures/avt.png'), (800, 800))
screen.blit(fon, (0, 0))
font = pygame.font.Font(None, 30)

login_edit = LineEdit(300, 200, 200, 50, font)
comments = pygame.Surface((1920, 1080))

button = pygame.Surface((250, 70))
text = font.render("Easy", True, (0, 0, 0))
text_rect = text.get_rect(
    center=(button.get_width() / 2,
            button.get_height() / 2))
button_rect = pygame.Rect(250, 500, 250, 70)


def terminate():
    pygame.quit()
    sys.exit()



def req():
    keys = pygame.key.get_pressed()
    a = login_edit.return_text()
    if keys[pygame.K_SPACE]:
        search = "SELECT record FROM records WHERE user_name = ?"
        answer = cur.execute(search, (a,)).fetchall()
        db.commit()
        if len(answer) == 0:
            return ''
        else:
            return answer[0][0]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                subprocess.run(['python', 'screen_load.py'])
                terminate()
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(button, (127, 255, 212), (1, 1, 248, 68))
        else:
            pygame.draw.rect(button, (0, 0, 0), (0, 0, 250, 70))
            pygame.draw.rect(button, (255, 255, 255), (1, 1, 248, 68))
            pygame.draw.rect(button, (0, 0, 0), (1, 1, 248, 1), 2)
            pygame.draw.rect(button, (0, 100, 0), (1, 68, 248, 10), 2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            Text(font_size=40).render(screen, f'Рекорд: {req()}', (300, 400))
        button.blit(text, text_rect)
        login_edit.handle_event(event)

    screen.blit(button, (button_rect.x, button_rect.y))
    login_edit.draw(screen)
    pygame.display.update()
