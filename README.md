# Terminal RPG in Python ⚔️🎲

A text-based RPG built from scratch in **Python**. Developed as a final project for Harvard's **CS50P: Introduction to Programming with Python**, the game features character creation, item management, stats and leveling systems, turn-based combat, an original story, and a choice system that changes the player's experience depending on the chosen paths, along with new mechanics implemented in the game to make it more dynamic and fun.

The project is divided between a file that keeps the classes on which the mechanics are based, and the main game file.

---

## ⚠️ Project Status Note
> **Development Status:** *Mechanics Complete / Story Work-in-Progress (WIP)*
> All core engines — including the turn-based combat system, dynamic shop logic, strict inventory memory buffers, leveling math, and large-scale army warfare algorithms — are **100% completed, fully optimized, and tested**. The main narrative campaign is playable up to the dramatic climax inside the King's secret fortress, with only final wrap-up story details currently in active writing.

---

## ⚙️ Core Classes & Modules

* **`Dice`:** Creates an $N$-sided physical die using Python's `random` module, processing game elements like accuracy, damage rolls, healing, and stat-checks.
* **`Armor`:** Handles armor attributes for different materials (Leather, Wood, Iron, Steel, Rebellion), mapping specific defense stats.
* **`Weapon`:** Represents the multiple weapons (Bow, Fireball Scroll, Sword, Mace, Knife, Army Sword) featured, applying damage by custom dice categories (e.g., Bow rolls a `d12`, while a Knife rolls a `d8`).
* **`Potions`:** Models consumable potions with unique effects (Healing, Strength, Quickness, Resistance, Super Healing), using custom combat boosts and automatic healing calculations.
* **`Classe`:** Sets baseline character archetypes (Archer, Wizard, Warrior, Ogre, Thief) and stores their starting statistical profiles.
* **`Character`:** The central object. It coordinates player metadata, dynamic stat updates, inventory, and core mechanics, such as attacking, leveling up, and receiving damage.

---

## 👥 The Character

* **Creation:** The character is created at the beginning of the game, when the player informs the guard of the protagonist's name, age, gender, and class.
* **Stats:** The stats are initially defined according to the class chosen, but whenever the player levels up, they are granted the choice of increasing one of them. Different classes have different advantages, and this is reflected in their stats (e.g., Ogres are the strongest, thieves are the most agile, etc.).
* **Inventory:** Items are stored in a dictionary that represents the character's inventory. Whenever the player picks up a new item, the game checks the current inventory to ensure it has not reached the limit for any of the items. There are also coins, which can be later used in the store to acquire many of the items available in the game. 
* **Level and XP:** Whenever the player beats an enemy, they gain a certain amount of XP depending on the opponent's difficulty. If upon defeating an enemy, the character reaches a specific threshold for each level, the player levels up, gaining more health and the choice to increase one stat.

---

## 🧠 Key Systems & Logic Implementations

### 🛡️ 1. Original Story

The story follows a villager who aims to combat the tyrannical government of King Jordan. After being previously arrested for alleged misbehavior, the protagonist escapes prison and counts on the help of many allies on the path to joining the resistance and defeating the Royal Forces.

### ⚔️ 2. Weapon Accuracy, Aim, and Protection
Unlike some RPGs where attacks always hit, this game uses weapon-specific thresholds combined with character attributes. Every attack performs a dice roll, and the result is compared against the player's `aim` stat:
* *Bow:* Must roll under $d10$ (high-difficulty, high-range).
* *Knife:* Must roll under $d4$ (easy-to-hit, low-range).

Damage mitigation is calculated using a formula combining physical factors with the armor the player possesses:
$$\text{Protection} = \text{Armor Protection} + \text{Natural Resistance Stat} + \text{Gender Modifier} + \text{Age Group Modifier}$$
* **Gender Modifiers:** Grant specific baseline defense points (+10 for Males, +8 for Females).
* **Age Bracket Modifiers:** Represent physical prime (+8 for ages 13–30, +7 for ages 30–60, and +6 for youth under 13 or seniors over 60).

### 🗺️ 3. Path-Changing Choices
As a true RPG, the game offers multiple paths and the opportunity to skip some parts of the game, such as battles and dialogues. Depending on the choices made by the player, the experience may differ in which opponents are faced or what items are obtained. The game also offers tips that can be granted through an intelligence roll with a threshold that varies depending on the character's intelligence stat. Some choices have such importance in the story that they may end the game at that very moment, interrupting the character's adventure.

### 🎒 4. Inventory Mechanics
The player's inventory contains a **5-potion limit**, along with one slot for armor and weapons. When a player attempts to pick up a 6th potion or another armor/weapon, the program blocks it, triggering an interactive swap menu that gives the player a choice to substitute a currently held item.

### 🎖️ 5. Large-Scale Army Battles
The end-game transitions from individual combat into a tactical army simulator. The player commands the Resistance against King Jordan's royal guard.
* Commands depend on identifying structural **weak spots/blind spots** (Left, Right, Front) during enemy positioning shifts.
* Players must choose to strike weak spots for critical damage or execute a "Defend" order to lower incoming damage.

### 👹 6. Special Encounters & Items
Some of the encounters in the game are different than the usual enemies and require their own battle mechanics, so they are implemented separately to give more creative freedom for those fights. There are also special items that are stronger and can only be obtained in the later sections of the game, such as the Rebellion armor and Super Healing potion (the strongest armor in the game, and a potion that heals the player back to full health, respectively).

### 🛠️ 7. Choice Function
The function (`Choice()`) features a useful interactive algorithm that serves as the base for the whole game. The program uses it for every decision the player must make, printing the options with their respective numbers and receiving the corresponding input for the player's choice. It also rejects invalid user inputs (letters, blank returns, or integers out of range) without throwing traceback exceptions to guarantee a crash-free experience.

### 🧪 8. Developer Admin Tools & Cheats
For debugging, using the cheat code `IDKFA` during character creation skips standard registration and generates a Max-Stats Administrator, while the built-in Developer Cheat Menu allows testing high-level late-game mechanics instantly.

---

## 🧪 Testing Suite

The code includes a robust automated test suite built with **Pytest** ensuring structural integrity.

### Prerequisites & Installation
Before running the tests, you need to install `pytest`. You can easily install it via `pip` by running the following command in your terminal:
```bash
pip install pytest
```

### Running the Tests   
To ensure interactive methods can be tested without freezing the terminal, the suite uses **Monkeypatching** to mock stdin/stdout.

To run the automated tests, execute:
```bash
pytest test_project.py
```

## 🚀 How to Play

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/Wahrenha/cs50p-Python-RPG.git](https://github.com/Wahrenha/cs50p-Python-RPG.git)
    ```
2. **Execute the game** via your terminal:
    ```bash
    python project.py
    ```
3. **Follow the prompt instructions** and have fun!
