import pygame
import random

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.99
ELASTICITY = 0.8
BG_COLOR = (0, 0, 0)
BALL_SPAWN_RATE = 10  # Number of frames between spawning new balls

# Random color generator
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bouncing Balls")
    clock = pygame.time.Clock()

    balls = []
    frame_count = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        # Add new ball at regular intervals
        if frame_count % BALL_SPAWN_RATE == 0:
            new_ball = Ball(
                random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS),
                random.randint(-SCREEN_HEIGHT, -BALL_RADIUS),
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random_color()
            )
            balls.append(new_ball)

        for ball in balls:
            ball.update()
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
