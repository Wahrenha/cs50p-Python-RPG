# Terminal RPG in Python ⚔️🎲

A text-based RPG built from scratch in **Python**. Developed as a final project for Harvard's **CS50P: Introduction to Programming with Python**, the game features character creation, item management, stats ane leveling systems, turn-based combat, an original story and a choice system that changes the player's experience depending on the chosen paths, along with new mechanics implemented in the game to make it more dinamic and fun.

The project is designed between a file that keeps the classes in which the mechanics are based in, and the main game file.

---

## ⚠️ Project Status Note
> **Development Status:** *Mechanics Complete / Story Work-in-Progress (WIP)*
> All core engines — including the turn-based combat system, dynamic shop logic, strict inventory memory buffers, leveling math, and large-scale army warfare algorithms — are **100% completed, fully optimized, and tested**. The main narrative campaign is playable up to the dramatic climax inside the King's secret fortress, with only final wrap-up story details currently in active writing.

---

## ⚙️ Core Classes & Modules

* **`Dice` Class:** Creates an $N$-sided physical dice using Python's `random` module, processing game elements like accuracy, damage rolls, healing and stat-checks.
* **`Armor` Class:** Handles armors attributes for different materials (Leather, Wood, Iron, Steel, Rebellion), mapping specific defense stats.
* **`Weapon` Class:** Represents the multiple weapons (Bow, Fireball Scroll, Sword, Mace, Knife, Army Sword) featured, applying damage by custom dice categories (e.g., Bow rolls a `d12`, while a Knife rolls a `d8`).
* **`Potions` Class:** Models consumable potions with unique effects (Healing, Strength, Quickness, Resistance, Super Healing), using custom combat boosts and automatic healing calculations.
* **`Classe` Class:** Sets baseline character archetypes (Archer, Wizard, Warrior, Ogre, Thief) and stores their starting statistical profiles.
* **`Character` Class:** The central object. It coordinates player metadata, dynamic stat updates, inventory, and core mechanics, such as attacking, levelling up and receiving damage.

---

## 🧠 Key Systems & Logic Implementations

### 🛡️ 1. Dynamic Protection Formula
Damage mitigation isn't static. It is calculated using a custom formula combining physical, biological, and environmental factors:
$$\text{Protection} = \text{Armor Protection} + \text{Natural Resistance Stat} + \text{Gender Modifier} + \text{Age Group Modifier}$$
* **Gender Modifiers:** Grant specific baseline defense points (+10 for Males, +8 for Females).
* **Age Bracket Modifiers:** Represent physical prime (+8 for ages 13–30, +7 for ages 30–60, and +6 for youth under 13 or seniors over 60).

### ⚔️ 2. Weapon Accuracy & Aim Math
Unlike standard RPGs where attacks always hit, this game uses weapon-specific thresholds combined with character attributes. Every attack performs a customized die roll compared against the player's `aim` stat:
* *Bow:* Must roll under $d10$ (high-difficulty, high-range).
* *Knife:* Must roll under $d4$ (easy-to-hit, low-range).

### 🎒 3. Strict Inventory Swap Algorithm
To enforce inventory management, the player's inventory contains a rigid **5-potion limit**. When a player attempts to pick up a 6th potion, the engine halts, triggers an interactive swap menu, handles potential input validation, and gracefully pops the selected old item to make room.

### 🎖️ 4. Large-Scale Strategic Army Warfare
The end-game transitions from individual combat into a tactical army simulator. The player commands the Resistance against King Jordan's royal guard.
* Commands depend on identifying structural **weak spots/blind spots** (Left, Right, Front) during enemy positioning shifts.
* Players must dynamically choose to strike weak spots for critical damage or execute a "Defend" order to mitigate incoming damage arrays.

### 🛠️ 5. Resilient Input Choice Engine
The custom interactive prompt (`Choice()`) features an exceptionally robust validator. It intercepts invalid user inputs (letters, blank returns, or integers out of range) without throwing traceback exceptions, utilizing recursive logic loops and input guard clauses to guarantee a crash-free experience.

### 🧪 6. Developer Admin Tools & Cheats
For debugging, entering the legacy cheat code `IDKFA` during character creation bypasses standard registration and generates a Max-Stats Administrator, while the built-in Developer Cheat Menu allows testing high-level late-game mechanics instantly.

---

## 🧪 Testing Suite

The code includes a robust automated test suite built with **Pytest** ensuring structural integrity.

### Prerequisites & Installation
Before running the tests, you need to install `pytest`. You can easily install it via `pip` by running the following command in your terminal:
```bash
pip install pytest
```
### Running the Tests   
To ensure interactive methods can be tested without freezing the terminal, the suite leverages **Monkeypatching** to mock stdin/stdout, verifying:
* Dynamic arithmetic of the protection formulas.
* Correct inventory item replacement when at maximum capacity.
* Resilience of the `Choice()` engine against malicious and invalid keyboard input arrays.

To run the automated tests, execute:
```bash
pytest test_project.py
```

## 🚀 How to Play

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/Wahrenha/your-repository-name.git](https://github.com/Wahrenha/your-repository-name.git)
    ```
2. **Execute the game** via your terminal:
    ```bash
    python project.py
    ```
3. **Follow the prompt instructions** and have fun!
