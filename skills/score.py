import pygame
import sys
import sqlite3 as sq
import os
from settings import screen_height, screen_width
# Инициализация переменных
db = sq.connect(os.path.abspath('bd/login.db'))
cur = db.cursor()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)
score = 0
start_time = 0
game_over = False
total = 0


def terminate():
    sys.exit()
    pygame.quit()

def get_score(value):
    global score
    score += value
    if score >= 1000:
        display_victory_screen(screen)

def start_timer():
    global start_time
    start_time = pygame.time.get_ticks()  # Запоминаем время начала игры


def get_total_time():
    global start_time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Время в секундах
    return elapsed_time


def draw_score(surface):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый цвет текста
    total_time = get_total_time()
    total_time_text = font.render(f"Total Time: {total_time:.1f}s", True, (255, 255, 255))
    surface.blit(score_text, (200, 20))
    surface.blit(total_time_text, (700, 20))


def display_victory_screen(surface):
    global game_over
    global total
    game_over = True
    total_time = get_total_time()
    total = total_time
    print(total, type(total))
    put = '''INSERT INTO records(record)
                                        VALUES(?)'''
    cur.execute(put, [str(total)]).fetchall()
    db.commit()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Нажмите Enter для возврата на главный экран
                    pygame.quit()
                    sys.exit()

        surface.fill((0, 255, 0))
        victory_text = pygame.font.Font(None, 74).render("You Win!", True, (255, 255, 255))
        time_text = font.render(f"Time: {total_time:.1f} seconds", True, (255, 255, 255))
        restart_text = font.render("Press Enter to return to main menu", True, (255, 255, 255))

        surface.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, screen_height // 2 - 40))
        surface.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, screen_height // 2 + 10))
        surface.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 60))
        pygame.display.flip()


# Запуск таймера
start_timer()
