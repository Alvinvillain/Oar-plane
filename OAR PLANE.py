import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 700
PLANE_SIZE = 30
GRAVITY = 1
JUMP_STRENGTH = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Import fonts
pygame.font.init()

# Font settings
FONT = pygame.font.SysFont("calibri", 50)

# Player class
class Plane:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = random.randint(0, HEIGHT // 2)  # Random initial vertical position within the top half
        self.velocity_y = 0
        self.velocity_x = 0
        self.color = BLUE
        self.score = 0

    def jump(self):
        self.velocity_y = -JUMP_STRENGTH

    def move_up(self):
        self.velocity_y = -0.5

    def move_down(self):
        if self.y < HEIGHT - PLANE_SIZE:
            self.velocity_y = 0.5
        else:
            self.velocity_y = 0  # Stop downward movement

    def move_left(self):
        self.velocity_x = -10

    def move_right(self):
        self.velocity_x = 10

    def stop_horizontal_movement(self):
        self.velocity_x = 0

    def update(self):
        self.y += self.velocity_y
        self.x += self.velocity_x

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - PLANE_SIZE:
            self.y = HEIGHT - PLANE_SIZE

        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - PLANE_SIZE:
            self.x = WIDTH - PLANE_SIZE

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, int(self.y), PLANE_SIZE, PLANE_SIZE))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -30
        self.width = 30
        self.height = random.randint(50, 150)
        self.color = GREEN

    def update(self, speed):
        self.y += speed

    def off_screen(self):
        return self.y > HEIGHT

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, int(self.y), self.width, self.height))

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    plane = Plane()
    obstacles = []

    game_over = False
    speed_increase_time = time.time() + 5
    speed = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    plane.jump()
                elif event.key == pygame.K_UP and not game_over:
                    plane.move_up()
                elif event.key == pygame.K_DOWN and not game_over:
                    plane.move_down()
                elif event.key == pygame.K_LEFT and not game_over:
                    plane.move_left()
                elif event.key == pygame.K_RIGHT and not game_over:
                    plane.move_right()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    plane.stop_horizontal_movement()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 <= event.pos[1] <= HEIGHT // 2 + 50:
                    plane = Plane()
                    obstacles = []
                    game_over = False
                    speed_increase_time = time.time() + 5

        if not game_over:
            plane.update()

            if time.time() >= speed_increase_time:
                speed += 1
                speed_increase_time = time.time() + 5

            if random.randint(1, 100) == 1:
                obstacles.append(Obstacle())

            for obstacle in obstacles:
                obstacle.update(speed)

            obstacles = [obstacle for obstacle in obstacles if not obstacle.off_screen()]

            for obstacle in obstacles:
                if (
                    plane.x < obstacle.x + obstacle.width
                    and plane.x + PLANE_SIZE > obstacle.x
                    and plane.y < obstacle.y + obstacle.height
                    and plane.y + PLANE_SIZE > obstacle.y
                ):
                    game_over = True

            plane.score += 1

            surface.fill((0, 0, 0))
            plane.render(surface)

            for obstacle in obstacles:
                obstacle.render(surface)

            score_text = FONT.render(f"Score: {plane.score}", True, WHITE)
            surface.blit(score_text, (10, 10))

        if game_over:
            game_over_text = FONT.render("Game Over", True, WHITE)
            surface.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
            score_text = FONT.render(f"Score: {plane.score}", True, WHITE)
            surface.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 + 50))

            new_game_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
            pygame.draw.rect(surface, WHITE, new_game_button_rect, 2)
            new_game_text = FONT.render("New Game", True, WHITE)
            surface.blit(new_game_text, (new_game_button_rect.centerx - new_game_text.get_width() // 2, HEIGHT // 2))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
