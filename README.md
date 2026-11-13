# Space Shooter (Project No. 59)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-orange.svg)](https://www.pygame.org/)
[![Build Status: Passed](https://img.shields.io/badge/Tests-4%2F4%20Passed-brightgreen.svg)]()
[![Course: RU--100--01--0021](https://img.shields.io/badge/Course-RU--100--01--0021-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Course:** Programming Fundamentals and Logic Building Using Python (`RU-100-01-0021`)  
> **Institution:** Rungta International Skills University, School of Computer Science and Engineering  
> **Degree:** Bachelor of Technology (Computer Science & Engineering)  
> **Academic Session:** 2026–2027  
> **Class:** B.Tech / CSE / First Semester / Section – K  
> **Date of Allocation:** 14th October 2026 | **Date of Submission:** 16th November 2026  

---

## 📌 Problem Statement (PS No. 59)

> **Build a space shooter game in which the player's spaceship moves left and right at the bottom of the screen and fires bullets upward to destroy enemy ships descending from the top. The player earns points for each hit and loses a life when an enemy reaches the bottom.**
>
> **Language:** Python 3  
> **Core Concepts:** Pygame, Object-Oriented Programming (Classes & Objects), Collision Detection (`Rect.colliderect`), Game Loop.  
> **Specifications:** Window `600x600`. Ship is `50x50` at $y = 520$ and moves `8 px` per key press. Bullet is `5x10` and moves `10 px` per frame upward; maximum `5` bullets on screen. Enemy is `40x40`. Hit = `+10 score`; an enemy reaching $y = 600$ costs `1 life` (starts with `3 lives`). Positions given as $(x, y) = \text{top-left corner}$.

---

## 🚀 Key Production Features

1. **Object-Oriented Design (BMR #2):**
   - Independent, decoupled classes for `Ship`, `Bullet`, and `Enemy`, each encapsulating position $(x, y)$, dimensions $(w, h)$, movement vectors, and rendering logic.
2. **Deterministic Player Navigation (BMR #3):**
   - Responsive horizontal navigation using the `LEFT` and `RIGHT` arrow keys at exactly $8\text{ px}$ per press.
   - Strict window clamping preventing the ship from exiting the screen ($x \in [0, 550]$).
3. **Throttled Ammunition System (BMR #3):**
   - Bullets fire from the precise center-top of the ship: $(x + 25, 520)$.
   - Active on-screen bullet cap strictly enforced at $N \le 5$. Extraneous space presses when 5 bullets are active are gracefully discarded.
4. **Collision Detection via Axis-Aligned Bounding Boxes (BMR #4):**
   - Bullet-enemy impacts are detected using `pygame.Rect.colliderect()`.
   - On collision, both interacting entities are atomically destroyed, and $+10$ points are credited to the player's score.
5. **Life Depletion & Game Over Protocol (BMR #5):**
   - The player starts with $3$ lives.
   - Any enemy crossing the lower threshold ($y \ge 600$) without being intercepted decrements the player's life count by $1$.
   - When lives reach $0$, the game transitions to a modal **GAME OVER** screen displaying the final score, offering instant session restart via `[R]` or exit via `[ESC]`.

---

## 🕹️ Controls & HUD Layout

| Action | Control Key | Description |
| :--- | :--- | :--- |
| **Move Left** | `LEFT Arrow` / `A` | Translates spaceship left by $8\text{ px}$ (min boundary: $x = 0$) |
| **Move Right** | `RIGHT Arrow` / `D` | Translates spaceship right by $8\text{ px}$ (max boundary: $x = 550$) |
| **Fire Laser** | `SPACEBAR` | Discharges upward bullet (max 5 simultaneous bullets) |
| **Restart Game** | `R` | Resets score, lives, entities, and restarts fresh game loop |
| **Quit Game** | `ESCAPE` / Window Close | Cleanly closes Pygame window and terminates process |

---

## 📐 Mathematical & Physics Formulations

### 1. Spaceship Clamping Inequality
The spaceship coordinate $(x_{\text{ship}}, y_{\text{ship}})$ with width $W_s = 50$ is constrained within a window of width $W = 600$:
$$0 \le x_{\text{ship}} \le (W - W_s) \implies 0 \le x_{\text{ship}} \le 550$$
Upon each directional movement command $\Delta \in \{-1, +1\}$:
$$x_{\text{new}} = \max\Big(0, \min\big(x_{\text{current}} + \Delta \cdot V_{\text{ship}},\, 550\big)\Big)$$
Where $V_{\text{ship}} = 8\text{ px}$.

### 2. Bullet Origin Coordinate Formula
Bullets must emerge precisely from the center of the ship's leading edge:
$$x_{\text{bullet}} = x_{\text{ship}} + \frac{W_s}{2} = 275 + 25 = 300$$
$$y_{\text{bullet}} = y_{\text{ship}} = 520$$
With top-left bounding rectangle:
$$\text{Rect}_{\text{bullet}} = \left(x_{\text{bullet}} - \frac{W_b}{2},\, y_{\text{bullet}},\, W_b,\, H_b\right) = (300 - 2,\, 520,\, 5,\, 10)$$

### 3. Collision Condition (AABB Intersection)
Two rectangular bounding boxes $R_1(x_1, y_1, w_1, h_1)$ and $R_2(x_2, y_2, w_2, h_2)$ collide if and only if all four 1D projections overlap:
$$\text{colliderect}(R_1, R_2) \iff (x_1 < x_2 + w_2) \land (x_1 + w_1 > x_2) \land (y_1 < y_2 + h_2) \land (y_1 + h_1 > y_2)$$

---

## 📊 Acceptance Test Cases Verification Table

| Test Case | Scenario / Input | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Test Case 1** | **Normal Input:**<br>Ship $x = 275$, 0 bullets on screen<br>Key: `SPACE` | Bullet fired at $(300, 520)$<br>Bullets on screen: $1$ | `Bullet fired at (300, 520) \| Bullets on screen: 1` | ✅ **PASS** |
| **Test Case 2 (a)** | **Boundary Min (Left Edge):**<br>Ship $x = 0$, Key: `LEFT` | Ship $x = 0$<br>(no movement, stays inside window) | `Ship x = 0 (no movement, stays inside window)` | ✅ **PASS** |
| **Test Case 2 (b)** | **Boundary Max (Right Edge):**<br>Ship $x = 550$, Key: `RIGHT` | Ship $x = 550$<br>(no movement, stays inside window) | `Ship x = 550 (no movement, stays inside window)` | ✅ **PASS** |
| **Test Case 3** | **Invalid Input (Limit Exceeded):**<br>5 bullets already on screen<br>Key: `SPACE` | Maximum 5 bullets on screen.<br>No bullet fired.<br>Bullets on screen: $5$ | `Maximum 5 bullets on screen. No bullet fired.`<br>`Bullets on screen: 5` | ✅ **PASS** |
| **Test Case 4 (a)** | **Game Event (Collision):**<br>Bullet at $(300, 100)$, Enemy at $(280, 90)$ | Enemy destroyed<br>Score: $10$ \| Lives: $3$ | `Enemy destroyed \| Score: 10 \| Lives: 3` | ✅ **PASS** |
| **Test Case 4 (b)** | **Game Event (Escaped Enemy):**<br>Enemy reaches $y = 600$, Lives before: $3$ | Enemy escaped<br>Lives: $2$ | `Enemy escaped \| Lives: 2` | ✅ **PASS** |

---

## 💻 How to Run the Project

Launch the 60 FPS graphical interactive game:
```powershell
python main.py
```

---

## 🎯 Viva Voce Technical Preparation

### Q1: What is the purpose of the Game Loop and `clock.tick(60)`?
**Answer:** The game loop continuously handles user events, updates physics/positions, and renders graphical frames. `clock.tick(60)` caps the game loop execution at 60 frames per second (FPS), ensuring consistent game speed and physics across machines with differing CPU architectures.

### Q2: Why is `Rect.colliderect()` preferred over manual pixel checking?
**Answer:** `Rect.colliderect()` performs Axis-Aligned Bounding Box (AABB) collision testing using high-speed C-level boundary comparisons in $O(1)$ time complexity, minimizing CPU overhead compared to costly per-pixel alpha mask checks.

### Q3: Why do we iterate over a shallow slice `self.bullets[:]` when removing items?
**Answer:** In Python, removing elements from a list while iterating over it causes the iterator indices to shift, resulting in skipped elements. Iterating over a shallow copy (`bullets[:]`) guarantees safe, deterministic removal of off-screen or collided entities.

### Q4: How is the maximum bullet constraint of 5 enforced?
**Answer:** Inside `fire_bullet()`, the length of the active bullet list (`len(self.bullets)`) is checked against `MAX_BULLETS = 5`. If equal to 5, the method returns `None` and skips spawning, preventing infinite bullet spamming.

---

## 📄 License
This project is developed for academic evaluation under the Computer Science & Engineering curriculum at Rungta International Skills University.
Licensed under the [MIT License](LICENSE).
