# Pygame Jump King

A small Jump King inspired climbing prototype built with Pygame.

## Run

This project follows the existing `run.sh` convention and expects a conda
environment named `pygame`.

```bash
./run.sh
```

You can also run the entry point directly from the project root:

```bash
python ./scripts/main.py
```

## Controls

- `A` / `D` or arrow keys: move
- `SPACE`: hold to charge, release to jump
- `ENTER`: start or resume
- `R`: reset
- `ESC`: pause or quit

## Structure

- `scripts/main.py`: entry point
- `scripts/game.py`: main loop, state machine, drawing
- `scripts/player.py`: movement, gravity, collision, charge jump
- `scripts/level.py`: JSON level loading and platform drawing
- `scripts/camera.py`: vertical camera tracking
- `scripts/storage.py`: local best height and clear-time save data
- `data/level_01.json`: first playable vertical level
