import pygame
import sys
import random
from config import colors, WIDTH, HEIGHT, GRIDSIZE

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load('background.jpg')

SCREEN.blit(background, (0, 0))
pygame.display.set_caption("Змейка")


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
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
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
        self.countPlusHp = 1

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Размер ячейки сетки


# Функция отрисовки сетки
def drawGrid(surface):
    for y in range(0, HEIGHT, GRIDSIZE):
        for x in range(0, WIDTH, GRIDSIZE):
            rect = pygame.Rect(x, y, GRIDSIZE, GRIDSIZE)
            # pygame.draw.rect(surface, colors["BLACK"], rect, 1)


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
            elif event.key == pygame.K_DOWN:
                if snake_1.direction != UP:
                    snake_1.direction = DOWN
            elif event.key == pygame.K_LEFT:
                if snake_1.direction != RIGHT:
                    snake_1.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                if snake_1.direction != LEFT:
                    snake_1.direction = RIGHT
            if snake_2 is not None:
                if event.key == pygame.K_w:
                    if snake_2.direction != DOWN:
                        snake_2.direction = UP
                elif event.key == pygame.K_s:
                    if snake_2.direction != UP:
                        snake_2.direction = DOWN
                elif event.key == pygame.K_a:
                    if snake_2.direction != RIGHT:
                        snake_2.direction = LEFT
                elif event.key == pygame.K_d:
                    if snake_2.direction != LEFT:
                        snake_2.direction = RIGHT


def show_score(screen, snake_1, snake_2=None):
    screen.fill(colors["BLACK"])
    drawGrid(screen)
    font = pygame.font.Font(None, 30)
    score_text1 = font.render("Score:" + str(snake_1.length), 1, snake_1.color)
    screen.blit(score_text1, (0, 0))
    if snake_2 is not None:
        score_text2 = font.render("Score:" + str(snake_2.length), 1, snake_2.color)
        screen.blit(score_text2, (710, 0))


def two_players_1():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    # Основной цикл игры
    while True:
        handle_events(snake_1, snake_2)
        snake_1.update(snake_2)
        snake_2.update(snake_1)

        if snake_1.get_head_position() == food.position:
            snake_1.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]

        if snake_2.get_head_position() == food.position:
            snake_2.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]

        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        food.render(SCREEN)

        pygame.display.update()
        pygame.time.Clock().tick(10)


def two_players_2():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    wall1 = Wall()
    wall2 = Wall()
    wall3 = Wall()
    # Основной цикл игры
    while True:
        handle_events(snake_1, snake_2)
        snake_1.update(snake_2)
        snake_2.update(snake_1)
        # Проверка на столкновение с едой
        if snake_1.get_head_position() == food.position:
            snake_1.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()

        if snake_2.get_head_position() == food.position:
            snake_2.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()

        if snake_2.get_head_position() == snake_1.get_head_position():
            snake_1.reset()

        if snake_1.get_head_position() == wall1.position or snake_1.get_head_position() == wall2.position or snake_1.get_head_position() == wall3.position:
            snake_1.reset()
        if snake_2.get_head_position() == wall1.position or snake_2.get_head_position() == wall2.position or snake_2.get_head_position() == wall3.position:
            snake_2.reset()

        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        wall1.render(SCREEN)
        wall2.render(SCREEN)
        wall3.render(SCREEN)
        food.render(SCREEN)
        # wall.render(SCREEN)

        pygame.display.update()
        pygame.time.Clock().tick(15)  # Устанавливаем скорость змейки


def two_players_3():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    wall1 = Wall()
    wall2 = Wall()
    wall3 = Wall()
    wall4 = Wall()
    wall5 = Wall()
    wall6 = Wall()
    wall7 = Wall()
    # Основной цикл игры
    while True:
        handle_events(snake_1, snake_2)
        snake_1.update(snake_2)
        snake_2.update(snake_1)
        # Проверка на столкновение с едой
        if snake_1.get_head_position() == food.position:
            snake_1.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()
            wall4.randomize_position()
            wall5.randomize_position()
            wall6.randomize_position()
            wall7.randomize_position()

        if snake_2.get_head_position() == food.position:
            snake_2.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()
            wall4.randomize_position()
            wall5.randomize_position()
            wall6.randomize_position()
            wall7.randomize_position()

        if snake_2.get_head_position() == snake_1.get_head_position():
            snake_1.reset()

        if snake_1.get_head_position() == wall1.position or snake_1.get_head_position() == wall2.position or snake_1.get_head_position() == wall3.position or snake_1.get_head_position() == wall4.position or snake_1.get_head_position() == wall5.position or snake_1.get_head_position() == wall6.position or snake_1.get_head_position() == wall7.position:
            snake_1.reset()
        if snake_2.get_head_position() == wall1.position or snake_2.get_head_position() == wall2.position or snake_2.get_head_position() == wall3.position or snake_2.get_head_position() == wall4.position or snake_2.get_head_position() == wall5.position or snake_2.get_head_position() == wall6.position or snake_2.get_head_position() == wall7.position:
            snake_2.reset()

        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        wall1.render(SCREEN)
        wall2.render(SCREEN)
        wall3.render(SCREEN)
        wall4.render(SCREEN)
        wall5.render(SCREEN)
        wall6.render(SCREEN)
        wall7.render(SCREEN)
        food.render(SCREEN)
        # wall.render(SCREEN)

        pygame.display.update()
        pygame.time.Clock().tick(15)  # Устанавливаем скорость змейки


def f_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    while True:
        handle_events(snake)
        snake.update()

        # Проверка на столкновение с едой
        if snake.get_head_position() == food.position:
            snake.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]

        show_score(screen=SCREEN, snake_1=snake)
        snake.render(SCREEN)
        food.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(10)  # Устанавливаем скорость змейки


def s_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    wall1 = Wall()
    wall2 = Wall()
    wall3 = Wall()
    while True:
        handle_events(snake)
        snake.update()

        if snake.get_head_position() == food.position:
            snake.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()

        if snake.get_head_position() == wall1.position or snake.get_head_position() == wall2.position or snake.get_head_position() == wall3.position:
            snake.reset()
        show_score(screen=SCREEN, snake_1=snake)
        snake.render(SCREEN)
        food.render(SCREEN)
        wall1.render(SCREEN)
        wall2.render(SCREEN)
        wall3.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(15)


def t_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    wall1 = Wall()
    wall2 = Wall()
    wall3 = Wall()
    wall4 = Wall()
    wall5 = Wall()
    wall6 = Wall()
    wall7 = Wall()

    while True:
        handle_events(snake)
        snake.update()

        if snake.get_head_position() == food.position:
            snake.length += food.countPlusHp
            food.randomize_position()
            random_list = [0, 1, 3]
            if 1 == random.choice(random_list):
                food.countPlusHp = random.randint(2, 5)
                food.color = colors["GOLD"]
            else:
                food.countPlusHp = 1
                food.color = colors["RED"]
            wall1.randomize_position()
            wall2.randomize_position()
            wall3.randomize_position()
            wall4.randomize_position()
            wall5.randomize_position()
            wall6.randomize_position()
            wall7.randomize_position()

        if snake.get_head_position() == wall1.position or snake.get_head_position() == wall2.position or snake.get_head_position() == wall3.position or snake.get_head_position() == wall4.position or snake.get_head_position() == wall5.position or snake.get_head_position() == wall6.position or snake.get_head_position() == wall7.position:
            snake.reset()
        show_score(screen=SCREEN, snake_1=snake)

        snake.render(SCREEN)
        food.render(SCREEN)
        wall1.render(SCREEN)
        wall2.render(SCREEN)
        wall3.render(SCREEN)
        wall4.render(SCREEN)
        wall5.render(SCREEN)
        wall6.render(SCREEN)
        wall7.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(20)
