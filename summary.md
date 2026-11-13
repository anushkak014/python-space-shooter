# Space Shooter – Project Summary (PS No. 59)

## Overview
A 2D arcade game built with Python 3 and Pygame. The player moves a spaceship at the bottom of a 600 × 600 window, fires bullets upward, destroys descending enemies, earns 10 points per enemy, and starts with three lives.

## Main features
- LEFT/RIGHT arrow keys move the ship.
- SPACE fires bullets; maximum five bullets on screen.
- Enemies descend from the top.
- `Rect.colliderect()` detects bullet-enemy collisions.
- Each destroyed enemy adds 10 points.
- Each enemy reaching y = 600 costs one life.
- Game Over displays the final score.

## Difficulties encountered
1. **Pygame installation:** The initial installation failed on the installed newer Python versions. The error included `ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'`. A compatible Python 3.13 environment was selected as the troubleshooting route.
2. **Syntax error:** The heading and run instructions at the top of the Python file were plain text. They were enclosed in triple quotation marks so the import statements remain executable.
3. **Filename:** The editor showed a filename ending in `.py.py`; rename it to `space_shooter.py`.
4. **Testing:** Run and verify every test before marking it as passed.

## Test evidence checklist

| Test | Expected result | Screenshot to add |
|---|---|---|
| Normal input: ship x=275, press SPACE | Bullet at (300, 520); count 1 | `test1_normal_input.png` |
| Left boundary: x=0, press LEFT | Ship stays at x=0 | `test2_left_boundary.png` |
| Right boundary: x=550, press RIGHT | Ship stays at x=550 | `test2_right_boundary.png` |
| Five bullets, press SPACE | No new bullet; count remains 5 | `test3_max_bullets.png` |
| Bullet (300,100), enemy (280,90) | Enemy destroyed; score 10; lives 3 | `test4a_collision.png` |
| Enemy reaches y=600, lives=3 | Enemy escaped; lives 2 | `test4b_enemy_escape.png` |

> **Important:** Screenshot entries are placeholders, not actual test screenshots. Capture the real game/test output with Windows + Shift + S and add the images before submission.

## Current status
The installation and syntax issues were identified during setup. Successful Pygame installation, game execution, and all test results still need confirmation. Do not mark tests as passed until they have been run.

## Author
- Name: Anushka Keshri
- Roll number: RU-26-01601
- Institution: Rungta International Skills University
