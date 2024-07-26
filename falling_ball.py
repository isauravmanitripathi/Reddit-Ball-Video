import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.99
ELASTICITY = 0.8
BALL_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)

class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.vy += GRAVITY  # Apply gravity
        self.x += self.vx
        self.y += self.vy

        # Bounce off the floor
        if self.y + BALL_RADIUS > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - BALL_RADIUS
            self.vy = -self.vy * ELASTICITY
            self.vx *= FRICTION

        # Bounce off the walls
        if self.x + BALL_RADIUS > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - BALL_RADIUS
            self.vx = -self.vx * ELASTICITY
        elif self.x - BALL_RADIUS < 0:
            self.x = BALL_RADIUS
            self.vx = -self.vx * ELASTICITY

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bouncing Balls")
    clock = pygame.time.Clock()

    balls = [Ball(random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS),
                  random.randint(-SCREEN_HEIGHT, -BALL_RADIUS),
                  random.uniform(-5, 5),
                  random.uniform(-5, 5)) for _ in range(10)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        for ball in balls:
            ball.update()
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
