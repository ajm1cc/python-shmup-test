# Cho Ren Sha - Python Edition

A vertical scrolling shoot'em up game inspired by the classic Cho Ren Sha 68k, built with Python and Pygame.

## Description

This is a fast-paced vertical scrolling shooter (shmup) featuring:
- Multiple enemy types with unique behavior patterns
- Progressive power-up system
- Challenging boss battles every 30 seconds
- Bomb system for clearing the screen
- Score tracking with high score persistence
- Smooth 60 FPS gameplay
- Classic arcade-style difficulty

## Features

### Gameplay Elements
- **4 Enemy Types**: Each with unique movement patterns and bullet patterns
  - Basic enemies with aimed shots
  - Fast enemies with spread shots
  - Tank enemies with five-way spread (higher HP)
  - Weaving enemies with circular bullet patterns

- **Power System**: Collect power-ups to increase your firepower up to 5 levels
  - Level 1: Single shot
  - Level 2: Double shot
  - Level 3: Triple shot with angled side shots
  - Level 4: Quad shot with wider spread
  - Level 5: Five-way maximum firepower

- **Boss Battles**: Epic encounters with large enemies featuring multiple attack patterns
  - Spiral bullet patterns
  - Ring explosions
  - Wave attacks
  - Health bar display

- **Bomb System**: Clear the screen of bullets and damage all enemies
  - Start with 3 bombs
  - Collect more from defeated enemies
  - Grants temporary invincibility

### Visual Effects
- Scrolling starfield background
- Explosion animations
- Invincibility flashing
- Dynamic bullet patterns

## Installation

### Requirements
- Python 3.7 or higher
- Pygame library

### Install Dependencies

```bash
pip install pygame
```

Or if you're using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

## How to Play

### Running the Game

```bash
python shmup.py
```

Or make it executable:
```bash
chmod +x shmup.py
./shmup.py
```

### Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move your ship |
| Z / Spacebar | Shoot |
| X | Use Bomb (clears enemy bullets and damages enemies) |
| ESC | Pause game / Return to menu |
| Enter | Start game / Continue after game over |

### Gameplay Tips

1. **Stay Mobile**: Constant movement is key to avoiding the dense bullet patterns
2. **Power Up Early**: Collect blue power-ups to increase your firepower
3. **Save Bombs for Emergencies**: Use bombs when surrounded by bullets
4. **Learn Enemy Patterns**: Each enemy type has predictable behavior
5. **Focus on Boss Patterns**: Boss attacks change every 5 seconds
6. **Don't Be Greedy**: Sometimes avoiding bullets is more important than scoring

### Scoring System

- Basic Enemy: 100 points
- Fast Enemy: 150 points
- Weaving Enemy: 200 points
- Tank Enemy: 300 points
- Boss: 5,000 points
- Power-up collected: 50 points
- Bomb collected: 100 points

## Game Mechanics

### Lives and Death
- Start with 3 lives
- Taking damage reduces your power level by 1
- Grants temporary invincibility after being hit
- Game over when all lives are lost

### Power-ups
- Appear randomly when enemies are destroyed (15% chance)
- Blue orbs increase weapon power
- Red orbs grant additional bombs
- Automatically attracted to your ship when nearby

### Boss Encounters
- Spawns every 30 seconds
- Has 100 HP
- Features three rotating attack patterns:
  1. Spiral Pattern: Rotating triple shots
  2. Ring Burst: 12-way explosions
  3. Wave Pattern: Cascading bullets
- Defeating boss increases level and difficulty

## Development

This game was created as a tribute to classic shoot'em ups like Cho Ren Sha 68k. The code is organized into clear classes for easy modification and extension.

### Project Structure
```
shmup.py - Main game file containing all classes and game logic
├── Player class - Player ship with shooting and power-up mechanics
├── Bullet class - Player projectiles
├── EnemyBullet class - Enemy projectiles with angle-based movement
├── Enemy class - Four enemy types with unique behaviors
├── Boss class - Boss enemy with pattern-based attacks
├── PowerUp class - Collectible items
├── Explosion class - Visual effects
└── Game class - Main game loop and state management
```

### Customization

You can easily modify game parameters by editing the constants at the top of `shmup.py`:
- Screen resolution (SCREEN_WIDTH, SCREEN_HEIGHT)
- Frame rate (FPS)
- Colors
- Enemy spawn rates
- Player speed and power levels
- Boss HP and attack patterns

## Troubleshooting

### Game runs slowly
- Check that you have hardware acceleration enabled
- Try reducing the screen resolution
- Close other applications

### No sound
- The game currently uses visual-only feedback
- Sound effects can be added using pygame.mixer

### Controls not responding
- Make sure the game window has focus
- Try clicking on the window
- Check if another application is intercepting key presses

## Credits

Inspired by:
- Cho Ren Sha 68k by Koichi "Famibe" Kitamura
- Classic arcade shoot'em ups

Created with Python and Pygame.

## License

This is a fan project created for educational purposes. Feel free to modify and extend it!

## Future Enhancements

Possible features to add:
- Sound effects and music
- Multiple difficulty levels
- Different player ships
- More enemy types
- Stage system with varied backgrounds
- Replay system
- Online leaderboards
- Gamepad support
- Configuration file for key bindings

Enjoy the game and aim for the high score!
