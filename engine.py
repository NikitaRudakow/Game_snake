import pygame
import sys
import random
from config import colors, WIDTH, HEIGHT, GRIDSIZE

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def save_to_txt(score, level, two_players):
    if two_players:
        file_name = "saves/save_level_" + str(level) + "_2_player.txt"
    else:
        file_name = "saves/save_level_" + str(level) + "_1_player.txt"
    with open(file_name, "a+", encoding="utf-8") as file:
        file.write(str(score) + "\n")


class Wall:
    def __init__(self):
        self.position = (0, 0)
        self.color = colors["GREY"]
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def render(self, surface):
        image = pygame.image.load('wall.webp')
        rect = pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE)
        scaled_image = pygame.transform.scale(image, (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))
        surface.blit(scaled_image, rect)


class Snake:
    def __init__(self, color):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.score = 1

    def get_head_position(self):
        return self.positions[0]

    def update(self, level, two_players=False, snake2=None):
        cur = self.get_head_position()
        x, y = self.direction

        self.score += 1
        new = (((cur[0] + (x * GRIDSIZE)) % WIDTH), (cur[1] + (y * GRIDSIZE)) % HEIGHT)
        if snake2 is not None:
            if len(self.positions) > 2 and new in self.positions[2:] or new in snake2.positions[2:]:
                self.reset(level, two_players)
            elif new == snake2.positions[0]:
                self.reset(level, two_players)
                snake2.reset(level, two_players)
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()
        else:
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.reset(level, two_players)
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()

    def reset(self, level, two_players):
        if self.length > 1:
            save_to_txt(self.length, level, two_players)
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(p[0], p[1], GRIDSIZE, GRIDSIZE))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = colors["RED"]
        self.randomize_position()
        self.countPlusHp = 1

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRIDSIZE) - 1) * GRIDSIZE,
                         random.randint(0, (HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def render(self, surface, is_golden_apple=False):
        if self.countPlusHp > 1:
            image = pygame.image.load('gold_apple.png')
        elif self.countPlusHp < 0:
            image = pygame.image.load('poison.png')
        else:
            image = pygame.image.load('apple.png')
        rect = pygame.Rect(self.position[0], self.position[1], GRIDSIZE, GRIDSIZE)
        scaled_image = pygame.transform.scale(image, (GRIDSIZE, GRIDSIZE))
        surface.blit(scaled_image, rect)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def drawGrid(surface):
    for y in range(0, HEIGHT, GRIDSIZE):
        for x in range(0, WIDTH, GRIDSIZE):
            rect = pygame.Rect(x, y, GRIDSIZE, GRIDSIZE)


def handle_events(snake_1, snake_2=None):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
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
    return running


def show_score(screen, snake_1, snake_2=None):
    screen.fill(colors["BLACK"])
    drawGrid(screen)
    font = pygame.font.Font(None, 30)
    score_text1 = font.render("Score:" + str(snake_1.length), 1, snake_1.color)
    screen.blit(score_text1, (0, 0))
    if snake_2 is not None:
        score_text2 = font.render("Score:" + str(snake_2.length), 1, snake_2.color)
        screen.blit(score_text2, (710, 0))


def render_walls(walls, screen):
    for wall in walls:
        wall.render(screen)


def randomize_position_walls(walls):
    for wall in walls:
        wall.randomize_position()


def check_snake_position_with_walls(snake_1, walls, level, two_players=False, snake_2=None):
    for wall in walls:
        if wall.position == snake_1.get_head_position():
            snake_1.reset(level, two_players)
        if snake_2 is not None:
            if wall.position == snake_2.get_head_position():
                snake_2.reset(level, two_players)


def spawn_food(food, walls, occupied_field):
    while True:
        food.randomize_position()
        if food.position == occupied_field.position:
            continue
        if walls is not None:
            for wall in walls:
                if food.position != wall.position:
                    continue
            else:
                return
        else:
            return


def check_snake_position_with_food(snake, food, poison, walls=None):
    if snake.get_head_position() == food.position:
        snake.length += food.countPlusHp

        if walls is not None:
            randomize_position_walls(walls)
        spawn_food(poison, walls, food)
        spawn_food(food, walls, poison)

        random_number = random.randint(0, 3)
        if 1 == random_number:
            food.countPlusHp = random.randint(1, 5)
        else:
            food.countPlusHp = 1


def check_and_spawn_poison(food, snake, poison, walls=None):
    if snake.get_head_position() == poison.position:
        snake.length += poison.countPlusHp
        spawn_food(food=poison, occupied_field=food, walls=walls)
        poison.countPlusHp = random.randint(-5, -1)


def two_players_1():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    poison = Food()
    running = True
    poison.countPlusHp = -1
    while running:
        running = handle_events(snake_1, snake_2)
        snake_1.update(snake2=snake_2, two_players=True, level=1)
        snake_2.update(snake2=snake_1, two_players=True, level=1)
        check_snake_position_with_food(snake_1, food, poison)
        check_snake_position_with_food(snake_2, food, poison)
        check_and_spawn_poison(food, snake_1, poison)
        check_and_spawn_poison(food, snake_2, poison)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset(1, True)
        if snake_2.length <= 0:
            snake_2.reset(1, True)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(10)


def two_players_2():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    poison = Food()
    poison.countPlusHp = -1
    walls = [Wall() for i in range(3)]

    running = True

    while running:
        running = handle_events(snake_1, snake_2)
        snake_1.update(snake2=snake_2, two_players=True, level=2)
        snake_2.update(snake2=snake_1, two_players=True, level=2)
        check_snake_position_with_food(snake_1, food, poison, walls)
        check_snake_position_with_food(snake_2, food, poison, walls)
        check_and_spawn_poison(food, snake_1, poison, walls)
        check_and_spawn_poison(food, snake_2, poison, walls)
        check_snake_position_with_walls(snake_1=snake_1, snake_2=snake_2, level=2, two_players=True, walls=walls)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset(2, True)
        if snake_2.length <= 0:
            snake_2.reset(2, True)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        render_walls(walls=walls, screen=SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(15)


def two_players_3():
    snake_1 = Snake(colors["WHITE"])
    snake_2 = Snake(colors["PINK"])
    food = Food()
    poison = Food()
    poison.countPlusHp = -1
    walls = [Wall() for i in range(7)]
    running = True

    while running:
        running = handle_events(snake_1, snake_2)
        snake_1.update(snake2=snake_2, two_players=True, level=3)
        snake_2.update(snake2=snake_1, two_players=True, level=3)
        check_snake_position_with_food(snake_1, food, poison, walls)
        check_snake_position_with_food(snake_2, food, poison, walls)
        check_and_spawn_poison(food, snake_1, poison, walls)
        check_and_spawn_poison(food, snake_2, poison, walls)
        check_snake_position_with_walls(snake_1=snake_1, snake_2=snake_2, level=3, two_players=True, walls=walls)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset(3, True)
        if snake_2.length <= 0:
            snake_2.reset(3, True)
        snake_1.render(SCREEN)
        snake_2.render(SCREEN)
        render_walls(walls, SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(15)


def f_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    poison = Food()
    poison.countPlusHp = -1
    running = True
    while running:
        running = handle_events(snake)
        snake.update(level=1, two_players=False)
        check_snake_position_with_food(snake, food, poison)
        check_and_spawn_poison(food, snake, poison)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset(1, False)
        snake.render(SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(10)


def s_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    poison = Food()
    poison.countPlusHp = -1
    walls = [Wall() for i in range(3)]

    running = True

    while running:
        running = handle_events(snake)
        snake.update(level=2, two_players=False)

        check_and_spawn_poison(food, snake, poison, walls)
        check_snake_position_with_food(snake, food, poison, walls)
        check_snake_position_with_walls(snake_1=snake, level=2, walls=walls, two_players=False)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset(2, False)
        snake.render(SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        render_walls(walls, SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(15)


def t_level():
    snake = Snake(colors["GREEN"])
    food = Food()
    poison = Food()
    poison.countPlusHp = -1
    walls = [Wall() for i in range(7)]
    running = True
    while running:
        running = handle_events(snake)
        snake.update(level=3, two_players=False)

        check_and_spawn_poison(food, snake, poison, walls)
        check_snake_position_with_food(snake, food, poison, walls)
        check_snake_position_with_walls(snake_1=snake, level=3, walls=walls, two_players=False)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset(3, False)
        snake.render(SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        render_walls(walls, SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(20)
