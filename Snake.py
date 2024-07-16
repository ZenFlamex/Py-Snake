import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1080, 720
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game states
MENU = 0
RUNNING = 1
GAME_OVER = 2
PAUSED = 3

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % WIDTH), (cur[1] + (y*GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    return PAUSED
        return RUNNING

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    state = MENU
    high_score = load_high_score()

    while True:
        screen.fill(BLACK)

        if state == MENU:
            draw_text(screen, "Press SPACE to Play", 36, GREEN, WIDTH//2, HEIGHT//2)
            draw_text(screen, f"High Score: {high_score}", 24, WHITE, WIDTH//2, HEIGHT//2 + 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Transition to RUNNING state when SPACE key is pressed
                        state = RUNNING

        elif state == RUNNING:
            result = snake.handle_keys()
            if result == PAUSED:
                state = PAUSED
            elif not snake.move():
                if snake.score > high_score:
                    high_score = snake.score
                    save_high_score(high_score)
                state = GAME_OVER
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                food.randomize_position()
            snake.draw(screen)
            food.draw(screen)
            draw_text(screen, f"Score: {snake.score}", 24, GREEN, 100, 10)
            pygame.display.update()
            clock.tick(10)

        elif state == GAME_OVER:
            draw_text(screen, "Game Over! Press SPACE to Play Again", 36, RED, WIDTH//2, HEIGHT//2)
            draw_text(screen, f"Your Score: {snake.score}", 24, RED, WIDTH//2, HEIGHT//2 + 50)
            draw_text(screen, f"High Score: {high_score}", 24, WHITE, WIDTH//2, HEIGHT//2 + 100)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        state = RUNNING

        elif state == PAUSED:
            draw_text(screen, "Paused. Press ESC to Resume", 36, WHITE, WIDTH//2, HEIGHT//2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = RUNNING

if __name__ == "__main__":
    main()
