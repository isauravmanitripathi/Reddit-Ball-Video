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
NUM_MOLECULES = 75
MOLECULE_RADIUS = 20
MAX_VELOCITY = 35
BG_COLOR = (0, 0, 0)
FPS = 60  # Frames per second for the video


# Random color generator
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Molecule:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self, molecules):
        self.x += self.vx
        self.y += self.vy

        # Bounce off the walls
        if self.x + MOLECULE_RADIUS > SCREEN_WIDTH or self.x - MOLECULE_RADIUS < 0:
            self.vx = -self.vx
        if self.y + MOLECULE_RADIUS > SCREEN_HEIGHT or self.y - MOLECULE_RADIUS < 0:
            self.vy = -self.vy

        # Handle collisions with other molecules
        for molecule in molecules:
            if molecule != self:
                dx = self.x - molecule.x
                dy = self.y - molecule.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < MOLECULE_RADIUS * 2:
                    # Simple elastic collision response
                    angle = math.atan2(dy, dx)
                    self.vx, self.vy = -self.vx, -self.vy
                    molecule.vx, molecule.vy = -molecule.vx, -molecule.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), MOLECULE_RADIUS)


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
    pygame.display.set_caption("Molecular Dynamics Simulation")
    clock = pygame.time.Clock()

    molecules = [Molecule(
        random.randint(MOLECULE_RADIUS, SCREEN_WIDTH - MOLECULE_RADIUS),
        random.randint(MOLECULE_RADIUS, SCREEN_HEIGHT - MOLECULE_RADIUS),
        random.uniform(-MAX_VELOCITY, MAX_VELOCITY),
        random.uniform(-MAX_VELOCITY, MAX_VELOCITY),
        random_color()
    ) for _ in range(NUM_MOLECULES)]

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

        for molecule in molecules:
            molecule.update(molecules)
            molecule.draw(screen)

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
        final_clip.write_videofile("molecular_dynamics_with_audio.mp4", codec="libx264", audio_codec="aac")
    except Exception as e:
        print(f"Error loading audio file: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    main(audio_path)
