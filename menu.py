import pygame
import sys
from config import colors, WIDTH, HEIGHT
from main import f_level, s_level, two_players_1
# Инициализация Pygame
pygame.init()


# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пример меню с Pygame")

# Определение шрифта
font = pygame.font.Font(None, 36)


def draw_menu():
    screen.fill(colors["WHITE"])

    # Рисование кнопок
    pygame.draw.rect(screen, colors["RED"], (50, 50, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (50, 150, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (50, 250, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (50, 350, 300, 50))

    # Рисование текста на кнопках
    text_level1 = font.render("Level 1", True, colors["BLACK"])
    text_level2 = font.render("Level 2", True, colors["BLACK"])
    text_level3 = font.render("Level 3", True, colors["BLACK"])
    text_level_two_players = font.render("Two players", True, colors["BLACK"])

    screen.blit(text_level1, (170 - text_level1.get_width() // 2, 65))
    screen.blit(text_level2, (170 - text_level2.get_width() // 2, 165))
    screen.blit(text_level3, (170 - text_level3.get_width() // 2, 265))
    screen.blit(text_level_two_players, (170 - text_level_two_players.get_width() // 2, 365))


def menu():
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
                        f_level()
                    elif 150 < y < 200:
                        s_level()
                    elif 250 < y < 300:
                        two_players_1()
                    elif 350 < y < 400:
                        two_players_1()

        # Отрисовка меню
        draw_menu()

        # Обновление экрана
        pygame.display.flip()
    # Основной цикл программы

if __name__ == "__main__":
    menu()
