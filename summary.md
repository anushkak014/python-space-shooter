# Academic Project Report & Summary: Space Shooter

**Course Title:** Programming Fundamentals and Logic Building Using Python  
**Course Code:** RU-100-01-0021  
**Institution:** Rungta International Skills University (RISU)  
**Department:** School of Computer Science and Engineering  
**Degree:** Bachelor of Technology (Computer Science & Engineering)  
**Semester & Section:** First Semester / Section K  
**Student Name:** Anushka Keshri  
**Roll Number:** RU-26-01601  
**Problem Statement Number:** PS No. 59  
**Project Title:** Space Shooter  
**Language:** Python 3  
**Key Concepts:** Pygame, Object-Oriented Programming (Classes & Objects), Collision Detection (`Rect.colliderect`), Game Loops  
**Date of Allocation:** 14th October 2026  
**Date of Submission:** 16th November 2026  

---

## 1. Project Overview & Objective

The objective of Problem Statement No. 59 is to engineer a 2D arcade Space Shooter application using Python 3 and Pygame. The system simulates a player-controlled spaceship moving along the bottom horizontal axis of a $600 \times 600$ pixel window, emitting vertical laser projectiles to intercept and destroy hostile alien ships descending from the top boundary.

The game implements deterministic collision resolution, dynamic score tracking, finite ammunition throttling, life management, and modal state transitions between gameplay and game over states.

---

## 2. Bare Minimum Requirements Compliance Matrix

| # | Requirement | Implementation Specification | Compliance Status |
| :-: | :--- | :--- | :-: |
| **1** | Write the solution in Python 3 (one `.py` file) using Pygame and run it from the console | Entire gameplay logic is contained in `main.py` (and `One.py`), executable directly from command prompt or terminal. | Fully Satisfied |
| **2** | Create Ship, Bullet, and Enemy as classes (objects) with position, size, and speed | Explicit object-oriented classes: `Ship` ($50 \times 50$, $y=520$, speed 8), `Bullet` ($5 \times 10$, speed 10), and `Enemy` ($40 \times 40$, speed 2). | Fully Satisfied |
| **3** | Move the ship with LEFT/RIGHT arrows, fire bullets with SPACE, and limit bullets on screen to 5 | `Ship.move()` handles discrete directional movement bounded within $[0, 550]$. `fire_bullet()` rejects triggers when active bullets equal 5. | Fully Satisfied |
| **4** | Detect bullet-enemy collisions using `Rect.colliderect()`; add 10 to score for every enemy destroyed | `SpaceShooter.check_collisions()` performs AABB bounding box collision checks, removes colliding entities, and credits $+10$ points. | Fully Satisfied |
| **5** | Reduce a life when an enemy reaches the bottom; show 'Game Over' with final score when lives reach 0 | Escaped enemies at $y \ge 600$ reduce lives from initial 3. At 0 lives, modal Game Over overlay presents final score and `[R]` restart hook. | Fully Satisfied |

---

## 3. System Architecture & Class Hierarchy

```
+---------------------------------------------------------------+
|                         SpaceShooter                          |
+---------------------------------------------------------------+
| - ship: Ship                                                  |
| - bullets: List[Bullet]                                       |
| - enemies: List[Enemy]                                        |
| - score: int                                                  |
| - lives: int                                                  |
| - game_over: bool                                             |
+---------------------------------------------------------------+
| + fire_bullet() -> Optional[Bullet]                           |
| + update_bullets() -> None                                    |
| + update_enemies() -> None                                    |
| + check_collisions() -> None                                  |
| + spawn_enemy() -> None                                       |
| + restart() -> None                                           |
+---------------------------------------------------------------+
        |                     |                     |
        | 1                   | 0..5                | 0..*
        v                     v                     v
+---------------+     +---------------+     +---------------+
|     Ship      |     |    Bullet     |     |     Enemy     |
+---------------+     +---------------+     +---------------+
| - x, y: int   |     | - x, y: int   |     | - x, y: int   |
| - width: 50   |     | - width: 5    |     | - width: 40   |
| - height: 50  |     | - height: 10  |     | - height: 40  |
| - speed: 8    |     | - speed: 10   |     | - speed: 2    |
+---------------+     +---------------+     +---------------+
| + move(dir)   |     | + update()    |     | + update()    |
| + draw(surf)  |     | + draw(surf)  |     | + draw(surf)  |
| + rect: Rect  |     | + rect: Rect  |     | + rect: Rect  |
+---------------+     +---------------+     +---------------+
```

---

## 4. Mathematical Model & Collision Logic

### 4.1 Boundary Invariant
To prevent the spaceship of width $W_s = 50$ from traversing outside window width $W = 600$:
$$0 \le x_{\text{ship}} \le (600 - 50) \implies x_{\text{ship}} \in [0, 550]$$

### 4.2 Bullet Center Alignment
Projectiles originate from the exact horizontal midpoint of the spaceship's leading edge:
$$x_{\text{bullet}} = x_{\text{ship}} + \frac{W_s}{2} = x_{\text{ship}} + 25$$
$$y_{\text{bullet}} = y_{\text{ship}} = 520$$

### 4.3 Axis-Aligned Bounding Box (AABB) Collision Detection
Collision between bullet rectangle $B(x_b, y_b, w_b, h_b)$ and enemy rectangle $E(x_e, y_e, w_e, h_e)$ occurs when:
$$\text{colliderect}(B, E) \iff (x_b < x_e + w_e) \land (x_b + w_b > x_e) \land (y_b < y_e + h_e) \land (y_b + h_b > y_e)$$
This $O(1)$ calculation evaluates in minimal CPU cycles per frame.

---

## 5. Acceptance Test Cases Verification Record

The official problem statement mandates 4 acceptance test scenarios. All 4 scenarios are verified against the core game physics and collision engine.

### Test Case 1: Normal Input
- **Input Parameters:** Ship $x = 275$, 0 bullets on screen, Key pressed: `SPACE`
- **Expected Output:** `Bullet fired at (300, 520) | Bullets on screen: 1`
- **Observed Console Output:**
  ```text
  Bullet fired at (300, 520) | Bullets on screen: 1
  ```
- **Evaluation:** PASS (Exact specification match)

### Test Case 2: Boundary / Minimum Input
- **Sub-case (a):** Ship $x = 0$ (left boundary), Key pressed: `LEFT arrow`
  - **Expected Output:** `Ship x = 0 (no movement, stays inside window)`
  - **Observed Console Output:** `Ship x = 0 (no movement, stays inside window)`
  - **Evaluation:** PASS
- **Sub-case (b):** Ship $x = 550$ (right boundary), Key pressed: `RIGHT arrow`
  - **Expected Output:** `Ship x = 550 (no movement, stays inside window)`
  - **Observed Console Output:** `Ship x = 550 (no movement, stays inside window)`
  - **Evaluation:** PASS

### Test Case 3: Invalid Input (Bullet Capacity Constraint)
- **Precondition:** 5 bullets already active on screen
- **Input:** Key pressed: `SPACE`
- **Expected Output:**
  ```text
  Maximum 5 bullets on screen. No bullet fired.
  Bullets on screen: 5
  ```
- **Observed Console Output:**
  ```text
  Maximum 5 bullets on screen. No bullet fired.
  Bullets on screen: 5
  ```
- **Evaluation:** PASS (Strict throttle adherence)

### Test Case 4: Different Valid Scenario
- **Sub-case (a):** Bullet at $(300, 100)$ and enemy at $(280, 90)$
  - **Expected Output:** `Enemy destroyed | Score: 10 | Lives: 3`
  - **Observed Console Output:** `Enemy destroyed | Score: 10 | Lives: 3`
  - **Evaluation:** PASS
- **Sub-case (b):** Enemy reaches bottom boundary $y = 600$, initial lives: 3
  - **Expected Output:** `Enemy escaped | Lives: 2`
  - **Observed Console Output:** `Enemy escaped | Lives: 2`
  - **Evaluation:** PASS

---

## 6. Visual Evidence & Screenshot Documentation

### 6.1 Application Launch & Game Setup
Visual proof of the application starting cleanly in the 60 FPS Pygame window:

![Application Execution](execution.png)

### 6.2 Active Gameplay & HUD
Real-time gameplay showing player spaceship, descending enemies, laser emission, and HUD (Score, Lives, Bullet capacity):

![Space Shooter Gameplay](gameplay.png)

### 6.3 Bullet-Enemy Collision Detection
Visual proof of bullet impact destroying enemy targets and incrementing score:

![Collision Detection](collision.png)

### 6.4 Scoring & Life Deduction System
Real-time score accumulation and life decrement when an enemy evades interception:

![Score and Lives HUD](score_lives.png)

### 6.5 Modal Game Over Screen
Final score presentation upon depletion of all 3 player lives with restart option:

![Game Over Screen](game_over.png)

---

## 7. Technical Challenges & Engineering Solutions

### 7.1 Pygame Installation Across Python Environments
- **Issue:** On cutting-edge Python builds (Python 3.14 pre-release), pre-compiled binary wheels for Pygame are unavailable, triggering compiler errors (`ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'`).
- **Solution:** Standardized on Python 3.12 with pre-compiled Pygame 2.6.1 wheels via isolated virtual environments, providing reproducible zero-compilation deployment.

### 7.2 List Mutation During Forward Iteration
- **Issue:** Removing items from `self.bullets` or `self.enemies` inside a `for item in self.bullets` loop alters list indices dynamically, causing the iterator to skip subsequent elements.
- **Solution:** Sliced shallow copies (`self.bullets[:]` and `self.enemies[:]`) were used for traversal, ensuring index stability while modifying the underlying collection.

### 7.3 Bounded Ammunition Throttling
- **Issue:** Rapid key repetition allows unbounded bullet instantiation, overwhelming CPU resources and violating problem constraints.
- **Solution:** Enforced an atomic capacity guard in `fire_bullet()` checking `len(self.bullets) < MAX_BULLETS` before object creation.

---

## 8. Conclusion

Problem Statement No. 59 (Space Shooter) has been engineered to university academic standards. The codebase cleanly satisfies all 5 Bare Minimum Requirements, passes all 4 acceptance test cases, and provides robust interactive gameplay with structured object-oriented architecture.
