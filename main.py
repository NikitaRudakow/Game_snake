import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Класс для представления змеи
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE)) % WIDTH), (cur[1] + (y*GRIDSIZE)) % HEIGHT)
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
        self.color = RED
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
            pygame.draw.rect(surface, BLACK, rect, 1)

# Функция обработки событий
def handle_events(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction != DOWN:
                    snake.direction = UP
            elif event.key == pygame.K_DOWN:
                if snake.direction != UP:
                    snake.direction = DOWN
            elif event.key == pygame.K_LEFT:
                if snake.direction != RIGHT:
                    snake.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                if snake.direction != LEFT:
                    snake.direction = RIGHT

# Инициализация змеи и еды
snake = Snake()
food = Food()

# Основной цикл игры
while True:
    handle_events(snake)
    snake.update()

    # Проверка на столкновение с едой
    if snake.get_head_position() == food.position:
        snake.length += 1
        food.randomize_position()

    SCREEN.fill(BLACK)
    drawGrid(SCREEN)
    snake.render(SCREEN)
    food.render(SCREEN)

    pygame.display.update()
    pygame.time.Clock().tick(15)  # Устанавливаем скорость змейки
