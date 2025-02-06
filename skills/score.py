import pygame

total_time = ''
font = pygame.font.Font("textures/ofont.ru_Press Start 2P.ttf", 40)
score = 0

def get_score(value):
    global score
    score += value

def draw_score(surface):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый цвет текста
    total_score_text = font.render(f"Total_score: {total_time}", True, (255, 255, 255))
    surface.blit(score_text, (200, 20))
    surface.blit(total_score_text, (700, 20))



