import pygame
import sys
import random
from config import colors, WIDTH, HEIGHT
# Инициализация Pygame
pygame.init()

# Параметры экран
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета


class Wall:
    def __init__(self):
        self.position = (0, 0)
        self.color = colors["GREY"]
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))
# Класс для представления змеи
class Snake:
    def __init__(self, color):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self, snake2=None):
        cur = self.get_head_position()
        x, y = self.direction
        self.score += 1
        new = (((cur[0] + (x*GRIDSIZE)) % WIDTH), (cur[1] + (y*GRIDSIZE)) % HEIGHT)
        if snake2 is not None:
            if len(self.positions) > 2 and new in self.positions[2:] or new in snake2.positions[2:]:
                self.reset()
            elif new == snake2.positions[0]:
                self.reset()
                snake2.reset()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()
        else:
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.reset()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(p[0], p[1], GRIDSIZE, GRIDSIZE))

# Класс для представления еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = colors["RED"]
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH//GRIDSIZE)-1) * GRIDSIZE,
                         random.randint(0, (HEIGHT//GRIDSIZE)-1) * GRIDSIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Размер ячейки сетки
GRIDSIZE = 20

# Функция отрисовки сетки
def drawGrid(surface):
    for y in range(0, HEIGHT, GRIDSIZE):
        for x in range(0, WIDTH, GRIDSIZE):
            rect = pygame.Rect(x, y, GRIDSIZE, GRIDSIZE)
            pygame.draw.rect(surface, colors["BLACK"], rect, 1)

# Функция обработки событий
def handle_events(snake_1, snake_2=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake_1.direction != DOWN:
                    snake_1.direction = UP
            if event.key == pygame.K_DOWN:
                if snake_1.direction != UP:
                    snake_1.direction = DOWN
            if event.key == pygame.K_LEFT:
                if snake_1.direction != RIGHT:
                    snake_1.direction = LEFT
            if event.key == pygame.K_RIGHT:
                if snake_1.direction != LEFT:
                    snake_1.direction = RIGHT
            if snake_2 is not None:
                if event.key == pygame.K_w:
                    if snake_2.direction != DOWN:
                        snake_2.direction = UP
                if event.key == pygame.K_s:
                    if snake_2.direction != UP:
                        snake_2.direction = DOWN
                if event.key == pygame.K_a:
                    if snake_2.direction != RIGHT:
                        snake_2.direction = LEFT
                if event.key == pygame.K_d:
                    if snake_2.direction != LEFT:
                        snake_2.direction = RIGHT

# Инициализация змеи и еды

#
# # Основной цикл игры
# while True:
#     handle_events(snake_1, snake_2)
#     snake_1.update(snake_2)
#     snake_2.update(snake_1)
#
#     # Проверка на столкновение с едой
#     if snake_1.get_head_position() == food.position:
#         snake_1.length += 1
#         food.randomize_position()
#         wall.randomize_position()
#
#     if snake_2.get_head_position() == food.position:
#         snake_2.length += 1
#         food.randomize_position()
#         wall.randomize_position()
#     # if snake_2.get_head_position() == snake_1.get_head_position():
#     #     snake_1.reset()
#
#     if snake_1.get_head_position() == wall.position:
#         snake_1.reset()
#     if snake_2.get_head_position() == wall.position:
#         snake_2.reset()
#
#     SCREEN.fill(BLACK)
#     drawGrid(SCREEN)
#     snake_1.render(SCREEN)
#     snake_2.render(SCREEN)
#     food.render(SCREEN)
#     wall.render(SCREEN)
#
#     pygame.display.update()
#     pygame.time.Clock().tick(10) # Устанавливаем скорость змейки


def f_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    while True:
        handle_events(snake)
        snake.update()

        # Проверка на столкновение с едой
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        SCREEN.fill(colors["BLACK"])
        drawGrid(SCREEN)
        snake.render(SCREEN)
        food.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(10)  # Устанавливаем скорость змейки


def s_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    wall = Wall()
    while True:
        handle_events(snake)
        snake.update()

        # Проверка на столкновение с едой
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        SCREEN.fill(colors["BLACK"])
        drawGrid(SCREEN)
        snake.render(SCREEN)
        food.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(10)


# Отрисовка счета
# font = pygame.font.Font(None, 36)
# text = font.render(f"Счет: {score}", True, WHITE)
# screen.blit(text, (10, 10))
#
# # Для обновления счета (например, когда змейка съедает еду), увеличьте score на 1:
# if snake[0] == food:
#     score += 1