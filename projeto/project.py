# rpg pequeno, com batalhas, dados para definir a sorte, criação de personagem (classe personagem), opcoes de ações para o jogador, etc
#vai precisar do random, talvez pygame?, inflect, sys, Image, fpdf, re, requests, etc
#historia?
#classes de personagens(mago, arqueiro), cada uma com danos diferentes vidas diferentes
#classes: arqueiro, mago, guerreiro, ogro, ladrao
from classes import Dice, Armor, Weapon, Potions, Classe, Character, Choice, print_slow, unlister, accuracy
from time import sleep
import sys
import os
import textwrap
import random
import re

Sword = Weapon("Sword")
Fireball = Weapon("Fireball Scroll")
Mace = Weapon("Mace")
Knife = Weapon("Knife")
Bow = Weapon("Bow")
Army = Weapon("Army Sword")
Resistance = Potions("Resistance")
Strength = Potions("Strength")
Quickness = Potions("Quickness")
Healing = Potions("Healing")
Super = Potions("Super Healing")
Leather = Armor("Leather")
Wood = Armor("Wood")
Iron = Armor("Iron")
Steel = Armor("Steel")
Rebellion = Armor("Rebellion")

reset = "\033[0m"
red = "\033[31m"
green = "\033[92m"
orange = "\033[33m"
magenta = "\033[95m"
cyan = "\033[96m"
blue = "\033[94m"

class RestartGame(Exception):
    pass

def print_header(player=None, jumplines=True):
    print("=" * 80)
    print(f"{cyan}{'PYTHON TERMINAL RPG':^80}{reset} ", sep="")
    print("=" * 80)
    if player: 
        match player.classe.type:  
            case "Archer":
                emote = '🏹'
            case "Wizard":
                emote = '🧙‍♂️'
            case "Warrior":
                emote = '⚔️'
            case "Ogre":
                emote = '👹'
            case "Thief": 
                emote = '🕵️‍♀️'
            case _: 
                emote = 'erro'
        player_status = f"{emote}   {player.name} (Lvl {player.level}) | ❤️ HP: {player.hp}/{player.max_hp}"
        print(f"{player_status:^80}")
    
    if jumplines:
        print("-" * 80)
        print("\n")
    else:
        print("-" * 80, sep="")

def clear_screen(player=None, jumplines = True):
    input("Press a button to continue.")
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header(player, jumplines)

def display_hud(player : Character, villain : Character = None, mode="battle"):
    width = 80 
    weapon = player.inventory['Weapon'].type if player.inventory['Weapon'] else "None"
    armor = player.inventory['Armor'].type if player.inventory['Armor'] else "None"
    potions = len(player.inventory['Potions'])
    money = player.inventory['Money']

    match mode:
        case "battle":
            if not villain:
                raise ValueError("Battle HUD requires a villain!")
            p_name = f"👤 {player.name} ({player.classe})" if hasattr(player, 'classe') else f"👤 {player.name}"
            v_name = f"👹 {villain.name} ({villain.classe})"
            
            p_hp = f"❤️  HP: {player.hp}/{player.max_hp}"
            v_hp = f"❤️  HP: {villain.hp}/{villain.max_hp}"
            
            p_prot = f"🛡️  Protection: {player.protection}"
            v_prot = f"🛡️  Protection: {villain.protection}"
            
            p_pot = f"🧪 Potions: {len(player.inventory['Potions'])}/5"

            
            print(f"⚔️ {'BATTLE':^74} ⚔️")
            print("-" * width)
            print(f"{p_name:<38} │ {v_name:<38}")
            print(f"{p_hp:<38} │ {v_hp:<38}")
            print(f"{p_prot:<38} │ {v_prot:<38}")
            print(f"{p_pot:<38} │")
            print("=" * width)
            print("\n")

        case "commerce":
            print(f"{'SHOP':^80}")
            print("-" * width)
            print(f"👤 {player.name:<12} | 💰 {money} coins")
            print(f"⚔️  Weapon: {weapon:<10} | 🛡️  Armor: {armor:<10} | 🧪 Potions: {potions}/5")
            print("=" * width)
            print("\n")

        case "chest":
            print(f"{'CHEST':^80}")
            print("-" * width)
            print(f"👤 {player.name:<12} | 💰 {money} coins")
            print(f"⚔️  Weapon: {weapon:<10} | 🛡️  Armor: {armor:<10} | 🧪 Potions: {potions}/5")
            print("=" * width)
            print("\n")

        case "boss":
            if not villain:
                raise ValueError("Boss HUD requires a villain!")
            tamanho_barra = 20
            max_hp = villain.max_hp if villain.max_hp > 0 else 1 
            proporcao = max(0, villain.hp) / max_hp
            blocos_cheios = int(proporcao * tamanho_barra)
            blocos_vazios = tamanho_barra - blocos_cheios
            blocos_vermelhos = f"{red}{'█' * blocos_cheios}{reset}"
            blocos_vazios_str = "░" * blocos_vazios
            health_bar = f"[{blocos_vermelhos}{blocos_vazios_str}] {villain.hp}/{villain.max_hp} HP"
            p_name = f"👤 {player.name}"
            p_hp = f"❤️  HP: {player.hp}/{player.max_hp}"
            p_prot = f"🛡️  Protection: {player.protection}"
            p_pot = f"🧪 Potions: {len(player.inventory['Potions'])}/5"
            health_bar_size = 2 + tamanho_barra + 1 + len(str(villain.hp)) + 1 + len(str(villain.max_hp)) + 3
            espacos_esq = " " * ((80 - health_bar_size) // 2)
            text = f"{espacos_esq}{health_bar}"
            text2 = f"{villain.hp}/{villain.max_hp} HP"
            print(f"👑 {villain.name.upper():^74} 👑")
            print(f"{text}")
            print(f"{text2:^80}")
            print("=" * width)
            print(f"{p_name:<28} │ {p_prot:<28}")
            print(f"{p_hp:<28} │ {p_pot:<28}")
            print("-" * width)
            print("\n")

        case "final":   
            if not villain:
                raise ValueError("Boss HUD requires a villain!")
            tamanho_barra = 20

            v_max_hp = villain.max_hp if villain.max_hp > 0 else 1 
            r_max_hp = player.max_hp if player.max_hp > 0 else 1

            v_proporcao = max(0, villain.hp) / v_max_hp
            r_proporcao = max(0, player.hp) / r_max_hp

            r_blocos_cheios = int(r_proporcao * tamanho_barra)
            v_blocos_cheios = int(v_proporcao * tamanho_barra)

            r_blocos_vazios = tamanho_barra - r_blocos_cheios
            r_blocos_vermelhos = f"{red}{'█' * r_blocos_cheios}{reset}"
            r_blocos_vazios_str = "░" * r_blocos_vazios
            r_health_bar = f"[{r_blocos_vermelhos}{r_blocos_vazios_str}] {player.hp}/{player.max_hp} HP"

            v_blocos_vazios = tamanho_barra - v_blocos_cheios
            v_blocos_vermelhos = f"{red}{'█' * v_blocos_cheios}{reset}"
            v_blocos_vazios_str = "░" * v_blocos_vazios
            v_health_bar = f"[{v_blocos_vermelhos}{v_blocos_vazios_str}] {villain.hp}/{villain.max_hp} HP"

            r_health_bar_size = 2 + tamanho_barra + 1 + len(str(player.hp)) + 1 + len(str(player.max_hp)) + 3
            v_health_bar_size = 2 + tamanho_barra + 1 + len(str(villain.hp)) + 1 + len(str(villain.max_hp)) + 3

            r_espacos_esq = " " * ((80 - r_health_bar_size) // 2)
            v_espacos_esq = " " * ((80 - v_health_bar_size) // 2)

            text = f"{r_espacos_esq}{r_health_bar}"
            text2 = f"{player.hp}/{player.max_hp} HP"

            text3 = f"{v_espacos_esq}{v_health_bar}"
            text4 = f"{villain.hp}/{villain.max_hp} HP"
                        
            print(f"⚔️ {player.name.upper():^74} ⚔️")
            print(f"{text}")
            print(f"{text2:^80}")
            print("=" * width)

            print(f"👑 {villain.name.upper():^74} 👑")
            print(f"{text3}")
            print(f"{text4:^80}")
            print("=" * width)
            print("\n")


def drink_potion(character : Character,potion : Potions):

#   Checking if the character has the refered potion, and gets the index of the potion in the inventory

    if not potion in character.inventory["Potions"]:
        raise ValueError(f"\n{character.name} does not have {potion}")
    index = character.inventory["Potions"].index(potion)
    if not type(potion) == Potions:
        return False
#   Checks the potion type, to perform the effect
    print_slow(f"{character.name} drank {potion}")
    match potion._type:

        case "Healing":
            character.heal(potion.effect)
            potion_drank = "healing"

        case "Strength":
            character.stats["strength"] += potion.effect
            print(f"{magenta}Player's new strength is: {character.stats['strength']}{reset}\n")
            potion_drank = "strength"

        case "Quickness":
            character.stats["agility"] += potion.effect
            potion_drank = "quickness"
            print(f"{magenta}Player's new agility is: {character.stats['agility']}{reset}\n")

        case "Resistance":
            character.stats["resistance"] += potion.effect
            potion_drank = "resistance"
            character.protection = character.stats
            print(f"{magenta}Player's new resistance is: {character.stats['resistance']} and player's new protection is {character.protection}{reset}\n")

        case "Super Healing":
            max = character.max_hp
            hp = character.hp
            heal = max-hp
            character.heal(heal)
            potion_drank = "super healing"

#   Takes the potion out of the character's inventory

    character.inventory["Potions"].pop(index)
    return potion_drank


#Setting do and choice to None, so the function can be easily tested, by calling the function with the choices
def player_action(player, villain, choice=None, do = None, choice_2 = None, nk = False, run=True):

    d10 = Dice(10)
#   The player has the choices of Attack, open inventory and run
#   If player opens inventory, player can drink potion, or go back

    while True:
        choice_2 = None
        if not choice:
            if run:
                choice = Choice(f"{cyan}What will you do?", "Attack", "Open Inventory", "Run")
            else:
                choice = Choice(f"{cyan}What will you do?", "Attack", "Open Inventory")
        clear_screen(player,jumplines=False)
        display_hud(player, villain, mode="battle")
                        

        match choice:
#   If the player chose to attack, the attack method will be called

            case "Attack":
                if nk:
                    player.attack(villain, nk = True)
                else:
                    player.attack(villain)
                action = "player attacked"
                break

#   If the player chose to run, the player has a 1 in 5 chance to suceed

            case "Run":

                if d10.roll() == 3 or d10.roll() == 5:
                    return True

                else:
                    return False


#   If the player chose to open the inventory, the inventory will be printed

            case "Open Inventory":
                player.print_inventory()

#   Now, the player can choose between drinking a potion or going back
                if not do:


                    do = Choice("What will you do?", "Drink Potion", "Go Back")

                match do:

#   If the player chose to drink a potion, if the player has any potions, they will have to choose which potion to drink
                    case "Drink Potion":

                        action = "Player tried to drink potion"
                        if len(player.inventory["Potions"]) > 0:
                            if len(player.inventory["Potions"]) >= 1:
                                if not choice_2:
                                    player_potions = []
                                    for i in player.inventory["Potions"]:
                                        player_potions.append(i)
                                    if len(player_potions) > 0:
                                        clear_screen(player, jumplines=False)
                                        display_hud(player, villain, mode="battle")
                                        choice_2 = Choice("What potion do you want?", *player_potions, "Go Back")
                                        if choice_2 == "Go Back":
                                            choice = None
                                            do = None
                                            action = "Go Back"
                                            clear_screen(player, jumplines=False)
                                            display_hud(player, villain, mode="battle")
                                            continue
                                        index = player.inventory["Potions"].index(choice_2)
                                        if drink_potion(player, player.inventory["Potions"][index]) == False:
                                            print_slow("You do not have any potions", "Red")
                                            clear_screen(player, jumplines=False)
                                            display_hud(player, villain, mode="battle")
                                            continue
                                        break

                        else:
                            print_slow("You do not have any potions\n", "Red")
                            choice = None
                            do = None
                            action = "Go Back"
                            clear_screen(player, jumplines=False)
                            display_hud(player, villain, mode="battle")
                                            
                            continue

#   If player chose to go back, the player's action will not be over yet, and he will go back to initial choice
                    case "Go Back":
                        choice = None
                        do = None
                        action = "Go Back"
                        clear_screen(player, jumplines=False)
                        display_hud(player, villain, mode="battle")
                        continue
    return action


def battle(player, villain, xp, first = None):



    run = False
    pturn = f"{player.name}'s turn:\n".upper()
    vturn = f"{villain.name}'s turn:\n".upper()

#   The battle lasts while the player and oponnent are alive,
#   and first it is set who attacks first, according to agility
    stats = player.stats.copy()
    while not player.hp <= 0 and not villain.hp <= 0 and not run:
        if not first:
            if player.stats["agility"] < villain.stats["agility"]:
                first = "villain"
            elif player.stats["agility"] >= villain.stats["agility"]:
                first = "player"
        if first == "villain":
            clear_screen(player, jumplines=False)
            display_hud(player, villain)
            print(orange, vturn)
            sleep(2)
            villain.attack(player)
            if player.hp <= 0:
                break

            clear_screen(player, jumplines=False)
            display_hud(player, villain, mode="battle")
            print(cyan, pturn)
            sleep(2)
            Ran = player_action(player,villain)
            if Ran == True:
                print_slow("You ran away", "Green")
                run = True
            elif Ran == False:
                print_slow("You tried to run away, but failed.", "Red")

        elif first == "player":
        
            if player.hp <= 0 or villain.hp <= 0:
                break
            clear_screen(player, jumplines=False)
            display_hud(player, villain, mode="battle")
            print(cyan, pturn)
            sleep(2)
            Ran_2 = player_action(player, villain)
            if Ran_2 == True:
                print_slow("You ran away", "Green")
                sleep(1)
                run = True
            elif Ran_2 == False:
                print_slow("You tried to run away, but failed.", "Red")

            if not villain.hp <= 0 and Ran_2 != True:
                clear_screen(player, jumplines=False)
                display_hud(player, villain, mode="battle")
                print(orange, vturn)
                sleep(2)
                villain.attack(player)
        first = None


    if player.hp <= 0:
        game_over(player)
    elif villain.hp <= 0:
        player._stats = stats
        player.protection = player.stats
        clear_screen(player)
        player.get_xp(xp)
        d50 = Dice(50)
        n = d50.roll()
        player.take_item(f"{n} coins")
        clear_screen(player)
        return "Villain Died"
    else:
        player._stats = stats
        player.protection = player.stats
        return "Ran away"


def create_character(name = None, gender = None, age = None, classe = None):

    #print_slow("Hello traveler, it is quite uncommon to see someone wandering around here...\n\n\n")

    while True:
        try:

#   Getting the name of the character, the name must have only letters, and it is optional to have two names
#   Those conditions are secured by the re.search use
            if not name:

                name = input("Hello prisoner, what's your name? ").strip()

                if name == "IDKFA": 
                    print("\nCheat mode enable...")
                    player = Character("Admin", "Male", 30, "Warrior")
                    player.take_item("5000 coins")
                    player.stats["strength"] = 50
                    return player
                name = name.title()
                _name  = re.search(r"([A-Z]{1}[a-z]+(?: [A-Z]{1}[a-z]+)?)", name)
                if not name == _name.group(1):
                    raise ValueError
                break

            else:
                break
        except (ValueError, AttributeError):
            print_slow("That does not seem to be a name \n\n")
            name = ""
            continue



    while True:
        try:

#   Then, the function gets the gender, which must be chosen by typing the number according to the option:
#   Type 1 for Male, and 2 for Female
            if not gender:
                gender = int(input(f"\nWhat's your gender?\n{blue}[1] Male\n{magenta}[2] Female\n\n{reset}"))
                sleep(0.5)
                if gender > 2 or gender < 1:
                    raise ValueError
                match gender:
                    case 1:
                        _gender = "Male"
                    case 2:
                        _gender = "Female"
                break
            else:
                _gender = gender
                break
        except (ValueError, TypeError):
            print("\n\nThat does not seem to be a valid gender (Type the number equivalent to your gender)")
            gender = None
            continue

    while True:
        try:

#   Now setting the age, only ages between 10 and 80 are accepted

          if not age:
                sleep(0.5)
                age = int(input("\nWhat's your age? "))
                sleep(0.5)

                if age < 10 or age > 80:
                    raise ValueError
                break
          else:
              break

        except:
            print("I'm sorry, but that does not seem to be your age")
            age = None
            continue

    while True:

        clear_screen()
#   Finally setting the class of the character, the player must choose between the existant classes
        if not classe:
            sleep(0.5)
            aclasse = Choice("To what class do you belong prisoner?", "Archer 🏹", "Wizard 🧙‍♂️", "Warrior ⚔️", "Ogre 👹", "Thief 🕵️‍♀️")
            sleep(0.5)
            classe, a = aclasse.split(" ")
            classe_chosen = Classe(classe)
            print(f"\n{classe_chosen.properties(classe)}")
            sleep(1)
            clear_screen()
            classe_chosen.print_stats()
            sleep(3)
            take = Choice("Are you sure?", "Yes", "No")
            if take == "Yes":
                _classe = classe
                break
            else:
                classe = None
                continue
        else:
            _classe = classe
            break

# Setting the player according to the info collected, and returning it

    player = Character(name, _gender, age, _classe)
    return player

def change_stats(character: Character, s, agi, i, r, aim, level=None):
    character.stats = {
                    "strength" : s,
                    "agility" : agi,
                    "inteligence" : i,
                    "resistance" : r,
                    "aim" : aim
                       }
    character.protection = character.stats
    if level:

        character.level_up(level,want_print=False)
    return character.stats, level

def chest(player):
    itens = [Sword, Fireball, Mace, Bow, Knife, Resistance, Healing, Strength, Leather]
    content = []
    for i in range(3):
        number = random.randint(1,len(itens))
        number -= 1
        content.append(itens[number])
        num = itens.index(itens[number])
        itens.pop(num)
    a = unlister(content).strip("[],")
    clear_screen(player, jumplines=False)
    display_hud(player, mode="chest") 
    print_slow(f"You open the chest.", "Magenta")
    sleep(2)   
    item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], content[1], content[2],  "leave chest")
    l = 0
    clear_screen(player, jumplines=False)
    
    while True:


        if item_show == "leave chest":
            break

        sleep(0.5)
        print(f"\n{item_show.properties()}")
        sleep(1)

        take = Choice("\nWill you take it?", "Yes", "No")
        if take == "Yes":
            took = player.take_item(item_show)
            i = content.index(item_show)
            if took: content.pop(i)
            l += 1
            clear_screen(player, jumplines=False)
            display_hud(player, mode="chest")
            if l == 1:
                item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], content[1], "leave chest")
            if l == 2:
                item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], "leave chest")
            if l == 3:
                break

        else:
            clear_screen(player, jumplines=False)
            display_hud(player, mode="chest")
            if l == 0:
                item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], content[1], content[2],  "leave chest")
            if l == 1:
                item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], content[1], "leave chest")
            if l == 2:
                item_show = Choice(f"{magenta}CHEST CONTENT:", content[0], "leave chest")
            if l == 3:
                break
        clear_screen(player)
    coins = random.randint(10,100)
    coins = str(coins)
    player.take_item(f"{coins} coins")
    print(reset)

def purchases(player, item_dict):
    options_list = [f"{item}: {price} coins" for item, price in item_dict.items()]
    options_list.append("Go Back")
    clear_screen(player, jumplines=False)
    display_hud(player, mode="commerce")
    choice_str = Choice("Select an item to buy:", *options_list)
    clear_screen(player, jumplines=False)
    display_hud(player, mode="commerce")
    if choice_str == "Go Back":
        return
    
    selected_item = None
    selected_price = 0

    for item, price in item_dict.items():
        if f"{item}: {price} coins" == choice_str:
            selected_item = item
            selected_price = price
            break

    if selected_item:
        if player.inventory["Money"] >= selected_price:
            confirm = Choice(f"Buy {selected_item} for {selected_price} coins?", "Yes", "No")
            if confirm == "Yes":
                took = player.take_item(selected_item)
                if took:
                    player.inventory["Money"] -= selected_price
                    print_slow(f"Transaction successful! Remaining balance: {player.inventory['Money']}", "Green")
        else:
            print_slow("You don't have enough money!", "Red")

def commerce(player):

    armor = {Leather: 60, Wood: 80, Iron: 140}
    potions = {Resistance: 40, Strength: 20, Quickness: 40, Healing: 60}
    weapons = {Sword: 50, Fireball: 50, Mace: 40, Knife: 20, Bow: 50}

    items = [weapons, potions, armor]

    while True:
        clear_screen(player, jumplines=False)
        display_hud(player, mode="commerce")
        cat_choice = Choice("What are you looking for?", "Weapons", "Potions", "Armors", "Go Back")
        match cat_choice:
            case "Weapons":
                purchases(player, weapons)
            case "Potions":
                purchases(player, potions)
            case "Armors":
                purchases(player, armor)
            case "Go Back":
                break
        clear_screen(player, jumplines=False)

def jack_battle(jack, player, text):

    damage = jack.damage()
    pro = round(player.protection/10)
    pro = int(pro)
    damage = int(damage)
    damage_taken = damage -  pro
    if damage_taken < 0: damage_taken = 0
    fail = False
    clear_screen(player, jumplines=False)
    display_hud(player, jack, mode="boss")
    print(f"{orange}\n\n{jack.name} tries to attack {player.name}{reset}")
    sleep(1)

    if jack.inventory["Weapon"]:
        if not accuracy(jack, jack.inventory["Weapon"]):
            print(f"{jack.name} failed")
            sleep(1)
            fail = True

    if not fail:

        if damage_taken >= player.hp:
            player.take_damage(player.hp - 1)
            print_slow(f"{player.name} lost.", 'Red')
            return "L"
        else:
            player.take_damage(damage_taken)


    while True:
        clear_screen(player, jumplines=False)    
        display_hud(player, jack, mode="boss")
        action = player_action(player, jack, nk=True)
        if action == True or action == False:
            print_slow("You can't run away from this fight.", 'Blue')
        else:
            break

    if text:
        clear_screen(player, jumplines=False)    
        display_hud(player, jack, mode="boss")
        print_slow(f"Jack: \n\n{text}", 'Orange')

def trainfight(player):
    jack = Character("Jack", "Male", 15, "Warrior")
    jack.take_item(Sword, want_print=False)
    jack.take_item(Leather, want_print=False)
    change_stats(jack, 5, 5, 3, 4, 5, 2)
    print_slow("Jack:\nI'M SO EXCITED! HERE I GO!", 'Orange')
    jack_sentences = ["Nice one", "That was crazy", "Hey! you are actually a great fighter", "You must teach me how to fight sometime", "That was amazing!", "Well done!"]
    winner = None
    while True:
        if jack.hp > 1:
            if len(jack_sentences) >= 1:
                numer = random.randint(0, len(jack_sentences) - 1)
                sentence = jack_sentences[numer]
                jack_sentences.remove(sentence)
            else:
                sentence = "..."
            if jack_battle(jack, player, sentence) == "L":
                winner = "Jack"
                break
            else:
                continue
        else:
            print_slow(f"{player.name} won!", 'Green')
            winner = "Player"
            break

    if winner == "Player":
        sleep(3)
        print_slow("Jack: \n\nWOW! That was awesome! Totally deserved, Thank you sooo much!!!", 'Orange')
        clear_screen(player)
        sleep(2)
        print_slow("Jack: \n\nHere you go!! The coins I promised, and take these healing potions too, to recover from the fight!", 'Orange')
        clear_screen(player)
        sleep(2)
        player.take_item(Healing)
        player.take_item(Healing)
        if Healing in player.inventory["Potions"]:
            drink_potion(player, Healing)
        if Healing in player.inventory["Potions"] and player.hp < player.max_hp - 3:
            drink_potion(player, Healing)
        sleep(2)
        player.take_item("70 coins")
        clear_screen(player)
        print_slow("Jack: \n\nWell, see you around traveller! Nice to meet you!\n\n", 'Orange')
        clear_screen(player)
    elif winner == "Jack":
        clear_screen(player)
        sleep(3)
        print_slow("Jack: \nWOW! That was awesome! Thank you sooo much!!!", 'Orange')
        clear_screen(player)
        sleep(2)
        print_slow("Jack: \nI guess I'm actually stronger than I thought right hahahaha!", 'Orange')
        sleep(2)
        print_slow("Jack: \nHere you go!! Take these healing potions to recover from the fight!", 'Orange')
        clear_screen(player)
        sleep(2)
        player.take_item(Healing)
        player.take_item(Healing)
        if Healing in player.inventory["Potions"]:
            drink_potion(player, Healing)
        if Healing in player.inventory["Potions"] and player.hp < player.max_hp - 3:
            drink_potion(player, Healing)
        sleep(2)
        clear_screen(player)
        print_slow("Jack: \nWell, see you around traveller! Nice to meet you! Better luck next time!")
        clear_screen(player)

def guard_battle(player):
    general = Character("General Pippen", "Male", 50, "Warrior")
    general.take_item(Steel, want_print=False)
    general.take_item(Army, want_print=False)
    general.take_item(Healing, want_print=False)
    change_stats(general, 12, 8, 5, 12, 11, 15)
    clear_screen(player)
    print_slow("General Pippen:\n\n-YOU ARE DONE TRAVELLER YOUR TIME IN THIS WORLD IS UP!", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    action_1 = player_action(player, general, nk=True)
    if action_1 == True or action_1 == False:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n-YOU REALLY THINK YOU CAN GET AWAY??", "Red")
    else:
        print_slow("General Pippen:\n\n-YOU ARE WEAK TRAVELLER, THERE IS NOTHING YOU CAN DO AGAINST ME!", "Red")
    
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    print_slow("General Pippen:\n\n-I WILL END YOU PRETTY SOON TRAVELLER, BUT I LIKE PLAYING WITH MY FOOD HAHAHAHAHAH \n- BE CAREFUL WITH YOUR STEPS", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    action_2 = player_action(player, general, nk=True)
    if action_2 == True or action_2 == False:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n-YOU FOOL, THERE IS NO GOING BACK!", "Red")
    else:
        print_slow("General Pippen:\n\n-DON'T YOU REALISE?? YOU ARE DOOMED!", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    print_slow("General Pippen:\n\n-I AM JUST SUPERIOR TO YOU TRAVELLER, YOU CAN'T EVEN SCRATCH MY ARMOR", 'Red')
    clear_screen(player)
    display_hud(player, general, mode="boss")
    print_slow(f"{general.name} tries to attack {player.name}", 'Red')
    damage = round(player.hp/2)
    player.take_damage(damage)
    print_slow("General Pippen:\n\n-STILL THINK YOU CAN BEAT ME, TRAVELLER?", 'Red')
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    action_3 = player_action(player, general, nk=True)
    if action_3 == True or action_3 == False:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n-YOU CANNOT GET AWAY!", "Red")
    else:
        print_slow("General Pippen:\n\n-HAAHAHAHAHAHAHAHAHAHAHAHAHA", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    action_4 = player_action(player, general, nk=True)
    if action_4 == True or action_4 == False:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n-...", "Red")
    else:
        print_slow("General Pippen:\n\n-...", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    action_5 = player_action(player, general, nk=True)
    if action_5 == True or action_5 == False:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n- ", "Red")
    else:
        print_slow("General Pippen:\n\n- ", "Red")
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    if player_action(player, general, nk=True) == True:
        print_slow("You try to run away, but the general outpaces you", "Orange")
        print_slow("General Pippen:\n\n-That's enough traveller", "Red")
    else:
        print_slow("General Pippen:\n\n-That's enough traveller", "Red")
    clear_screen(player, jumplines=False) 
    display_hud(player, general, mode="boss")
    general.take_item(Super, want_print=False)
    drink_potion(general, Super)
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    print_slow(f"{general.name} tries to attack {player.name}")
    damage = player.hp - 1
    player.take_damage(damage)
    clear_screen(player, jumplines=False)
    display_hud(player, general, mode="boss")
    print_slow("General Pippen:\n\n-It's over, it was an honorable fight traveller, but your time is up", "Red")
    print_slow("The General raises his sword, and your journey is over.", "Blue")
    clear_screen(player, jumplines=False)
    sleep(3)
    print_slow("However you hear a strange sound.", "Blue")
    sleep(2)
    print_slow("You look up and see tens of arrows that fly towards the General.", "Blue")
    sleep(2)
    print_slow("You see as he barely dodges and runs away, and a wind of hope crosses you.", "Blue")
    clear_screen(player, jumplines=False)

def final_battle(player):
    kingattack = ["\nThe Royal Archers suddenly start shooting at the resistance.\n", "\nThe King's Ogre squad out of nowhere started throwing rocks from the walls of the fortress.\n", "\nThieves from the kingdom suddenly appeared at the fight in the King's side, and are now attacking the resistance.\n"]
    happened = ["\nResistance Archers are shooting the right side of the army.\n", "\nResistance Wizards are shooting fireballs at the left side of the army.\n", "\nThe Resistance Cavalry is attacking the back of the army.\n", "\nYou overhear the opposite commandant ordering a powerful attack.\n"]
    rounds = 0
    resistance_army = Character("The Resistance", "Male", 30, "Warrior")
    resistance_army.max_hp = 1000
    resistance_army.hp = 1000

    king_army = Character("Jordan's Army", "Male", 30, "Warrior")
    king_army.max_hp = 1000
    king_army.hp = 1000

    armysblindspot = ""
    damage = 0
    rdamage = 0
    reduce_d = 0
    pattack = False
    d150 = Dice(150)
    d100 = Dice(100)
    d70 = Dice(70)
    d50 = Dice(50)
    d20 = Dice(20)
    while resistance_army.hp > 0 and king_army.hp > 0:
        if rounds != 0 and rounds%3 == 0:
            event = kingattack[random.randint(0,2)]
            print_slow(event, "Red")
            event_damage = 0
            while event_damage < 30:
                event_damage = d70.roll()
            resistance_army.hp -= event_damage
            print_slow(f"The Resistance suffered {event_damage} damage.", "Red")

        damage = 0
        if pattack:
            while damage < 70:
                damage = d150.roll()
            pattack = False
        else:
            while damage < 20:
                damage = d70.roll()
        rdamage = 0
        clear_screen(player, jumplines=False)
        display_hud(resistance_army, king_army, mode="final")
        choice = Choice(f"{cyan}What will you do?", "Attack the left", "Attack the right", "Attack the front", "Defend")
        clear_screen(player, jumplines=False)
        display_hud(resistance_army, king_army, mode="final")
        match choice:
            case "Attack the left":
                if armysblindspot == "Left":
                    while rdamage < 70:
                        rdamage = d150.roll()
                    print_slow("You hit the army's weak spot, causing more damage.", "Green")
                else:
                    while rdamage < 20:
                        rdamage = d70.roll()
                print_slow("Your troops attack succesfully through the left side of the opposite army\n\n", "Green")
                king_army.hp -= rdamage
                print_slow(f"The attack dealt {rdamage} damage\n\n", "Green")
            case "Attack the right":
                if armysblindspot == "Right":
                    while rdamage < 70:
                        rdamage = d150.roll()
                    print_slow("You hit the army's weak spot, causing more damage.", "Green")
                else:
                    while rdamage < 20:
                        rdamage = d70.roll()
                print_slow("Your troops attack succesfully through the right side of the opposite army\n\n", "Green")
                king_army.hp -= rdamage
                print_slow(f"The attack dealt {rdamage} damage\n\n", "Green")
            case "Attack the front":
                if armysblindspot == "Front":
                    while rdamage < 70:
                        rdamage = d150.roll()
                    print_slow("You hit the army's weak spot, causing more damage.", "Green")
                else:
                    while rdamage < 20:
                        rdamage = d70.roll()
                print_slow("Your troops attack succesfully through the front side of the opposite army\n\n", "Green")
                king_army.hp -= rdamage
                print_slow(f"The attack dealt {rdamage} damage\n\n", "Green")
            case "Defend":
                reduce_d = 0
                while reduce_d < 20:
                    reduce_d = d70.roll()
                if reduce_d > damage:
                    damage = 0
                else:
                    damage -= reduce_d
                print_slow("Your troops defend themselves from the opponent's attack, mitigating the damage\n\n", "Green")
        happen = happened[random.randint(0,3)]
        if resistance_army.hp > 0 and king_army.hp > 0:
            resistance_army.hp -= damage
            print_slow("The royal army strikes the resistance with an attack.", "Red")
            print_slow(f"The resistance army suffered {damage} damage.\n", "Red")
            sleep(1.5)
            if resistance_army.hp > 0 :
                print_slow(happen, "Green")
        match happen:
            case "\nResistance Archers are shooting the right side of the army.\n":
                armysblindspot = "Left"
            case "\nResistance Wizards are shooting fireballs at the left side of the army.\n":
                armysblindspot = "Right"
            case "\nThe Resistance Chivalry is attacking the back of the army.\n":
                armysblindspot = "Front"
            case "\nYou overhear the opposite commandant ordering a powerful attack.\n":
                armysblindspot = ""
                pattack = True

        sleep(1.5)
        #print(frases[rounds])
        rounds += 1
    if king_army.hp <= 0:
        sleep(2)
        print_slow("The resistance defeated the army, and is now raiding the fortress, with the commanders leading the way.", "Cyan")
        sleep(3)
    elif resistance_army.hp <= 0:
        sleep(2)
        clear_screen()
        print_slow(f"\n\n{red}The Resistance was defeated, and all the survivors were executed.{reset}")
        game_over(player)

    clear_screen(player)
    print_slow("You are the leader of one of the squads in the raid, and you see villagers running for their lives.", "Orange")
    sleep(2)
    print_slow(f"John:\n\n-{player.name} stay here, stand your ground, my squad will be going in first.", "Orange")
    print_slow("You follow John's orders and, alongside other squads, you watch the gates of the fortress.", "Blue")
    sleep(2)
    print_slow("-AAAHHHHHH", "Green")
    sleep(1)
    print_slow("HAHAHAHAHAHHAHAH! YOU REALLY THOUGHT IT WAS OVER JOHN?", "Red")
    sleep(1)
    print_slow("As you hear those voices, you rush to the fortress, and make your way in the main room of the castle.", "Orange")
    sleep(1)
    print_slow("You enter the room, and see tens of soldiers from both sides laying dead on the ground, and in the very center, John with a sword in his chest as General Pippen and King Jordan, the only ones alive in the room, laugh at him", "Orange")
    sleep(2)
    print_slow("Other commanders of the Resistance also arrive in the room, and you are now filled with rage", "Red")
    sleep(1)
    d30 = Dice(30)
    general = Character("General Pippen", "Male", 50, "Warrior")
    general.take_item(Steel, want_print=False)
    general.take_item(Army, want_print=False)
    general.take_item(Healing, want_print=False)
    change_stats(general, 12, 8, 5, 12, 11, 15)
    roundgeneral = 1
    falas = ["Is that all you got? You pigs!", "You really think you can take me?", "My army is coming, they will end you. If I don't do that first...", "How many more are coming? You are not enough to fight me!", "HAHAHAHAH Good try!"]
    while general.hp > 0:
        clear_screen(player, jumplines=False)
        display_hud(player, general, mode="boss")
        player_action(player, general, run=False)
        if general.hp <= 0:
            break
        clear_screen(player, jumplines=False)
        display_hud(player, general, mode="boss")
        if roundgeneral % 3 == 0:
            print_slow("The resistance commanders join forces to attack the general\n", "Blue")
            dam = d30.roll()
            general.take_damage(dam)
            clear_screen(player, jumplines=False)
            display_hud(player, general, mode="boss")

        if general.hp <= 0:
            break
        if roundgeneral % 2 == 0:
            print_slow(falas[random.randint(0,4)], "Red")
        clear_screen(player, jumplines=False)
        display_hud(player, general, mode="boss")
        general.attack(player)
        if player.hp <= 0:
            game_over(player)
        roundgeneral += 1

def story_1():
    clear_screen()
    print_slow("A long, long time ago, when the countries were not yet formed, and the nations as we know today didn't even exist, the world was composed of small villages and reigns. The Kingdom of the East was one of the most prominent in the continent, being ruled by the ruthless and brilliant mind of King Jordan, who expanded his kingdom to many lengths.", "Blue")
    print_slow("Although King Jordan had plenty success with his plans of domination and expansion, he had a big amount of enemies, people who were seeking to overthrow him at all costs. \n\nKing Jordan started to become paranoid of such actions, and took immediate caution to arrest those involved.", "Blue")
    clear_screen()
    print_slow("However, not all of those arrested had something to do with the threats of coups, and lots of innocent people and political enemies were imprisioned as well.", "Blue")
    print_slow('Alongside some friends, you, a villager with much more knowledge of combat than the usual citizen of the kingdom, found yourself in one of those prisons, sentenced unfairly to treason, for simply trying to protect a friend who was being arrested.', "Blue")
    print_slow('You wait in what seems like an infinite line to the much awaited day of working outside, when you finally reach the guard.', "Blue")
    clear_screen()
    player = create_character()
    return player

def story_2(player):
    clear_screen(player)
    print_slow("Just as expected, there it is. The knife you bought from the prison's dealer was outside in the hidden spot he chose.", "Blue")
    player.take_item(Knife)
    print_slow("As you leave the building to the fenced area outside, you spot a breach. A hole in the fence, in a part which was only being watched by one single guard. And the perfect chance to take him out.", "Blue")
    print_slow("You approach the guard, with your knife at your back, pretending to look for information, and jump him.", "Orange")
    guard = Character("guard", "Male", 40, "Thief")
    guard.take_damage(6,want_print=False)
    guard.take_item(Knife, want_print=False)
    change_stats(guard, 2,2,2,2,2,1)
    battle(player, guard, 50, first = "player")
    print_slow("After taking the guard out, you run without looking backwards, as fast as you can towards a forest nearby. The large amount of trees seems to hide you well and there you find a small cabin in the wild.", "Blue")
    print_slow("You try to look inside, but there is nothing to see. You turn around feeling defeated, and hear a sound in a bush by the side of the house.", "Blue")
    print_slow("An old man walks out of the trees, with what seems like a fascinated look to your face, an open mouth and a huge knife in his hands.", "Orange")
    clear_screen(player)
    print_slow("Stranger:\n\n-What? A prisoner??", "Green")
    print_slow("-Come in fast, don't let them see ya.", "Green")
    clear_screen(player)
    print_slow("You enter the cabin, it is small but very comfortable. There is a bed with a large chest on its side and what seems to be a kitchen in the other side of the room.", "Blue")
    print_slow("Stranger:\n\n-Have a look in the chest, there might be something to help you, and then sit down so I can give you a couple of healing potions. Drink one now, you look rough. Take the other with you.", 'Green')
    chest(player)
    print_slow("Stranger:\n\n-Here, take the healing potion.\n", 'Green')
    healing = Potions("Healing")
    player.take_item(healing)
    player.take_item(healing)
    if healing in player.inventory["Potions"]:
        drink_potion(player, healing)
    if player.hp < 12 and healing in player.inventory["Potions"]:
        drink_potion(player, healing)
    clear_screen(player)
    print_slow("Stranger:\n\n-Now leave. You shouldn't be here, do not tell anyone about this. You should head north where you will find the headquarters of the resistance army. Good luck!", 'Green')
    clear_screen(player)
    sleep(1)

def story_3(player):
    print_slow("You leave the cabin and start heading north, feeling restored with the help of the old man and decided to fight the king with everything you got.", "Blue")
    print_slow("The forest is not an easy path and the trees hold you back along the way. \nSuddenly you hear some noise in the back.", "Orange")
    bandit = Character("Bandit", "Male", 25, "Thief")
    knife = Weapon("Knife")
    bandit.take_item(knife, want_print = False)
    change_stats(bandit, 2, 2, 3, 0, 3)
    bandit.take_damage(3, want_print = False)
    result = battle(player, bandit, 200, first="villain")
    if result == "Villain Died":
        print_slow("You won the battle against the bandit. Feeling stronger, you keep going in your journey.", "Blue")
    else:
        print_slow("You escaped the bandit and kept going on your way.", "Blue")
    print_slow("Moving forward, you eventually stumble upon a fork in the way.", "Blue")
    clear_screen(player)
    sleep(2)
    w_roll = Choice("Roll for intelligence to investigate the paths?", "Yes", "No")
    if w_roll == "Yes":
        intelligence = player.stats["inteligence"]
        intel_dice = Dice(intelligence)
        i_roll = intel_dice.roll()
        clear_screen(player)
        sleep(2)
        print_slow("The roll's result was: ", 'Blue', jumpline=False)
        sleep(2)
        print_slow(f"{i_roll}\n", 'Blue')
        sleep(1)
        if i_roll >= 5:
            print_slow("You succeeded!", "Green")
            sleep(2)
            print_slow("You look more closely, and notice huge yet subtle footsteps, leading to the left way.", 'Blue')
            sleep(2)
        else:
            print_slow("You failed!", "Red")
            sleep(2)
            print_slow("You investigate both ways, but do not see anything notable.", 'Blue')
            sleep(2)
    clear_screen(player)
    way = Choice("\n\nWhich way will you go?", "Right", "Left")
    clear_screen(player)
    match way:
        case "Right":
            print_slow("You walk slowly through the dark woods, and you hear something moving.", "Orange")
            sleep(1)
            print_slow("As you approach the source of the sounds, you find a", "Orange", jumpline=False)
            sleep(2)
            print_slow(" Chest", "Orange")
            sleep(2)
            chest(player)
            print_slow("You keep moving through the forest hopeful to find the resistance, but as it is late at night, you decide to get some rest.", "Blue")
            sleep(2)
            print_slow("You pass the night feeling scared of noises of the forest, and do not manage to sleep well.", "Blue")
            sleep(1)
            print_slow("However, you still wake up feeling quite recovered", "Green")
            clear_screen(player)
            sleep(1)
            d8 = Dice(8)
            roll = d8.roll()
            player.heal(roll)


        case "Left":
            print_slow("You follow a little source of light coming from the left way, and move through narrow spaces between trees.", "Blue")
            print_slow("As you come closer to the light, you realize that it is actually fire, that belonged to some campers.", "Orange")
            clear_screen(player)
            sleep(2)
            print_slow("You hear a sound and", "Orange", jumpline=False)
            sleep(0.5)
            print_slow(".", "Orange", jumpline=False)
            sleep(0.5)
            print_slow(".", "Orange", jumpline=False)
            sleep(0.5)
            print_slow(".", "Orange")
            sleep(0.5)
            print_slow(f"An ogre jumps you", 'Red')
    
            ogre = Character("ogre", "Male", 40, "Ogre")
            change_stats(ogre, 4, 1, 1, 6, 4)
            mace = Weapon("Mace")
            ogre.take_item(mace, want_print = False)
            battle(player, ogre, 500,first = "villain")
            print_slow("Feeling tired after the fight, you decide to get some rest in the ogre tent and sleeps through the night.", "Blue")
            sleep(2)
            print_slow("The fire and the calm of the tent makes you feel comfortable and safe, and you have a nice sleep.", "Blue")
            sleep(1)
            print_slow("You wake up feeling entirely recovered.\n", "Green")
            clear_screen(player)
            d12 = Dice(12)
            roll = d12.roll()
            player.heal(roll)

def story_4(player):

    print_slow("You walk.", 'Blue', jumpline=False)
    sleep(1)
    print_slow(" A lot.", 'Blue')
    sleep(2)
    print_slow("The journey is really getting to your head, and the sight of the trees are starting to get obnoxious.", 'Blue')
    clear_screen(player)
    sleep(2)
    print_slow("Stranger:\n\n-HEY! YOU THERE!", "Orange")
    sleep(2)
    print_slow("Stranger:\n\n-HEY! SLOW DOWN! I WANT TO OFFER YOU SOMETHING!", 'Orange')
    sleep(1)
    clear_screen(player)
    print_slow("You wait for the stranger to get to you.", 'Blue')
    sleep(3)
    print_slow("Stranger:\n\n-HELLO! MY NAME IS JACK! DO YOU WANT TO FIGHT ME?", 'Orange')
    sleep(1)
    clear_screen(player)
    print_slow("Jack:\n\n-I know it sounds weird, but I really need to learn to fight. I will give you gold if you beat me, 70 coins, do we have a deal?", 'Orange')
    sleep(2)
    fight = Choice("", "Yes", "No")
    clear_screen(player)
    if fight == "Yes":
        print_slow("Jack:\n\n-Let's do it then!", 'Orange')
        trainfight(player)
    else:
        print_slow("Jack:\n\n-That is a shame, i'll keep looking around.", 'Orange')

    print_slow("You pack your things and continue your journey.", "Blue")
    print_slow("After about a mile walking, you see the two ways converge, and a sign that had an arrow pointing forward and 1 Mile written below.", "Blue")
    print_slow("Curious as to what it meant, you take that direction, and you discover that it was actually a trader that worked in that forest.", "Blue")
    clear_screen(player)
    sleep(2)
    print_slow("Trader:\n\n-Hello traveler, may I help you with anything?", "Orange")
    print_slow("\n-I have all kinds of items, if you'd wanna have a look.", "Orange")
    sleep(2)
    print_slow("Trader:\n\n-The path upon you is tough, I'd take a look at the armors if I were you.", "Orange")
    commerce(player)
    clear_screen(player)
    print_slow("Trader:\n\n-If I were ya I would be careful from now on, drink some potions right now, just a tip.", "Orange")
    while True:
        if len(player.inventory["Potions"]) > 0:
            if len(player.inventory["Potions"]) >= 1:
                player_potions = []
                for i in player.inventory["Potions"]:
                    player_potions.append(i)
                if len(player_potions) > 0:
                    choice_2 = Choice("What potion do you want to drink?", *player_potions, "Go Back")
                    if choice_2 == "Go Back":
                        choice = None
                        do = None
                        action = "Go Back"
                        break
                    index = player.inventory["Potions"].index(choice_2)
                    if drink_potion(player, player.inventory["Potions"][index]) == False:
                        print_slow("You do not have any potions", "Red")
                        break
                    break
                else:
                    print_slow("You do not have any potions\n", "Red")
                    do = None
                    break
        else:
            print_slow("You do not have any potions\n", "Red")
            choice = None
            do = None
            action = "Go Back"
            break

    clear_screen(player)
    print_slow("After your encounter with the trader, you keep going on, until you find a three way fork in the way.", "Blue")
    sleep(2)
    w_roll = Choice("Roll for intelligence to investigate the paths?", "Yes", "No")
    clear_screen(player)
    if w_roll == "Yes":
        intelligence = player.stats["inteligence"]
        intel_dice = Dice(intelligence)
        i_roll = intel_dice.roll()
        sleep(2)
        print_slow("The roll's result was: ", 'Blue', jumpline=False)
        sleep(2)
        print_slow(f"{i_roll}\n", 'Blue')
        sleep(1)
        if i_roll >= 5:
            print_slow("You succeeded!", "Green")
            sleep(2)
            print_slow("You look more closely, and notice something weird.", 'Blue')
            sleep(2)
            print_slow("You see some coins dropped in the northeast direction.", 'Blue')
            sleep(2)
            print_slow("You look to the north way and feel a strange sensation, a unatural aura.", 'Blue')
            sleep(2)
            print_slow("However, the northwest direction seem strangely empty.", 'Blue')
        else:
            print_slow("You failed!", "Red")
            sleep(2)
            print_slow("You investigate, but do not see anything notable.", 'Blue')
            sleep(2)
    clear_screen(player)
    way = Choice("Which way are you heading?", "Northeast", "North", "Northwest")
    clear_screen(player)
    match way:
        case "Northeast":
            sleep(2)
            print_slow("You head northeast and you find a very bright little town.", "Blue")
            print_slow("For the amount of stores and houses, you figure it is way too empty, but you do not fear it.", "Blue")
            print_slow("However, as you keep walking, you hear a voice.", "Orange")
            clear_screen(player)
            sleep(2)
            print_slow("Stranger:\n\n-Look a traveller!", "Magenta")
            print_slow("Hey you! hand your items right now or you will regret it.","Magenta")
            print_slow("You look back and see 3 thieves. They don't look very threatening, but they outnumber you.", "Orange")
            clear_screen(player)
            choice = Choice("What will you do?", "Fight them", "Hand your items")
            clear_screen(player)
            match choice:
                case "Fight them":
                    thief_1 = Character("Thief 1", "Male", 20, "Thief")
                    thief_1.take_item(Knife, want_print=False)
                    change_stats(thief_1, 4, 5, 9, 10, 7)
                    battle(player, thief_1, 200)
                    print_slow("Thief:\n\n-NOOOO WHAT DID YOU DO!", "Red")
                    thief_2 = Character("Thief 2", "Male", 20, "Thief")
                    thief_2.take_item(Knife, want_print=False)
                    change_stats(thief_2, 3, 4, 9, 10, 7)
                    battle(player, thief_2, 200)
                    print_slow("Thief:\n\n-WHAT, HOW CAN YOU DO THAT?? YOU ARE DEAD NOW!", "Red")
                    thief_3 = Character("Thief 3", "Male", 20, "Thief")
                    thief_3.take_item(Knife, want_print=False)
                    change_stats(thief_3, 3, 3, 9, 10, 7)
                    battle(player, thief_3, 300)
                    sleep(2)
                    print_slow("You defeated your enemies, but are still feeling wounded.", "Blue")
                    sleep(2)
                case "Hand your items":
                    xp = player.inventory['XP']
                    inventory = {
                        'Armor' : None,
                        'Weapon' : None,
                        'Potions' : [],
                        'Money' : 0,
                        'XP' : xp
                    }
                    player.inventory = inventory
                    player.print_inventory()
                    sleep(2)
                    print_slow("Thief:\n\n-HAHA! YOU LOSER!", "Red")
                    sleep(2)
                    print_slow("They walk away with all the items you fought hard to conquer.", "Blue")
                    clear_screen(player)


        case "North":
            sleep(2)
            print_slow("You head north through a tough way in the forest. It looks very suspicious.", "Blue")
            print_slow("You keep moving until you hear some weird noises.", "Orange")
            print_slow("You stop to investigate and you actually hear a conversation, but see no one.", "Orange")
            clear_screen(player)
            sleep(2)
            print_slow("Stranger:\n\n-That is our last chance, we have to get him or our boss will kill us, we have no choice.", "Magenta")
            clear_screen(player)
            sleep(2)
            print_slow("Out of nowhere two masked wizards materialize in front of you, looking a bit frightened, but determined", "Magenta")
            print_slow("The younger one approaches you first.", "Blue")
            clear_screen(player)
            y_wiz = Character("Younger Wizard", "Male", 18, "Wizard")
            y_wiz.take_item(Fireball, want_print=False)
            battle(player, y_wiz, 150)
            print_slow("Older Wizard:\n\n-WHAT..? NOOO!! YOU KILLED MY SON", "Red")
            print_slow("The second wizard jumps straight into you and their mask drops revealing an adult woman, with tears of anger in her face.", "Blue")
            old_wiz = Character("Wizard", "Female", 30, "Wizard")
            old_wiz.take_item(Fireball, want_print=False)
            battle(player, old_wiz, 400)
            sleep(2)
            print_slow("You defeated your enemies, but are still feeling wounded.", "Blue")
            sleep(2)
            print_slow("You cannot help but feel bad for the family you just defeated, but you know you have to carry on.", "Blue")
            print_slow("You know the end is near.", "Orange")
            clear_screen(player)
        case "Northwest":
            sleep(2)
            print_slow("You head northwest and find a clear path in front of you, and suddenly feel like you're being followed.", "Blue")
            sleep(1)
            print_slow("This feeling follows you through the empty path and you start to feel paranoid about some forest noises.", "Blue")
            sleep(1)
            print_slow("You walk a lot and then you finally see it.", "Blue")
            sleep(1)
            print_slow("As you approach a suspicious tree that has an arrow stuck in it, you know what to do.", "Blue")
            sleep(1)
            print_slow("However...", "Orange")
            clear_screen(player)
            sleep(2)

    if way != "Northwest":
            print_slow("You keep going on in your journey, and ultimately head west in the forest path.", "Blue")
            print_slow("You walk a lot, and start feeling tired.")
            sleep(1)
            print_slow("Everything around you starts to spin and suddenly, it is all black.", 'Blue')
            sleep(3)
            print_slow("You wake up in the next day, feeling a bit recovered!\n", "Cyan")
            clear_screen(player)
            d6 = Dice(6)
            player.heal(d6.roll())
            sleep(2)
            print_slow("As you walk you hear noises, and what seems like two people talking in the back.", 'Orange')
            sleep(2)
            print_slow("Not sure if you are going insane, you keep on walking.", 'Orange')
            sleep(2)
            print_slow("However...", "Orange")
            clear_screen(player)
            sleep(2)
    print_slow("Two guards come out from behind the trees behind you.", "Orange")
    print_slow("You recognize their armor, they are a part of the high ranked army that responds only to the king himself.", "Orange")
    clear_screen(player)
    sleep(2)
    print_slow("General:\n\n-THAT'S IT! WE KNEW YOU WOULD LEAD US TO THE RESISTANCE YOU FOOL!", "Red")
    print_slow("High rank guard:\n\n-You really thought you could get away like that prisoner? We've been following you since the very start.", "Red")
    print_slow("-Surrender now prisoner and we will spare you for getting us all the way here.", "Red")
    clear_screen(player)
    sleep(2)
    print_slow("You think back through your journey. You are close, very close, you know that, but the opponents look stronger than you.", "Blue")
    print_slow("You consider every option, but you have to make the ultimate choice.", "Blue")
    clear_screen(player)
    do = Choice("What will you do?", "Surrender", "Fight")
    clear_screen(player)
    match do:
        case "Surrender":
            sleep(2)
            print_slow("You get on your knees, with your hands on your head, and get taken away without resistance.", "Red")
            print_slow("\n\nYou surrendered and got back to the prison.", "Red")
            game_over(player)
            #end game
        case "Fight":
            print_slow("You find the courage to fight and resist.\n", "Cyan")
            sleep(2)
            print_slow("General:\n\n-HAHA! He thinks he can fight us... Go on Gray, take him down already.", "Red")
            sleep(2)
            print_slow("The smaller and lower ranked guard comes to you, with his sword held up.", "Red")
            gray = Character("Gray", "Male", 25, "Warrior")
            gray.take_item(Army, want_print=False)
            gray.take_item(Iron, want_print=False)
            change_stats(gray, 6, 6, 4, 8, 10, 3)
            battle(player, gray, 500)
    guard_battle(player)
    sleep(2)
    print_slow("Stranger:\n\n-Hello traveller, we have been expecting you.", "Green")
    sleep(3)
    print_slow("Resistance archer:\n\n-Here, have this potions.\n", "Green")
    clear_screen(player)
    player.take_item(Super)
    player.take_item(Super)
    if Super in player.inventory["Potions"]:
        drink_potion(player, Super)
    sleep(2)
    clear_screen(player)
    print_slow("Resistance soldier:\n\nHey! You fought with a lot of bravery! Defeating Gray was very impressive, but you are no longer alone!", "Green")
    print_slow("\nGray actually carried a letter written by the king himself, and it has a stamp showing the king's secret location. This is our golden chance!!", "Green")
    sleep(2)
    clear_screen(player)
    print_slow("Resistance soldier:\n\nCome with us traveller, we will take you to our headquarters, where you can get some rest and then join our council, this will be a very important one.", "Green")
    clear_screen(player)
    sleep(3)
    print_slow("You take some days to rest and get to know the headquarters. \n\nYou see the training fields and all the gear they have, and start to feel very confident about victory.", "Blue")

def story_5(player):
    clear_screen(player)
    sleep(3)
    print_slow("The day of the council arrives, and you know that you are very requested", "Blue")
    sleep(2)
    print_slow("Resistance soldier:\n\nHey! Let's go, they are already waiting!", "Green")
    sleep(1)
    print_slow("You follow him, and enter a very large room, with a ginormous table in the middle, and about 10 people around it, all equipped with very strong armors.", "Blue")
    sleep(2)
    print_slow(f"Resistance leader:\n\n{player.name}! We have been expecting you! I'm John, the leader of the Resistance! Sit down! We have some things to talk about!", "Green")
    sleep(1)
    print_slow(f"John:\n\nAs we all know, {player.name} has done great things to get to us, and even getting us our most prized information: the king's location.", "Green")
    clear_screen(player)
    print_slow(f"John:\n\nTherefore, {player.name} has earned the right to join this council, as one of the commanders of the resistance! Here son, take this!\n", "Green")
    sleep(1)
    player.take_item(Rebellion)
    clear_screen(player)
    sleep(2)
    print_slow(f"John:\n\nThis shall keep you safer from your enemies! Welcome {player.name}! But now, let's talk strategies.", "Green")
    sleep(3)
    print_slow("You feel very accomplished for becoming a commander, and you and the council discuss the strategies of the invasion for hours on end.", "Blue")
    sleep(1)
    print_slow("Eventually, it is decided, the resistance will invade the king's secret fortress in 2 days, and you are in charge of commanding the infantry.\n\n", "Blue")
    clear_screen(player)
    sleep(5)
    print_slow("The day of the battle arrives. The troops are all ready, marching to the battlefield.\n", "Blue")
    print_slow("You could not be more nervous. This is what it all comes to, the final battle for freedom.", "Blue")
    clear_screen(player)
    sleep(2)
    print_slow("As one of the commanders, you ride your horse, leading your troops, and you finally identify the fortress.", "Orange")
    print_slow("You are leading the frontline, so it is time to begin the attacks.", "Orange")
    sleep(2)
    print_slow("And now you cannot run.", "Red")
    sleep(3)
    clear_screen(player)
    final_battle(player)

def story_end(player):
    
    clear_screen(player)
    print_slow("General Pippen falls down in the stone cold floor...", "Blue")
    print_slow("The room goes completely silent. King Jordan is no longer laughing and he takes a step back.", "Orange")
    clear_screen(player)
    print_slow("King Jordan:\n\nPippen...", "Orange")
    sleep(2)
    print_slow("King Jordan:\n\nOld friend, they got you. I cannot leave it like this!", "Orange")
    clear_screen(player)
    print_slow("King Jordan tries to attack ", "Orange")
    sleep(0.5)
    print_slow("You disarm King Jordan before he can raise his sword!", "Green")
    print_slow("The King falls to the floor, desperately looking for a weapon he can defend himself with", "Blue")
    clear_screen(player)
    print_slow("Suddenly, the King's face closes, and he looks reckless.", "Orange")
    print_slow("King Jordan:\n\nYou won son, deal with me as you must. You are a great warrior, you could do a great general, now that Pippen is gone...", "Orange")
    sleep(2)
    print_slow("Your sword is pointing to his face as the entire room is staring at you, waiting for your decision.", "Orange")
    clear_screen(player)
    
    
    # O grande menu de decisão usando a sua função Choice
    decisao_final = Choice(
        "What will you do?",
        "Accept Jordan's offer",
        "Arrest Jordan and let the people decide his fate",
        "Execute him."
    )
    clear_screen(player)
    match decisao_final:
        case "Accept Jordan's offer":
            print_slow("You retrieve your sword and offer your hand to the King.", "Green")
            print_slow("Jordan smiles, and gladly takes your hand", "Green")
            clear_screen(player)
            print_slow("However, as his hand grabs yours, you feel a blood fluid in your back", "Orange")
            clear_screen(player)
            print_slow("You realize it is blood as you remove the arrow that hit you.", "Red")
            clear_screen(player)
            print_slow(f"Resistance Commander:\n\nI'm sorry {player.name}, but you really thought you could betray us?", "Red")
            clear_screen(player)
            print_slow("You look around, and none of your soldiers approach to help.", "Red")
            print_slow("You can only watch as the commander executes King Jordan in front of you.", "Red")
            clear_screen(player)
            print_slow("And then, it all turns black.", "Red",jumpline=False)
            print(". ", end="")
            sleep(1)
            print(". ", end="")
            sleep(1)
            print(". ")
            sleep(1)
            return False
            
        case "Arrest Jordan and let the people decide his fate":
            print_slow("The commander:\nThat ends now Jordan.", "Red")
            print_slow("As he draws his sword, you raise your arms, and everybody stops.", "Red")
            sleep(2)
            print_slow("You:\n\nThe King is defeated. We do not have the right to decide his fate. Let the people judge him for his crimes.", "Orange")
            clear_screen(player)
            print_slow("The commander advances towards you, but your soldiers surround him.", "Red")
            print_slow("You signal to your soldiers, that quickly handcuff him and take him away, along with the commander.", "Blue")
            print_slow("You take the fallen crown in your hand, more uncertain than ever about the future.", "Blue")
            return True
        
        case "Execute him.":
            print_slow("You see Jordan in the floor and John is all you think about.", "Red")
            print_slow("You are filled with rage...", "Red")
            clear_screen(player)
            print_slow("You:\n\nYou killed him. You showed no mercy. This ends now.", "Red")
            clear_screen(player)
            print_slow("You raise your sword and drop it right in Jordan's chest.", "Red")
            print_slow("The dead king's face turn completely white as the whole room stares at what you did.", "Red")
            print_slow("You pick up the fallen crown. Everyone fears you now.", "Red")
            return True

def main_menu():

    while True: 
        clear_screen(jumplines=False)
        print(cyan, end="")
        print(f"{'MAIN MENU':^80}")
        line = "-"*80
        choice = Choice(f"{line}", "Start Game", "How to play", "Credits", "Exit") 
        match choice:
            case "Start Game":
                break
            case "How to play":
                clear_screen()
                print(magenta)
                text = "This is an interactive terminal RPG. Your actions are made through choices during the game, where you select your desired options pressing the respective number."
                text2 = "The game features a turn-based combat, and has multiple paths you can engage in, according to the choices you make throughout the adventure."
                text3 = "Make sure to manage your items well, and choose your actions wisely! GLHF!"
                            
                ftxt = textwrap.fill(text, width=80)
                ftxt2 = textwrap.fill(text2, width=80)
                ftxt3 = textwrap.fill(text3, width=80)

                print(ftxt, "\n")
                print(ftxt2, "\n")
                print(ftxt3, "\n")

            case "Credits":
                print(orange)
                clear_screen()
                print(orange)
                text = "This game was fully developed by me, Victor Wahrendorff, including the story and all the mechanics."
                text2 = "Check my other projects in github.com/Wahrenha !"

                ftxt = textwrap.fill(text, width=80)
                ftxt2 = textwrap.fill(text2, width=80)

                print(ftxt, "\n")
                print(ftxt2, "\n")

            case "Exit":
                sys.exit("\nThank you for playing! Hope you enjoyed your experience!")
            
def game_over(player, won=False):
    clear_screen(None, jumplines=False)
    message = f"This is the end of {player.name}'s story"
    
    if won:
        print(green, end="")
        print(f"{'CONGRATULATIONS!!':^80}")
    else:
        print(red, end="")
        print(f"{'GAME OVER':^80}")
    print("="*80)
    print(f"{message:^80}")
    print(f"{'Thank you for playing, feel free to play again anytime!':^80}")
    print("-"*80)
    clear_screen(None)
    continua = Choice("What now?", "Play again", "Exit")
    match continua:
        case "Play again":
            raise RestartGame()
        case "Exit":
            sys.exit("Thank you for playing!")


    #adicionar menu principal para começo do jogo e pra quando morrer

    #attack options outros itens pra ajudar no combate (bomba(?), faca pra arremessar, )
    # pegar um turno pra estrategizar (aumenta o dano pelo valor da rolagem em inteligencia), imobilizar(?) se rolagem em forca for sucesso, da pouco dano mas impede o proximo ataque
    #protect?
    #Habilidade especiais:
        #warrior: furia (dobra o dano do proximo ataque)
        # Thief: stealth (vc fica indetectavel, o proximo ataque do inimigo nao te afeta e vc da 50% mais dano)
        #  Ogre: xxx (seus proximos tres ataques causam 30% mais dano, mas os proximos dois do inimigo te causam 30% a mais tbm)
        #  Wizard: weakness spell (o inimigo da 50% menos dano nos proximos tres turnos)
        #  Archer: Sharpenss arrow ( vc corre para tras e usa flechas maiores e mais afiadas. o inimigo gasta um turno pra chegar ate voce e seus proximos tres ataques atravessam protecoes)

    #balance classes

    # format right the texts
# compactar codigo no final

#print the current round

def main():
    print(cyan) 
    print("=" * 80)
    print(f"{'Welcome!':^80}")
    print("This is a Terminal RPG made from scratch in Python as the final project for CS50p.")
    print("This game was made with a lot of care, and I hope you enjoy your experience.")
    print(f"{'Have fun!':^80}")
    print("=" * 80, reset)
    while True:
        try:
            main_menu()
            player = story_1()
            story_2(player)
            story_3(player)
            story_4(player)
            story_5(player)
            venceu = story_end(player)
            game_over(player, won=venceu)
        except RestartGame:
            continue

if __name__ == "__main__":
    main()