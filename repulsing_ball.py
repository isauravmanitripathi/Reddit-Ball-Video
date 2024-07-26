import pygame
import random
import math
import time
import subprocess
from moviepy.editor import ImageSequenceClip, AudioFileClip
import sys

# Constants
SCREEN_WIDTH = 1080  # Resolution for Instagram Reels or YouTube Shorts
SCREEN_HEIGHT = 1920
BALL_RADIUS = 40  # Increased ball radius to twice the size
MAX_BALLS = 20  # Number of balls
REPEL_FORCE = 1000  # Force of repulsion
FPS = 60  # Frames per second for the video


class Ball:
    def __init__(self, x, y, vx, vy, radius, color):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(vx, vy)
        self.radius = radius
        self.color = color

    def update(self, balls):
        for ball in balls:
            if ball != self:
                distance = self.position.distance_to(ball.position)
                if distance < 2 * self.radius:
                    direction = (self.position - ball.position).normalize()
                    self.velocity += direction * (REPEL_FORCE / (distance ** 2))
                    ball.velocity -= direction * (REPEL_FORCE / (distance ** 2))

        self.position += self.velocity

        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= SCREEN_WIDTH:
            self.velocity.x = -self.velocity.x
            self.position.x = max(self.position.x, self.radius)
            self.position.x = min(self.position.x, SCREEN_WIDTH - self.radius)

        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y
            self.position.y = max(self.position.y, self.radius)
            self.position.y = min(self.position.y, SCREEN_HEIGHT - self.radius)


class MainState:
    def __init__(self):
        self.balls = [
            Ball(
                random.uniform(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS),
                random.uniform(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS),
                random.uniform(-10, 10),  # Increased speed range
                random.uniform(-10, 10),  # Increased speed range
                BALL_RADIUS,
                pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ) for _ in range(MAX_BALLS)
        ]

    def update(self):
        for ball in self.balls:
            ball.update(self.balls)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for ball in self.balls:
            pygame.draw.circle(screen, ball.color, (int(ball.position.x), int(ball.position.y)), ball.radius)


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
    pygame.display.set_caption("Repulsing Balls Animation")

    clock = pygame.time.Clock()
    state = MainState()

    # Get the audio duration
    audio_duration = get_audio_duration(audio_path)
    frames = []
    running = True
    start_time = time.time()

    while running and (time.time() - start_time) < audio_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state.update()
        state.draw(screen)

        # Capture the current frame
        frame = pygame.surfarray.array3d(screen)
        frame = frame.transpose([1, 0, 2])  # Convert from (width, height, colors) to (height, width, colors)
        frames.append(frame)

        clock.tick(FPS)

    pygame.quit()

    # Save the captured frames as a video file
    clip = ImageSequenceClip(frames, fps=FPS)
    audio_clip = AudioFileClip(audio_path)

    # Ensure the audio clip duration matches the video clip duration
    if audio_clip.duration > clip.duration:
        audio_clip = audio_clip.subclip(0, clip.duration)

    final_clip = clip.set_audio(audio_clip)
    final_clip.write_videofile(
        "repulsing_balls_with_audio.mp4",
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        preset="slow",
        ffmpeg_params=["-crf", "18"],  # Use CRF 18 for high-quality encoding
        threads=4  # Use multiple threads for faster encoding
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
