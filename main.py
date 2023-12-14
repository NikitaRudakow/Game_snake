import pygame
import sys
from config import colors, WIDTH, HEIGHT
from engine import f_level, s_level, two_players_1, two_players_2, t_level, two_players_3

pygame.init()

background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Определение шрифта
font = pygame.font.Font(None, 36)
def get_record(level, game_mode):
    path = "saves/save_level_" + str(level) + "_" + str(game_mode) + "_player.txt"
    data_int_list = [0]
    try:
        with open(path, "r") as file:
            data_int_list = [int(x) for x in (file.read()).split()]
    except FileNotFoundError:
        return 0
    return max(data_int_list)

def draw_menu():
    screen.blit(background, (0, 0))

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

    font_for_number = pygame.font.Font(None, 50)
    number_1 = font_for_number.render("1", True, colors["BLACK"])
    number_2 = font_for_number.render("2", True, colors["BLACK"])
    number_3 = font_for_number.render("3", True, colors["BLACK"])
    text_one_player = font.render("One player", True, colors["BLACK"])
    text_level_two_players = font.render("Two players", True, colors["BLACK"])
    record_for_1_1 = font.render(str(get_record(1,1)), True, colors["BLACK"])
    record_for_2_1 = font.render(str(get_record(2, 1)), True, colors["BLACK"])
    record_for_3_1 = font.render(str(get_record(3, 1)), True, colors["BLACK"])
    record_for_1_2 = font.render(str(get_record(1, 2)), True, colors["BLACK"])
    record_for_2_2 = font.render(str(get_record(2, 2)), True, colors["BLACK"])
    record_for_3_2 = font.render(str(get_record(3, 2)), True, colors["BLACK"])

    screen.blit(text_one_player, (125, 20))
    screen.blit(text_level_two_players, (480, 20))
    screen.blit(text_level1, (150, 65))
    screen.blit(text_level1, (510, 65))
    screen.blit(text_level2, (150, 165))
    screen.blit(text_level2, (510, 165))
    screen.blit(text_level3, (150, 265))
    screen.blit(text_level3, (510, 265))
    screen.blit(number_1, (367, 345))
    screen.blit(number_2, (367, 397))
    screen.blit(number_3, (367, 449))
    screen.blit(record_for_1_1, (55, 355))
    screen.blit(record_for_2_1, (55, 405))
    screen.blit(record_for_3_1, (55, 455))
    screen.blit(record_for_1_2, (407, 355))
    screen.blit(record_for_2_2, (407, 405))
    screen.blit(record_for_3_2, (407, 455))


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
                        t_level()
                elif 400 < x < 700:
                    if 50 < y < 100:
                        two_players_1()
                    elif 150 < y < 200:
                        two_players_2()
                    elif 250 < y < 300:
                        two_players_3()

        draw_menu()

        pygame.display.flip()

if __name__ == "__main__":
    menu()
