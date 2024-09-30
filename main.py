import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Попадание в кирпичи")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Скорость кадров
FPS = 60

# Параметры платформы
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7

# Параметры мяча
BALL_RADIUS = 10
BALL_SPEED = 5

# Параметры кирпичей
BRICK_COLORS = [RED, BLUE, GREEN]
BRICK_TYPES = [(100, 20), (80, 25), (120, 15), (60, 30), (90, 18)]

# Шрифт
font = pygame.font.SysFont('Arial', 30)


# Класс платформы
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


# Класс мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = random.choice([BALL_SPEED, -BALL_SPEED])
        self.speed_y = -BALL_SPEED

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x

        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, RED, (self.rect.centerx, self.rect.centery), BALL_RADIUS)

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.speed_x = random.choice([BALL_SPEED, -BALL_SPEED])
        self.speed_y = -BALL_SPEED


# Класс кирпичей
class Brick:
    def __init__(self):
        width, height = random.choice(BRICK_TYPES)
        self.rect = pygame.Rect(random.randint(0, WIDTH - width), random.randint(50, HEIGHT - 200), width, height)
        self.color = random.choice(BRICK_COLORS)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# Класс игры
class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.misses = 0
        self.running = True
        self.generate_brick()

    def generate_brick(self):
        self.bricks.append(Brick())

    def check_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y = -self.ball.speed_y

        for brick in self.bricks:
            if self.ball.rect.colliderect(brick.rect):
                self.bricks.remove(brick)
                self.score += 1
                self.ball.speed_y = -self.ball.speed_y
                self.generate_brick()
                break

        if self.ball.rect.bottom >= HEIGHT:
            self.misses += 1
            self.ball.reset()
            self.generate_brick()

        if self.misses >= 3:
            self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PADDLE_SPEED
        self.paddle.move(dx)
        self.ball.move()
        self.check_collision()

    def draw(self):
        screen.fill(BLACK)
        self.paddle.draw()
        self.ball.draw()
        for brick in self.bricks:
            brick.draw()

        # Отображение счета и промахов
        score_text = font.render(f'Очки: {self.score}', True, WHITE)
        misses_text = font.render(f'Промахи: {self.misses}/3', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(misses_text, (10, 40))

        pygame.display.flip()


def draw_start_screen():
    screen.fill(BLACK)
    title_text = font.render("Попадание в кирпичи", True, WHITE)
    start_text = font.render("Нажмите любую клавишу для старта", True, WHITE)
    rules_text = font.render("Правила: Попадите мячиком в кирпичи", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(rules_text, (WIDTH // 2 - rules_text.get_width() // 2, HEIGHT // 2))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()


def draw_game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render(f'Игра окончена! Ваши очки: {score}', True, WHITE)
    restart_text = font.render("Нажмите R, чтобы начать заново, или Q для выхода", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    in_start_menu = True
    in_game_over = False
    game = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if in_start_menu:
            draw_start_screen()
            keys = pygame.key.get_pressed()
            if any(keys):
                in_start_menu = False
                game = Game()

        elif in_game_over:
            draw_game_over_screen(game.score)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                in_game_over = False
                game = Game()
            if keys[pygame.K_q]:
                pygame.quit()
                return

        else:
            if game.running:
                game.update()
                game.draw()
            else:
                in_game_over = True

        clock.tick(FPS)


if __name__ == "__main__":
    main()
