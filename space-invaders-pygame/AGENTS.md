# Space Invaders Pygame - Agent Instructions

## Project Overview
Space Invaders clone built with Pygame.

## How to Run
```bash
cd space-invaders-pygame/project/scripts
python main.py
```

## Project Structure
```
space-invaders-pygame/project/scripts/
├── main.py          # Entry point
├── settings.py      # Constants, colors, game config
├── game.py          # Game loop, state management, collision detection
├── player.py        # Player ship (movement, shooting, invincibility)
├── alien.py         # Aliens (3 types, 5x11 grid, movement, firing)
├── bullet.py        # Bullets + BulletManager (player/alien)
├── barrier.py       # Barriers + BarrierManager (4 shields, block-level destruction)
├── score.py         # Score, high score, level, lives HUD
├── explosion.py     # Explosion effects (Explosion + ExplosionManager)
└── game_over.py     # Start/pause/game over/victory screens
```

## Key Conventions
- `pygame.init()` is called in `Game.__init__()` (not in main.py)
- All game constants live in `settings.py`
- Colors are hex strings in `COLORS` dict, accessed via `pygame.Color(COLORS[key])`
- Alien types: `'top'` (30pts), `'mid'` (20pts), `'bottom'` (10pts) — mapped to color keys via `ALIEN_COLOR_MAP` in explosion.py
- Sprites are drawn programmatically (no image files)
- Game states: `STATE_START`, `STATE_PLAYING`, `STATE_GAME_OVER`, `STATE_LEVEL_CLEAR`, `STATE_PAUSED`

## Controls
- ← → : Move | SPACE : Shoot | P : Pause | R : Restart (game over) | ESC : Quit

## Known Issues / TODO
- No sound effects or BGM yet (sound/ directory empty)
- No UFO bonus enemy
- Alien sprites are basic pixel art; could be replaced with proper sprite sheets
