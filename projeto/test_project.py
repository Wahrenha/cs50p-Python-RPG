import pytest
from project import create_character, drink_potion, chest, player_action, battle, change_stats
from classes import Character, Armor, Weapon, Potions, Choice

#   This program tests the game to make sure the main funcions are not in error
#   it uses pytest with monkeypatch to test everything, including functions that depend on users input
#   it also mocks some functions to get expected outputs

@pytest.fixture
def character():
    # Creates a testcharacter, that can be used along the program
    return Character("Testcharacter", "Male", 25, "Warrior")

def inputs_tester(monkeypatch, list_inputs):
    #   The function that effectvely tests inputs 
    #   if it is necessary to press a button to continue, it recognizes it and returns "enter"
    inputs = iter(list_inputs)
    def mock_test(prompt):
        if "Press a button to continue" in prompt:
            return ""
        return next(inputs)
    monkeypatch.setattr('builtins.input', mock_test)


# Tests the protection calculations
def test_protection(character):

    assert character.protection == 38, "Error in base protection"

#   adds an armor to improve protection
    leather = Armor("Leather")
    character.inventory["Armor"] = leather
    character.protection = character.stats

    assert character.protection == 48, "Error in armor protection sum"

def test_healing_potion_logic(character):
#   Tests it the potions heal properly

    heal_potion = Potions("Healing")
    character.inventory["Potions"].append(heal_potion)

#   sets hp to 1 and calls drink potion
    character.hp = 1 
    drink_potion(character, heal_potion)

#   Checks the expected outcomes
    assert character.hp > 1, "Potion did not heal"
    assert len(character.inventory["Potions"]) == 0, "Potion was taken off the inventory"


def test_choice_resilience(monkeypatch):

#   Tests the choice function, making sure it doesnt take invalid inputs

#inputs list
    respostas = iter(["a", "5", "1"])

    # Forces the inputs in the list to the game
    monkeypatch.setattr('builtins.input', lambda _: next(respostas))

    # Calls the function and tests
    resultado = Choice("Test", "Correct option", "Other")

    assert resultado == "Correct option"


def test_create_character_flow(monkeypatch):

#   Emulates character creation using a list of inputs that answer the questions in create_character
#   inputs_tester handles the confirmations necessary in the clear_screen
 
    inputs = iter(["David", "1", "30", "3", "1"])

#   Tests the function with the inputs
    inputs_tester(monkeypatch, inputs)
    player = create_character()

# makes sure the character has the right name strength and money
    assert player.name == "David"
    assert player.classe.stats["strength"] == 6 
    assert player.inventory["Money"] == 0 

def test_inventory_full_replace(monkeypatch, character):

# Tests if the replace option when the inventory is full of potions work

# Fills the inventory  
    for _ in range(5):
        character.inventory["Potions"].append(Potions("Strength"))

    nova_pocao = Potions("Healing")

    # Replaces one of the potions for a healing
    inputs = iter(["1", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    character.take_item(nova_pocao)

    # Checks if healing made to the inventory
    tipos_pocoes = [p._type for p in character.inventory["Potions"]]
    assert "Healing" in tipos_pocoes

    # potions list length must still be 5
    assert len(character.inventory["Potions"]) == 5 

# Tests the chest
def test_chest(monkeypatch, character):

# Simulates the player taking an item, confirming and leaving the chest
    inputs = iter(["1", "1", "3"])
    inputs_tester(monkeypatch, inputs)

#   calls the function and asserts the inventory isnt empty
    chest(character)
    assert character.inventory['Money'] > 0
    assert character.inventory['Armor'] != None or character.inventory['Weapon'] != None or len(character.inventory['Potions']) > 0


# Resets the inventory and tries to take all the items in the chest
    character.inventory = "reset"

    inputs2 = iter(["3", "1", "2", "1", "1", "1"])

    # this mock function makes the chest "rigged", and alters the randint function to put specific items there, including 50 coins
    def mock_randint(a, b):
        if a == 1:
            match b:
                case 9:
                    return 1
                case 8:
                    return 5
                case 7:
                    return 7
        if a == 10 and b == 100:
            return 50
        return b
    
    monkeypatch.setattr("random.randint", mock_randint)
    inputs_tester(monkeypatch, inputs2)
    chest(character)

#   tests if the player took the items
    assert character.inventory['Money'] == 50
    assert character.inventory['Armor'].type == "Leather" 
    assert character.inventory['Weapon'].type ==  "Sword"
    assert character.inventory['Potions'][0].type == "Resistance" 


# Tests the player actions choices
def test_player_action(monkeypatch, character):

# Creates a weak opponent and sets the character aim to max
    opponent = Character("opp", "Male", 20, "Archer")
    change_stats(opponent, 0, 0, 0, 0, 0)
    initialhp = opponent.hp
    character.stats["aim"] = 100
    inputs = iter(["1", "1"])
    inputs_tester(monkeypatch, inputs)
    retorno = player_action(character, opponent)

#   after simulating and attack, asserts the opponent was damaged
    assert opponent.hp < initialhp
    assert retorno == "player attacked"

#  Makes randint always return 3 to make the run away dice roll always be true
    def mock_randint(a,b):
        return 3
    monkeypatch.setattr("random.randint", mock_randint)
    inputs = iter(["3", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado1 = player_action(character, opponent)

# Now makes it 1 so the dice roll is now always false
    def mock_randint(a,b):
        return 1
    monkeypatch.setattr("random.randint", mock_randint)
    inputs = iter(["3", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado2 = player_action(character, opponent)

# Tests if the runs were successful
    assert resultado1 == True
    assert resultado2 == False


# Finally tests if the outcomes of the battles were as expected
def test_battle(monkeypatch, character):

#   Forces a fatal attack from the player
    opponent = Character("opp", "Male", 20, "Archer")
    change_stats(opponent, 0, 0, 0, 0, 0)
    opponent.hp = 1
    character.stats["aim"] = 100
    inputs = iter(["1", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado = battle(character, opponent, xp=150)

#   asserts if the villain died and the player received the correcter amount of xp
    assert resultado == "Villain Died"
    assert character.inventory["XP"] == 150
