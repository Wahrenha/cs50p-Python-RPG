# Terminal RPG in Python ⚔️🎲

A text-based RPG built from scratch in **Python**. Developed as a final project for Harvard's **CS50P: Introduction to Programming with Python**, the game features character creation, item management, stats and leveling systems, turn-based combat, an original story and a choice system that changes the player's experience depending on the chosen paths, along with new mechanics implemented in the game to make it more dinamic and fun.

The project is divided between a file that keeps the classes in which the mechanics are based in, and the main game file.

---

## ⚠️ Project Status Note
> **Development Status:** *Mechanics Complete / Story Work-in-Progress (WIP)*
> All core engines — including the turn-based combat system, dynamic shop logic, strict inventory memory buffers, leveling math, and large-scale army warfare algorithms — are **100% completed, fully optimized, and tested**. The main narrative campaign is playable up to the dramatic climax inside the King's secret fortress, with only final wrap-up story details currently in active writing.

---

## ⚙️ Core Classes & Modules

* **`Dice` Class:** Creates an $N$-sided physical dice using Python's `random` module, processing game elements like accuracy, damage rolls, healing and stat-checks.
* **`Armor` Class:** Handles armors attributes for different materials (Leather, Wood, Iron, Steel, Rebellion), mapping specific defense stats.
* **`Weapon` Class:** Represents the multiple weapons (Bow, Fireball Scroll, Sword, Mace, Knife, Army Sword) featured, applying damage by custom dice categories (ex: Bow rolls a `d12`, while a Knife rolls a `d8`).
* **`Potions` Class:** Models consumable potions with unique effects (Healing, Strength, Quickness, Resistance, Super Healing), using custom combat boosts and automatic healing calculations.
* **`Classe` Class:** Sets baseline character archetypes (Archer, Wizard, Warrior, Ogre, Thief) and stores their starting statistical profiles.
* **`Character` Class:** The central object. It coordinates player metadata, dynamic stat updates, inventory, and core mechanics, such as attacking, levelling up and receiving damage.

---

## The Character

* **Creation:** The character is created at the beginning of the game, when the player informs the guard the protagonist's name, age, gender and class.
* **Stats:** The stats are intially defined according to the class chosen, but whenever the player levels up, it is granted the choice of increasing one of them. Different classes have different advantages, and this is reflected in their stats (ex: Ogres are the strongest, thieves are the most agile, etc).
* **Inventory:** Items are stored in a dictionary that represents the character's inventory. Whenever the player picks up a new item, the game checks the current inventory to check if it has reached the limit for any of the items. There are also coins, that can be later used in the store to acquire many of the items avaiable in the game. 
* **Level and XP:** Whenever the player beats an enemy, they gain a certain amount of XP depending on the opponent's difficulty. If upon defeating an enemy, the character reaches a certain treshold, which is specific for each level, the player levels up, and is granted more health and the choice of one stat to upper.

---

## 🧠 Key Systems & Logic Implementations

### 🛡️ 1. Original Story
The Story follows a villager that aims to combat the tiranic government of King Jordan. After being previously arrested for allegedly misbehaviour, the protagonist escapes prision and counts with the help of many allies in the path to joining the resistance and defeating the Royal Forces.

### ⚔️ 2. Weapon Accuracy, Aim and Protection
Unlike some RPGs where attacks always hit, this game uses weapon-specific thresholds combined with character attributes. Every attack performs a dice roll and the result is compared against the player's `aim` stat:
* *Bow:* Must roll under $d10$ (high-difficulty, high-range).
* *Knife:* Must roll under $d4$ (easy-to-hit, low-range).

Damage mitigation is calculated using a formula combining physical factors with what armor the player possesses:
$$\text{Protection} = \text{Armor Protection} + \text{Natural Resistance Stat} + \text{Gender Modifier} + \text{Age Group Modifier}$$
* **Gender Modifiers:** Grant specific baseline defense points (+10 for Males, +8 for Females).
* **Age Bracket Modifiers:** Represent physical prime (+8 for ages 13–30, +7 for ages 30–60, and +6 for youth under 13 or seniors over 60).

### 3. Path-Changing Choices
As a true RPG, the game offers multiple paths and the opportunity to skip some parts of the game, such as battles and dialogues. Depending on the choices made by the player, the experience may differ in which opponents are faced or what items are obtained. The game also offers tips that can be granted through an intelligence roll with a treshold that varies depending on the character's intelligence stat. Some choices have such importance in the story that may end the game in the very moment, and interrupt the character's adventure.

### 🎒 4. Inventory Mechanics
The player's inventory contains a **5-potion limit**, along with one slot for armors and weapons. When a player attempts to pick up a 6th potion or another armor/weapon, the program blocks it, triggering an interactive swap menu, giving the player a choice to substitute a currently held item.

### 🎖️ 5. Large-Scale Army Battles
The end-game transitions from individual combat into a tactical army simulator. The player commands the Resistance against King Jordan's royal guard.
* Commands depend on identifying structural **weak spots/blind spots** (Left, Right, Front) during enemy positioning shifts.
* Players must choose to strike weak spots for critical damage or execute a "Defend" order to lower incoming damage.

### 6. Special Items and Encounters
Some of the encounters in the game are different than the usual enemies, and require their own battle mechanics, so they are implemented separetly to give more creative freedom for those fights. There are also special items, that are stronger and can only be obtained in the later section of the game, such as the Rebellion armor and Super Healing potion, the strongest armor in the game, and a potion the heals the player back to full health, respectively.

### 🛠️ 7. Choice Function
The function (`Choice()`) features an useful interative algorithm that is the base for the whole game. The program uses for every decision the player must make in the game, printing the options with their respective numbers, and receiving the correspondent input for the player's choice. It also rejects invalid user inputs (letters, blank returns, or integers out of range) without throwing traceback exceptions to guarantee a crash-free experience.

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