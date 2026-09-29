# Arcade 2D Ship Shooter

A classic 2D arcade space shooter built with **Python** and **Pygame**.

---

## Features

* **Frame-Rate Independent:** Uses Delta Time ($\Delta t$) so movement speed remains consistent across all monitor refresh rates.
* **Balanced Movement:** Vector normalization prevents faster diagonal movement.
* **Modular Architecture:** Clean separation of game logic across dedicated entity files.
* **Dynamic Enemy Spawning:** Automatic timer system using custom Pygame events (`USEREVENT`) to spawn incoming enemies at randomized screen positions.
* **Collision Detection:** Efficient sprite-group collision management for projectile hits and player damage.
* **Memory Management:** Auto-destroys off-screen projectiles and defeated enemies to conserve memory.

---

## Project Structure

```text
ship_shooter/
├── settings.py     # Game configuration, screen size, colors, and speeds
├── main.py         # Entry point, game loop, timers, collision checking, and rendering
├── player.py       # Player movement, boundary collision, and laser firing logic
├── projectile.py   # Laser movement and off-screen cleanup
├── enemy.py        # Enemy movement and boundary cleanup
└── README.md
