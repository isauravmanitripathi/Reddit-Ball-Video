import pygame
import random
import time
import subprocess
from moviepy.editor import ImageSequenceClip, AudioFileClip
import sys

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
NUM_FIREFLIES = 50
FIREFLY_RADIUS = 5
MAX_VELOCITY = 2
BG_COLOR = (0, 0, 0)
GLOW_COLOR = (255, 255, 0)
FPS = 60  # Frames per second for the video


# Random color generator
def random_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


class Firefly:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off the walls
        if self.x + FIREFLY_RADIUS > SCREEN_WIDTH or self.x - FIREFLY_RADIUS < 0:
            self.vx = -self.vx
        if self.y + FIREFLY_RADIUS > SCREEN_HEIGHT or self.y - FIREFLY_RADIUS < 0:
            self.vy = -self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), FIREFLY_RADIUS)
        pygame.draw.circle(screen, GLOW_COLOR, (int(self.x), int(self.y)), FIREFLY_RADIUS * 3, 1)


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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HIDDEN)
    pygame.display.set_caption("Firefly Animation")
    clock = pygame.time.Clock()

    fireflies = [Firefly(
        random.randint(FIREFLY_RADIUS, SCREEN_WIDTH - FIREFLY_RADIUS),
        random.randint(FIREFLY_RADIUS, SCREEN_HEIGHT - FIREFLY_RADIUS),
        random.uniform(-MAX_VELOCITY, MAX_VELOCITY),
        random.uniform(-MAX_VELOCITY, MAX_VELOCITY),
        random_color()
    ) for _ in range(NUM_FIREFLIES)]

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

        for firefly in fireflies:
            firefly.update()
            firefly.draw(screen)

        # Capture the current frame
        frame = pygame.surfarray.array3d(screen)
        frame = frame.transpose([1, 0, 2])  # Convert from (width, height, colors) to (height, width, colors)
        frames.append(frame)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

    # Save the captured frames as a video file
    clip = ImageSequenceClip(frames, fps=FPS)

    # Load the audio file
    try:
        audio_clip = AudioFileClip(audio_path)
        final_clip = clip.set_audio(audio_clip)
        final_clip.write_videofile("firefly_animation_with_audio.mp4", codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Error loading audio file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
