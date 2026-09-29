# Arcade 2D Ship Shooter

A classic 2D arcade space shooter built with **Python** and **Pygame**.

---

## Features

* **Frame-Rate Independent:** Uses Delta Time so movement speed is smooth on any monitor.
* **Balanced Movement:** Vector normalization prevents faster diagonal movement.
* **Modular Code Structure:** Clean separation of game logic into distinct files.
* **Memory Management:** Auto-destroys off-screen projectiles to save memory.

---

## Project Structure

```text
ship_shooter/
├── settings.py     # Game configuration, screen size, colors, and speeds
├── main.py         # Entry point, game loop, and rendering
├── player.py       # Player movement, boundary collision, and shooting
├── projectile.py   # Laser movement and cleanup
├── assets.py       # TBD
└── README.md
