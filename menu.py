import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Определение размеров экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пример меню с Pygame")

# Определение шрифта
font = pygame.font.Font(None, 36)


def draw_menu():
    screen.fill(WHITE)

    # Рисование кнопок
    pygame.draw.rect(screen, RED, (50, 50, 300, 50))
    pygame.draw.rect(screen, RED, (50, 150, 300, 50))
    pygame.draw.rect(screen, RED, (50, 250, 300, 50))
    pygame.draw.rect(screen, RED, (50, 350, 300, 50))

    # Рисование текста на кнопках
    text_play = font.render("Play", True, BLACK)
    text_quit = font.render("Quit", True, BLACK)
    text_option = font.render("Options", True, BLACK)
    text_highscore = font.render("Highscore", True, BLACK)

    screen.blit(text_play, (170 - text_play.get_width() // 2, 65))
    screen.blit(text_quit, (170 - text_quit.get_width() // 2, 165))
    screen.blit(text_option, (170 - text_option.get_width() // 2, 265))
    screen.blit(text_highscore, (170 - text_highscore.get_width() // 2, 365))


# Основной цикл программы
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Обработка нажатий на кнопки
            x, y = pygame.mouse.get_pos()
            if 50 < x < 350:
                if 50 < y < 100:
                    print("Play button pressed")
                elif 150 < y < 200:
                    print("Quit button pressed")
                elif 250 < y < 300:
                    print("Options button pressed")
                elif 350 < y < 400:
                    print("Highscore button pressed")

    # Отрисовка меню
    draw_menu()

    # Обновление экрана
    pygame.display.flip()
