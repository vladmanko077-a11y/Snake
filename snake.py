import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 500, 500
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Vlad")
clock = pygame.time.Clock()

# 🎨 Кольори
BG_COLOR = (20, 20, 30)
GRID_COLOR = (40, 40, 55)
FOOD_COLOR = (255, 90, 90)
TEXT_COLOR = (220, 220, 255)

font_big = pygame.font.SysFont(None, 72)
font_small = pygame.font.SysFont(None, 36)

def reset_game():
    snake = [(200, 200)]
    direction = (CELL, 0)
    food = (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )
    score = 0
    speed = 8  # комфортна стартова швидкість
    game_over = False
    return snake, direction, food, score, speed, game_over

snake, direction, food, score, speed, game_over = reset_game()

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

# Меню
def show_menu():
    screen.fill(BG_COLOR)
    title = font_big.render("SNAKE ", True, (0, 255, 200))
    play_text = font_small.render("Press SPACE to Play", True, TEXT_COLOR)
    exit_text = font_small.render("Press ESC to Exit", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
    screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2))
    screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 40))
    pygame.display.update()

# Плавне тіло та поворот голови
def draw_snake(snake, direction):
    for i, (x, y) in enumerate(snake):
        green = max(50, 255 - i * 8)
        blue = max(80, 200 - i * 6)
        color = (0, green, blue)
        # Плавне "гойдання"
        offset = 2 * math.sin(pygame.time.get_ticks()/200 + i)
        # Голова — овал із напрямком
        if i == 0:
            head_rect = pygame.Rect(x+offset, y+offset, CELL-2, CELL-2)
            if direction[0] > 0:   # вправо
                pygame.draw.ellipse(screen, color, head_rect)
            elif direction[0] < 0: # вліво
                pygame.draw.ellipse(screen, color, head_rect)
            elif direction[1] > 0: # вниз
                pygame.draw.ellipse(screen, color, head_rect)
            elif direction[1] < 0: # вверх
                pygame.draw.ellipse(screen, color, head_rect)
        else:
            pygame.draw.rect(screen, color,
                             (x+offset, y+offset, CELL-2, CELL-2),
                             border_radius=6)

in_menu = True
running = True

while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if in_menu:
        show_menu()
        if keys[pygame.K_SPACE]:
            in_menu = False
            snake, direction, food, score, speed, game_over = reset_game()
        if keys[pygame.K_ESCAPE]:
            running = False
        continue

    if not game_over:
        if keys[pygame.K_UP] and direction != (0, CELL):
            direction = (0, -CELL)
        if keys[pygame.K_DOWN] and direction != (0, -CELL):
            direction = (0, CELL)
        if keys[pygame.K_LEFT] and direction != (CELL, 0):
            direction = (-CELL, 0)
        if keys[pygame.K_RIGHT] and direction != (-CELL, 0):
            direction = (CELL, 0)

        head = (snake[0][0] + direction[0],
                snake[0][1] + direction[1])

        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            game_over = True
        if head in snake:
            game_over = True

        snake.insert(0, head)

        if head == food:
            score += 1
            speed += 0.3  # плавне прискорення
            food = (
                random.randrange(0, WIDTH, CELL),
                random.randrange(0, HEIGHT, CELL)
            )
        else:
            snake.pop()
    else:
        if keys[pygame.K_r]:
            snake, direction, food, score, speed, game_over = reset_game()

    # Малювання
    screen.fill(BG_COLOR)
    draw_grid()
    pygame.draw.rect(screen, FOOD_COLOR,
                     (food[0], food[1], CELL, CELL),
                     border_radius=6)
    draw_snake(snake, direction)

    score_text = font_small.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text1 = font_big.render("GAME OVER", True, (255, 80, 80))
        text2 = font_small.render("Press R to Restart", True, TEXT_COLOR)
        screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 60))
        screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 10))

    pygame.display.update()

pygame.quit()