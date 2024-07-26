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
BALL_RADIUS = 10  # Smaller ball radius
COOLDOWN_DURATION = 1  # 1 second cooldown
MAX_BALLS = 2500  # Reduced maximum number of balls for performance
FPS = 60  # Frames per second for the video


class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(vx, vy)
        self.color = color
        self.last_multiplied = time.time()

    def update(self):
        self.position += self.velocity
        hit = False

        if self.position.x - BALL_RADIUS <= 0 or self.position.x + BALL_RADIUS >= SCREEN_WIDTH:
            self.velocity.x = -self.velocity.x
            self.position.x = max(self.position.x, BALL_RADIUS)
            self.position.x = min(self.position.x, SCREEN_WIDTH - BALL_RADIUS)
            hit = True

        if self.position.y - BALL_RADIUS <= 0 or self.position.y + BALL_RADIUS >= SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y
            self.position.y = max(self.position.y, BALL_RADIUS)
            self.position.y = min(self.position.y, SCREEN_HEIGHT - BALL_RADIUS)
            hit = True

        return hit


class MainState:
    def __init__(self):
        self.balls = [Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 5, 7, pygame.Color('white'))]

    def update(self):
        new_balls = []
        num_balls = len(self.balls)
        for ball in self.balls:
            if ball.update() and time.time() - ball.last_multiplied > COOLDOWN_DURATION and num_balls + len(
                    new_balls) < MAX_BALLS:
                color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                angle = random.uniform(0, math.pi * 2)
                new_velocity = pygame.math.Vector2(math.cos(angle) * 5, math.sin(angle) * 5)
                new_balls.append(Ball(ball.position.x, ball.position.y, new_velocity.x, new_velocity.y, color))
                ball.last_multiplied = time.time()
        self.balls.extend(new_balls)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for ball in self.balls:
            pygame.draw.circle(screen, ball.color, (int(ball.position.x), int(ball.position.y)), BALL_RADIUS)


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
    pygame.display.set_caption("Multiplying Balls")

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
        "multiplying_balls_with_audio.mp4",
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
