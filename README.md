# OpenGL 3D Shooter Survival

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenGL](https://img.shields.io/badge/Library-PyOpenGL-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

**Repository Link:** [https://github.com/rfuadur/OpenGL-3D-Shooter-Survival](https://github.com/rfuadur/OpenGL-3D-Shooter-Survival)

## 📝 Project Overview
This project is a 3D survival shooter game developed using **Python** and **OpenGL**. It demonstrates 3D rendering, camera transformations (`gluLookAt`), and perspective projection (`gluPerspective`).

The player controls a character in a 3D arena, defending against waves of enemies that track the player's position. The game features multiple camera perspectives, a cheat mode for auto-aiming, and win/loss conditions based on survival metrics.

## ✨ Key Technical Features
* **3D Rendering Pipeline:** Utilizes `GL_PROJECTION` and `GL_MODELVIEW` matrices to render a 3D world with depth testing (`GL_DEPTH_TEST`).
* **Camera Systems:**
    * **Third-Person (Default):** Fixed overhead view of the arena.
    * **First-Person:** Immersive view that follows the player's rotation and movement.
* **Enemy AI:** Enemies (spheres) automatically calculate vectors to track and move towards the player's current position.
* **Collision Detection:** Implements distance-based collision logic between bullets, enemies, and the player.
* **Cheat Modes:**
    * **Auto-Aim (C):** Automatically rotates the player to face the nearest enemy.
    * **Vision Lock (V):** Locks the camera to the player's target for cinematic effect (First-Person only).

## 🎮 Controls

| Input | Action | Description |
| :--- | :--- | :--- |
| **W / S** | Move Forward/Back | Moves the player relative to their facing direction. |
| **A / D** | Rotate Player | Rotates the character left or right. |
| **Spacebar** | Shoot | Fires a bullet in the current facing direction. |
| **Right Click** | Toggle Camera | Switches between First-Person and Third-Person views. |
| **C** | Cheat Mode | Toggles Auto-Aim and Auto-Fire. |
| **V** | Vision Cheat | Toggles Camera Lock (First-Person only). |
| **R** | Restart | Resets the game after a "Game Over". |

## 🛠️ Prerequisites
To run this project, you need the following installed:
* **Python 3.x**
* **PyOpenGL**

## 🚀 How to Run

### 1. Install Dependencies
If you haven't installed the OpenGL library yet, run this command in your terminal:

```bash
pip install PyOpenGL PyOpenGL_accelerate
