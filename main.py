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


def check_snake_head_positions(snake_1, snake_2):
    if snake_2.get_head_position() == snake_1.get_head_position():
        snake_1.reset()
        snake_2.reset()


def check_snake_position_with_walls(snake_1, walls, snake_2=None):
    for wall in walls:
        if wall.position == snake_1.get_head_position():
            snake_1.reset()
        if snake_2 is not None:
            if wall.position == snake_2.get_head_position():
                snake_2.reset()

# def check_snake_with_bad_food(snake, bad_food):
#     if bad_food


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
        snake_1.update(snake_2)
        snake_2.update(snake_1)
        check_snake_position_with_food(snake_1, food, poison)
        check_snake_position_with_food(snake_2, food, poison)
        check_and_spawn_poison(food, snake_1, poison)
        check_and_spawn_poison(food, snake_2, poison)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset()
        if snake_2.length <= 0:
            snake_2.reset()
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
    walls = [Wall() for i in range(6)]

    running = True

    while running:
        running = handle_events(snake_1, snake_2)
        snake_1.update(snake_2)
        snake_2.update(snake_1)
        check_snake_position_with_food(snake_1, food, poison, walls)
        check_snake_position_with_food(snake_2, food, poison, walls)
        check_and_spawn_poison(food, snake_1, poison, walls)
        check_and_spawn_poison(food, snake_2, poison, walls)
        check_snake_head_positions(snake_1, snake_2)
        check_snake_position_with_walls(snake_1=snake_1, snake_2=snake_2, walls=walls)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset()
        if snake_2.length <= 0:
            snake_2.reset()
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
    walls = [Wall() for i in range(15)]
    running = True

    while running:
        running = handle_events(snake_1, snake_2)
        snake_1.update(snake_2)
        snake_2.update(snake_1)
        check_snake_position_with_food(snake_1, food, poison, walls)
        check_snake_position_with_food(snake_2, food, poison, walls)
        check_and_spawn_poison(food, snake_1, poison, walls)
        check_and_spawn_poison(food, snake_2, poison, walls)
        check_snake_head_positions(snake_1, snake_2)
        check_snake_position_with_walls(snake_1=snake_1, snake_2=snake_2, walls=walls)
        show_score(screen=SCREEN, snake_1=snake_1, snake_2=snake_2)
        if snake_1.length <= 0:
            snake_1.reset()
        if snake_2.length <= 0:
            snake_2.reset()
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
        snake.update()
        check_snake_position_with_food(snake, food, poison)
        check_and_spawn_poison(food, snake, poison)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset()
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
    walls = [Wall() for i in range(6)]

    running = True

    while running:
        running = handle_events(snake)
        snake.update()

        check_and_spawn_poison(food, snake, poison, walls)
        check_snake_position_with_food(snake, food, poison, walls)
        check_snake_position_with_walls(snake_1=snake, walls=walls)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset()
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
    walls = [Wall() for i in range(15)]
    running = True
    while running:
        running = handle_events(snake)
        snake.update()

        check_and_spawn_poison(food, snake, poison, walls)
        check_snake_position_with_food(snake, food, poison, walls)
        check_snake_position_with_walls(snake_1=snake, walls=walls)
        show_score(screen=SCREEN, snake_1=snake)
        if snake.length <= 0:
            snake.reset()
        snake.render(SCREEN)
        food.render(SCREEN)
        poison.render(SCREEN)
        render_walls(walls, SCREEN)
        pygame.display.update()
        pygame.time.Clock().tick(20)

