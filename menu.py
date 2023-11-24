import pygame
import sys
from config import colors, WIDTH, HEIGHT
from main import f_level, s_level, two_players_1, two_players_2
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
    pygame.draw.rect(screen, colors["RED"], (50, 250, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (50, 150, 300, 50))

    pygame.draw.rect(screen, colors["RED"], (400, 50, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (400, 150, 300, 50))
    pygame.draw.rect(screen, colors["RED"], (400, 250, 300, 50))

    # Рисование текста на кнопках
    text_level1 = font.render("Level 1", True, colors["BLACK"])
    text_level2 = font.render("Level 2", True, colors["BLACK"])
    text_level3 = font.render("Level 3", True, colors["BLACK"])
    text_one_player = font.render("One player", True, colors["BLACK"])
    text_level_two_players = font.render("Two players", True, colors["BLACK"])

    screen.blit(text_one_player, (125, 20))
    screen.blit(text_level_two_players, (480, 20))
    screen.blit(text_level1, (150, 65))
    screen.blit(text_level1, (510, 65))
    screen.blit(text_level2, (150, 165))
    screen.blit(text_level2, (510, 165))
    screen.blit(text_level3, (150, 265))
    screen.blit(text_level3, (510, 265))


def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатий на кнопки
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if 50 < x < 350:
                    if 50 < y < 100:
                        f_level()
                    elif 150 < y < 200:
                        s_level()
                    elif 250 < y < 300:
                        two_players_1()
                elif 400 < x < 700:
                    if 50 < y < 100:
                        two_players_1()
                    elif 150 < y < 200:
                        two_players_2()
                    elif 250 < y < 300:
                        two_players_2()


        # Отрисовка меню
        draw_menu()

        # Обновление экрана
        pygame.display.flip()
    # Основной цикл программы

if __name__ == "__main__":
    menu()
