# Python Tetris

A classic Tetris game implemented in Python using Pygame.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

Run the game:

```bash
python tetris.py
```

### Controls

- Left Arrow: Move piece left
- Right Arrow: Move piece right
- Down Arrow: Move piece down faster
- Up Arrow: Rotate piece
- Space: Hard drop (instantly drop the piece)

### Game Features

- Score tracking
- Level progression (speed increases with level)
- Next piece preview
- Lines cleared counter
- Game over screen

### Scoring System

- 1 line: 100 points × level
- 2 lines: 300 points × level
- 3 lines: 500 points × level
- 4 lines: 800 points × level

The level increases for every 10 lines cleared.
