# Animation Projects with Pygame and MoviePy

This project is a collection of animation scripts using Pygame and MoviePy to create various animations and save them as videos with audio. The animations include falling balls, fireflies, a spiral galaxy, repulsing balls, and molecular dynamics simulations.

## Animations Overview

1. **Falling Balls Animation**
    - Video: [bouncing_balls_with_audio.mp4](./bouncing_balls_with_audio.mp4)
2. **Firefly Animation**
    - Video: [firefly_animation_with_audio.mp4](./firefly_animation_with_audio.mp4)
3. **Spiral Galaxy Animation**
    - Video: [spiral_galaxy_with_audio.mp4](./spiral_galaxy_with_audio.mp4)
4. **Repulsing Balls Animation**
    - Video: [repulsing_balls_with_audio.mp4](./repulsing_balls_with_audio.mp4)
5. **Molecular Dynamics Simulation**
    - Video: [molecular_dynamics_with_audio.mp4](./molecular_dynamics_with_audio.mp4)

## Requirements

The project requires Python and the following libraries, which are listed in the `requirements.txt` file:

- pygame
- moviepy

## Setting Up the Environment

To run these animations, it is recommended to set up a virtual environment. Below are the instructions for different operating systems.

### Windows

1. Open Command Prompt (cmd).
2. Navigate to the project directory.
3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```sh
   venv\Scripts\activate
   ```
5. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

### MacOS and Linux (Ubuntu)

1. Open Terminal.
2. Navigate to the project directory.
3. Create a virtual environment:
   ```sh
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```sh
   source venv/bin/activate
   ```
5. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Animations

Each animation has its own script file. Below are instructions on how to run each animation.

### Falling Balls Animation

1. Ensure the virtual environment is activated.
2. Run the script with the path to the audio file:
   ```sh
   python falling_balls.py <path_to_audio_file>
   ```

### Firefly Animation

1. Ensure the virtual environment is activated.
2. Run the script with the path to the audio file:
   ```sh
   python firefly_animation.py <path_to_audio_file>
   ```

### Spiral Galaxy Animation

1. Ensure the virtual environment is activated.
2. Run the script with the path to the audio file:
   ```sh
   python spiral_galaxy.py <path_to_audio_file>
   ```

### Repulsing Balls Animation

1. Ensure the virtual environment is activated.
2. Run the script with the path to the audio file:
   ```sh
   python repulsing_balls.py <path_to_audio_file>
   ```

### Molecular Dynamics Simulation

1. Ensure the virtual environment is activated.
2. Run the script with the path to the audio file:
   ```sh
   python molecular_dynamics.py <path_to_audio_file>
   ```

## Project Files

### falling_balls.py

This script generates an animation of bouncing balls with a gravitational effect. The balls bounce off the edges of the screen and interact with each other. The animation is saved as a video with the specified audio file.

### firefly_animation.py

This script creates an animation of fireflies moving around the screen. The fireflies glow and move in random directions. The animation is saved as a video with the specified audio file.

### spiral_galaxy.py

This script generates an animation of a spiral galaxy. Stars move in a spiral pattern, creating a galaxy-like effect. The animation is saved as a video with the specified audio file.

### repulsing_balls.py

This script creates an animation of balls that repel each other when they come close. The balls move around the screen and bounce off the edges. The animation is saved as a video with the specified audio file.

### molecular_dynamics.py

This script simulates molecular dynamics where molecules move around and collide with each other. The animation is saved as a video with the specified audio file.

## Conclusion

This project demonstrates various animations using Pygame for graphical rendering and MoviePy for video creation and adding audio. Each script is designed to create a specific type of animation and save it as a video file. Make sure to have the required audio files ready and follow the instructions to run each animation script. Enjoy the animations!

For more details and to watch the videos, refer to the links provided above.