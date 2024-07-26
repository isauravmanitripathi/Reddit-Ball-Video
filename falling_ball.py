import pygame
import random
import time
import subprocess
from moviepy.editor import ImageSequenceClip, AudioFileClip
import sys

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.99
ELASTICITY = 0.8
BG_COLOR = (0, 0, 0)
BALL_SPAWN_RATE = 10  # Number of frames between spawning new balls
FPS = 60  # Frames per second for the video


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


def get_audio_duration(audio_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
         audio_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)


def main(audio_path):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bouncing Balls")
    clock = pygame.time.Clock()

    balls = []
    frame_count = 0

    # Get the audio duration
    audio_duration = get_audio_duration(audio_path)
    frames = []
    running = True
    start_time = time.time()

    while running and (time.time() - start_time) < audio_duration:
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

        # Capture the current frame
        frame = pygame.surfarray.array3d(screen)
        frame = frame.transpose([1, 0, 2])  # Convert from (width, height, colors) to (height, width, colors)
        frames.append(frame)

        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1

    pygame.quit()

    # Save the captured frames as a video file
    clip = ImageSequenceClip(frames, fps=FPS)

    # Load the audio file
    try:
        audio_clip = AudioFileClip(audio_path)
        final_clip = clip.set_audio(audio_clip)
        final_clip.write_videofile("bouncing_balls_with_audio.mp4", codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Error loading audio file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
