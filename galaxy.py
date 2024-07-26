import pygame
import random
import math
import time
import subprocess
from moviepy.editor import ImageSequenceClip, AudioFileClip
import sys

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
NUM_STARS = 500
STAR_RADIUS = 3
ROTATION_SPEED = 0.01
SPIRAL_TIGHTNESS = 0.1
BG_COLOR = (0, 0, 0)
FPS = 30  # Frames per second for the video

# Random color generator
def random_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

class Star:
    def __init__(self, angle, distance, color):
        self.angle = angle
        self.distance = distance
        self.color = color
        self.x = SCREEN_WIDTH // 2 + distance * math.cos(angle)
        self.y = SCREEN_HEIGHT // 2 + distance * math.sin(angle)

    def update(self):
        self.angle += ROTATION_SPEED
        self.distance += SPIRAL_TIGHTNESS
        self.x = SCREEN_WIDTH // 2 + self.distance * math.cos(self.angle)
        self.y = SCREEN_HEIGHT // 2 + self.distance * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), STAR_RADIUS)

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
    pygame.display.set_caption("Spiral Galaxy Animation")
    clock = pygame.time.Clock()

    stars = [Star(
        random.uniform(0, 2 * math.pi),
        random.uniform(0, 100),
        random_color()
    ) for _ in range(NUM_STARS)]

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

        for star in stars:
            star.update()
            star.draw(screen)

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
        final_clip.write_videofile("spiral_galaxy_with_audio.mp4", codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Error loading audio file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
