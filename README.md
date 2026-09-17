# Flappy Bird 3D with Python Pygame

A school project that turns Flappy Bird-style gameplay into a pseudo-3D presentation using 2D Pygame artwork. The game renders a bird, perspective-scaled wall pairs, animated lizards, scrolling scenery, sound effects, and a persistent high score.

## Play

- Press **Space** to flap and begin the game.
- Pass between the wall pairs to score.
- Click the pause icon in the upper-left corner to pause and resume.
- After a collision, press **R** to restart.
- Close the window to exit.

The game runs at a 500 × 700 window and targets 60 frames per second. It stores the high score with Python's `shelve` module in the local `score` files.

## Run the source

The source entry point is `flappy3D.py`. The repository does not include a requirements file; install a compatible Python 3 and Pygame environment, then run from the repository root so the relative `images/`, `fonts/`, and `sounds/` paths resolve:

```bash
python -m pip install pygame
python flappy3D.py
```

The repository also includes a Windows executable, `flappy3D.exe`, together with its bundled Python/Pygame runtime files. On Windows, the executable can be launched directly from the repository directory.

## Assets

- `images/` contains the bird animation frames, wall pieces/caps, lizard shadows, gradient, and pause artwork.
- `fonts/pixel.ttf` supplies the in-game text.
- `sounds/` contains the music and gameplay effects.
- `flappy3D.py` contains the game loop, perspective wall scaling, collision checks, scoring, pause flow, and restart flow.

## Development status

This is a compact educational game rather than a packaged library. No automated tests, dependency lockfile, build configuration, CI workflow, or license file is included. The checked-in executable and native libraries are Windows-oriented; running the Python source on another platform requires a separately configured Pygame installation and compatible media support.
