import pygame
import sys


def main():
    pygame.init()
    pygame.display.set_caption('Дота 2')
    size = 800, 600
    screen = pygame.display.set_mode(size)
    draw(screen)
    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def draw(screen):
    width, height = screen.get_size()
    screen.fill((0, 0, 0))

    font_size = 36
    font_path = "Neuropol.ttf"
    font = pygame.font.Font(font_path, font_size)
    text_color = (255, 0, 207)

    text = font.render("А ТЫ СИГМА???",True, text_color)

    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


if __name__ == '__main__':
    sys.exit(main())
