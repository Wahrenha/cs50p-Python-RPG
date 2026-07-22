from time import sleep
import sys
import random
import os

#This code stores the classes for the game
#The classes are Dice, Weapon, Potions, Classe, and Character

reset = "\033[0m"
red = "\033[31m"
green = "\033[92m"
orange = "\033[33m"
magenta = "\033[95m"
cyan = "\033[96m"
blue = "\033[94m"

DEBUG_MODE = True

def clear_screen():
    input("Press a button to continue.")
    os.system('cls' if os.name == 'nt' else 'clear')


class Dice:

    #Dice init method receives n as argument, with n being the number of sides for the dice
    def __init__(self, n):
        self.sides = n

    #defining the number of sides of the object
    @property
    def sides(self):
        return self._sides
    @sides.setter
    def sides(self, n):
        if type(n) == int:
            self._sides = n

    #finally, implementing the roll function for the dice, and returning the random number
    def roll(self):
        roll = random.randint(1,self.sides)
        return roll

class Armor:

#Weapon init method receives the name of the weapon, which will be used to define the atributtes of the object
    #The weapon must be one of 5 options: Bow, Spell, Sword, Mace, or Knife
    def __init__(self, armor):
        self.type = armor

    #Weapon str method will return what weapon the object is, which will be stored in weapon.type
    def __str__(self):
        return f"{self.type} Armor"

    #_type method stores the weapon type, that being which weapon it is in the available options
    @property
    def _type(self):
        return self.type
    @_type.setter
    def _type(self, armor):
        if not armor in ["Leather", "Wood", "Iron", "Steel", "Rebellion"]:
            raise ValueError("Inexistant armor")
        self.type = armor

    def protection(self):
        armor = self.type
        protection = 0
        match armor:
            case "Leather":
                protection = 10
            case "Wood":
                protection = 20
            case "Iron":
                protection = 30
            case "Steel":
                protection = 40
            case "Rebellion":
                protection = 50

        return protection

    def properties(self):
        weapon = self._type
        match weapon:
            case "Leather":
                properties = "A very fragile armor, but certainly better than nothing."
            case "Wood":
                properties = "A decent armor, offers good protection."
            case "Iron":
                properties = "A good armor, can be the difference between life or death in a battle."
            case "Steel":
                properties = "A great armor, can protect you even from the most damaging attacks."
            case "Rebellion":
                properties = "An amazing armor, it will make you feel untouchable in the battlefield."
        return properties



#Setting a Weapon class, to store information related to the weapons
class Weapon:

    #Weapon init method receives the name of the weapon, which will be used to define the atributtes of the object
    #The weapon must be one of 5 options: Bow, Spell, Sword, Mace, or Knife
    def __init__(self, weapon):
        self.type = weapon

    #Weapon str method will return what weapon the object is, which will be stored in weapon.type
    def __str__(self):
        return f"{self.type}"

    #_type method stores the weapon type, that being which weapon it is in the available options
    @property
    def _type(self):
        return self.type
    @_type.setter
    def _type(self, weapon):
        if not weapon in ["Bow", "Fireball Scroll", "Sword", "Mace", "Knife", "Army Sword"]:
            raise ValueError("Inexistant weapon")
        self.type = weapon

    #damage method stores the damage of the weapon, dependent of the weapon type. The damage will be a dice roll

    def damage(self):

        d4 = Dice(4)
        d6 = Dice(6)
        d8 = Dice(8)
        d10 = Dice(10)
        d12 = Dice(12)
        damage = 0
        weapon = self.type

        match weapon:
            case "Bow":
                damage = d12.roll()
            case "Fireball Scroll":
                damage = d12.roll()
            case "Sword":
                damage = d10.roll()
            case "Mace":
                damage = d10.roll()
            case "Knife":
                damage = d8.roll()
            case "Army Sword":
                damage = d10.roll()
        return damage
#   Finally, Weapon properties describes the weapon types
#   Weapon properties should be called only when presenting the weapons for the character

    def properties(self):
        weapon = self._type
        match weapon:
            case "Sword":
                properties = "A versatile weapon, which mixes agility and strength. Very useful for warriors."
            case "Fireball Scroll":
                properties = "A piece of magic, which causes a big explosion and damages your oponnents. Best for wizards"
            case "Mace":
                properties = "A huge and high damaging weapon, takes a lot of strength to use. Perfect for ogres."
            case "Knife":
                properties = "A subtle but tricky weapon, best for fast and stealth attacks. Very recommended for thieves."
            case "Bow":
                properties = "A high range, and technical weapon, also causes a lot of damage. Wonderful for Archers."
        return properties





#Seting also a Potions class to store info for the potions

class Potions:

    #Potions init method, similarly to Weapon class, receives the potion type as argument
    #potion argument must be one of 4 options: Healing, Strength, Quickness, or Resistance
    #other informations for the potion depends directly of the potion type

    def __init__(self, potion):
        self._type = potion
        self.effect = potion

    #Potions str method returns the type of the potion, which will be one of the options of potions

    def __str__(self):
        return f"{self._type} Potion"

    #Storing the type of the weapon, and verifying if the argument for the init method is valid

    @property
    def _type(self):
        return self.type
    @_type.setter
    def _type(self, potion):
        if not potion in ["Healing", "Strength", "Quickness", "Resistance", "Super Healing"]:
            raise ValueError("Inexistant Potion")
        self.type = potion

    #Effect method will define and store the effect of the potion, being dependent of the type of the potion

    @property
    def effect(self):
        return self._effect
    @effect.setter
    def effect(self, potion):

        d4 = Dice(4)
        d16 = Dice(16)
        d20 = Dice(20)

        match potion:
            case "Healing":
                self._effect = 0
                while self._effect < 8:
                    self._effect = d16.roll()
            case "Strength":
                self._effect = d4.roll()
            case "Quickness":
                self._effect = d4.roll()
            case "Resistance":
                self._effect = d20.roll()
            case "Super Healing":
                self._effect = "Max"


    #Finally, just as Weapon properties, Potion properties describes the potions types
    #Potions properties should be called only when presenting the potions for the character

    def properties(self):
        potion = self._type
        match potion:
            case "Healing":
                properties = "This potion will heal your injuries and get you brand new!"
            case "Strength":
                properties = "This potion will make you stronger and ready do fight!"
            case "Quickness":
                properties = "This potion will make you fast and agile, you will be faster than your oponnent!"
            case "Resistance":
                properties = "This potion will make you super resistant, you won't feel a thing!"
        return properties


#The Classe class (kinda redundant sorry lol) stores the initial information for the character dependant of its class

class Classe:

#   Classe init method receives classe as argument, which should be one of the classes options:
#   Archer, Wizard, Warrios, Ogre, or Thief
#   All of the Classes information depends of classe

    def __init__(self, classe):
        if not classe in ["Archer","Wizard","Warrior","Ogre","Thief"]:
            raise ValueError("Inexistant class")
        self.stats = classe
        self.hp = classe

#   Classe str method returns the stats and hp related to each of the classes
#   This method will probably not be used, but it is here just in case

    def __str__(self):
        return f"{self.stats}, {self.hp}"

#   stats method stores and defines the stats for each class
#   Those will be the initial stats for every level 1 character

    @property
    def stats(self):
        return self._stats
    @stats.setter
    def stats(self, classe):
        match classe:
            case "Archer":
                stat = {
                    "strength" : 4,
                    "agility" : 4,
                    "inteligence" : 8,
                    "resistance" : 15,
                    "aim" : 10
                        }
            case  "Wizard":
                stat = {
                    "strength" : 4,
                    "agility" : 5,
                    "inteligence" : 10,
                    "resistance" : 15,
                    "aim" : 8
                        }
            case "Warrior":
                stat = {
                    "strength" : 6,
                    "agility" : 3,
                    "inteligence" : 7,
                    "resistance" : 20,
                    "aim" : 6
                        }
            case "Ogre":
                stat = {
                    "strength" : 6,
                    "agility" : 1,
                    "inteligence" : 5,
                    "resistance" : 20,
                    "aim" : 6
                        }
            case "Thief":
                stat = {
                    "strength" : 4,
                    "agility" : 5,
                    "inteligence" : 9,
                    "resistance" : 15,
                    "aim" : 7
                        }

        self._stats = stat

    def print_stats(self):

        statline = self.stats
        print(green,"\n\nClass's stats:\n")
        for i in statline:
            print(i.strip("'").strip().capitalize(), ":", statline[i])
        print(reset)

#   hp method stores max hp for each class
#   Those will be the max hp for character's of each class in level 1

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, classe):
        match classe:
            case "Archer":
                self._hp = 16
            case "Wizard":
                self._hp = 16
            case "Warrior":
                self._hp = 18
            case "Ogre":
                self._hp = 18
            case "Thief":
                self._hp = 16


#   Finally, the properties method also defines and stores the properties and info for each class
#   This should be presented to the player when choosing the character's classe

    def properties(self, classe):
        match classe:
            case "Archer":
                return "Archers are great distance shooters, which makes them very good attackers, but also fragile."
            case "Wizard":
                return "Wizards use their enviable magic to cast spells which may cause a very large damage. They are also quiet fragile."
            case "Warrior":
                return "Warriors are tough, they mix resistance and strength to the limit, but lack the speed and inteligence to make it perfect."
            case "Ogre":
                return "Ogres are dumb strong creatures. If you ever see one, do not stand on its way!"
            case "Thief":
                return "Thieves are stealthy and quiet, very agile and can be very tricky."




#Character class is the most important of all.
#it stores all the information about the character in one single place

class Character():

#   First of all, the init method takes 4 arguments, other than self:
#   Name: the name of the character;
#   Gender: The gender of the character, between Male and Female, with upper first letters;
#   Age: The age of the character
#   classe (the only in lower to not conflict with the class Classe): The character class

#   The init method also call most of the setter methods of the Character, based on its class
#   Worth noting:
#       self.protection takes Classe.stats because it is dependent of the stat Resistance;
#       self.level is initially set to 1;
#       self.inventory takes a random string, because whatever it takes, the inventory will initially be the same

    def __init__(self, Name, Gender, Age, classe):
        self.name = Name
        self.gender = Gender
        self.age = Age
        Class = Classe(classe)
        self.classe = Class
        self.stats = Class.stats
        self.level = 1
        self.max_hp = Class.hp
        self.hp = Class.hp
        self.inventory = "inventory"
        self.protection = self.stats

#   Character's str method returns all the information on the object
    def __str__(self):
         return f"Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Protection: {self.protection}, HP: {self.hp}, Level: {self.level}"


#   This part of the code basically just sets most of the information on the character
#   Starting with the name

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

#   Then setting the gender
    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, gender):
        self._gender = gender

#   Setting the age

    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, age):
        self._age = age

#   setting the character's class
    @property
    def classe(self):
        return self._classe
    @classe.setter
    def classe(self, classe):
        self._classe = classe


#   This part sets the character's natural protection + armor protection
#   The character's natural protection depends on 3 factors: Age, Gender and the stat Resistance

    @property
    def protection(self):
        return self._protection
    @protection.setter
    def protection(self, resistance):

#   Being male grants 2 points, and female 1 point of protection
        armor = self.inventory["Armor"]

        match self.gender:
            case "Male":
                x = 10
            case "Female":
                x = 8

#   Also, if the character is between 13 and 30 years old, it is granted 3 points
#   if the character is below 13 or over 60 years old, it is granted only 1 point
#   Finally, if the character is between 30 and 60, it is granted 2 points

        if self.age >= 60 or self.age <= 13:
            y = 6
        elif self.age <= 30:
            y = 8
        else:
            y = 7

        if armor:
            a_pro = armor.protection()
        else:
            a_pro = 0
        protection = a_pro + resistance["resistance"] + x + y
        self._protection = protection


#   Here, the stats of the character are set
#   The stats method receives a dict as an argument
#   That is because it is supposed to receive the class stats, so it will be the initial stats

    @property
    def stats(self):
        return self._stats
    @stats.setter
    def stats(self, stats:dict):

        self._stats = stats


    #Setting the hp of the character, dependent of the classes hp
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, hp):

        if not hp >= self.max_hp:
            self._hp = hp
        else:
            self._hp = self.max_hp

#   The damage of the character is set here
#   The damage depends on two things: The character's strength and if it is using weapons or not
#   So the damage will be the value of the character's strength + the weapon's damage
#   The setter method takes a random argument, because the damage is only dependent on that two things


    def damage(self):
        weapon = self.inventory["Weapon"]
        strength = self.stats["strength"]
        if weapon:
            da = weapon.damage()
            damage = strength + da
        else:
            damage = strength

        return int(damage)


#   This method sets the level for the Character

    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level


#   This method is called to level up the character
#   Every time the character gets xp, this method is called

    def level_up(self, newlevel=None, want_print=True):
        xp = self.inventory["XP"]
        l = {
            "level_1" : 0,
            "level_2" : 100,
            "level_3" : 500,
            "level_4" : 750,
            "level_5" : 1000,
            "level_6" : 1500,
            "level_7" : 2000,
            "level_8" : 2500,
            "level_9" : 3000,
            "level_10" : 4000
        }

#   First of all, it checks if the character on which level the character is, based on the xp necessary set on the l dict

        if not newlevel:
            if xp > l["level_10"]:
                newlevel = 10
            elif xp > l["level_9"]:
                newlevel = 9
            elif xp > l["level_8"]:
                newlevel = 8
            elif xp > l["level_7"]:
                newlevel = 7
            elif xp > l["level_6"]:
                newlevel = 6
            elif xp > l["level_5"]:
                newlevel = 5
            elif xp > l["level_4"]:
                newlevel = 4
            elif xp > l["level_3"]:
                newlevel = 3
            elif xp > l["level_2"]:
                newlevel = 2
            elif xp >= l["level_1"]:
                newlevel = 1

#   Then, the method checks if the level is different than the character's actual level
#   And if it is, the character has leveled up
        levels_gained = newlevel - self.level
        if want_print and newlevel != self.level:
            print(f"\n\n{green}Congratulations!!! {self.name} has reached level {newlevel}!{reset}")
            sleep(3)


#   Leveling up grants the character a choice on which stat to improve for level gained



            for _ in range(levels_gained):
                print(green,"\n\nPlayer's current statline:", reset)
                self.print_stats()
                sleep(3)
                choice = Choice("Choose a stat to upper a level!","Strength", "Agility", "Intelligence", "Resistance", "Aim")
                match choice:
                    case "Strength":
                        self.stats["strength"] += 1
                    case "Agility":
                        self.stats["agility"] += 1
                    case "Intelligence":
                        self.stats["inteligence"] += 1
                    case "Resistance":
                        self.stats["resistance"] += 5
                    case "Aim":
                        self.stats["aim"] += 1
                print(green, "\n\nPlayer's new statline: ", reset)
                self.print_stats()
                sleep(2)

#   The character level is updated, and so is the max hp

        self.protection = self.stats
        self.level = newlevel
        if levels_gained > 0:
            self.max_hp = levels_gained
            if want_print:
                self.heal(levels_gained*5, want_print)
                print(f"{green}Your new max hp now is {self.max_hp}!{reset}")
            else:
                self.heal(levels_gained*5, want_print=False)
#   This method sets the character's max hp

    @property
    def max_hp(self):
        return self._max_hp
    @max_hp.setter
    def max_hp(self, n):


        if self.level == 1:

#   First of all, if the level is 1, it means that it is being set in the init method, so the max hp is set to the argument
#   We can be sure of that because there are only two places where the method is called: init and level_up

            self._max_hp = n


#   So if level is not 1, it is being called in level_up, and receives the number of levels gained as n
#   Now, the max hp will be increase by 5 for level gained

        else:
            self._max_hp += (5*n)


#   This method is called when the character take damage

    def take_damage(self, damage, want_print=True):

#  Applies the final calculated damage to the character's HP.


        self.hp = round(self.hp - damage, 2)

        if want_print:
            print(f"\n{red}{self.name} took {damage} damage{reset}")
            sleep(1)

            if self.hp <= 0:
                print(f"{red}{self.name}'s hp is now 0\n{self.name} Died{reset}")
                sleep(1)
            else:
                print(f"\n{self.name}'s hp is now {self.hp}")
                sleep(1)
#   This part grants that, if the damage is greater than the character's hp, the character died


#   Now, the hp is subtracted by the damage



#   This method heals the character, receiving the amount of hp to be restored
    def heal(self, heal:int, want_print=True):

        new_hp = self.hp + heal
        self.hp = new_hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        if want_print:
            print(f"\n{green}{self.name} healed {heal} hp and now has {self.hp} hp{reset}")

#   This method sets the character's inventory, initially empty
#   When the inventory is modified, it isn't by this method, but modifying the values in the self._inventory variable

    @property
    def inventory(self):
        return self._inventory
    @inventory.setter
    def inventory(self, a):
        if(type(a) == dict):
            inventory = a
        else:
            inventory = {
                'Armor' : None,
                'Weapon' : None,
                'Potions' : [],
                'Money' : 0,
                'XP' : 0
            }
        self._inventory = inventory

#   This method prints the character's inventory
    def print_inventory(self):

#   The method checks if there are weapons and potions in the inventory, and prints the result depending on that
        armor_name = self.inventory['Armor'].type if self.inventory['Armor'] else "None"
        weapon_name = self.inventory['Weapon'].type if self.inventory['Weapon'] else "None"
        list_potions = [p.type for p in self.inventory['Potions'] if isinstance(p, Potions)]
        potions_str = unlister(*list_potions) if list_potions else "None"

        print(f"{self.name}'s inventory: \n")
        print(f"{orange}Armor: {armor_name}")
        print(f"{red}Weapon: {weapon_name}")
        print(f"{blue}Potions: {potions_str}".strip(","))
        print(f"{green}Money: {self.inventory['Money']}")
        print(f"{green}XP: {self.inventory['XP']}")

        print(reset)
        sleep(2)

#   This method print the stats but 'undicting' the statline

    def print_stats(self):

        statline = self.stats
        protection = self.protection
        print(f"\n\n{cyan}Player's stats:\n")
        for i in statline:
            print(i.strip("'").strip().capitalize(), ":", statline[i])
        print(f"{cyan}Protection: {protection}{reset}")

#   This method implements an item in the character's inventory
    def take_item(self, item, want_print=True):

#   The method checks the type(class) of the item, to put it in the right place
        t = 0
        if type(item) == Armor:
            if want_print:
                print(f"{green}You took a {item}!!{reset}\n")
                sleep(1)
            if self.inventory["Armor"]:
                while True:
                    try:
                        want = Choice(f"\nAre you sure you want to trade {self.inventory['Armor']} for {item}", "Yes", "No")
                        if  want == "Yes":
                            self.inventory["Armor"] = item
                            self.protection = self.stats
                            if want_print:
                                print(green, "Your protection now is:", self.protection, reset)
                            break
                        elif want == "No":
                            return None
                        else:
                            raise TypeError

                    except TypeError:
                        print("\nPlese type the number corresponded to your answer, 1 or 2")
                        continue
            else:
                self.inventory["Armor"] = item
                self.protection = self.stats
                if want_print:
                    print(green, "Your protection now is:", self.protection, reset)

        elif type(item) == Weapon:
            if want_print:
                print(f"{green}You took a {item}!!{reset}")
                sleep(1)
            if self.inventory["Weapon"]:
                while True:
                    try:
                        want = Choice(f"\nAre you sure you want to trade {self.inventory['Weapon']} for {item}", "Yes", "No")
                        if  want == "Yes":
                            self.inventory["Weapon"] = item
                            break
                        elif want == "No":
                            return None
                        else:
                            raise TypeError

                    except TypeError:
                        print("\nPlese type the number corresponded to your answer, 1 or 2")
                        continue
            else:
                self.inventory["Weapon"] = item

        elif type(item) == Potions:
            if want_print:
                print(f"{green}You took a {item}!!{reset}")
                sleep(1)
            potions_number =   0
            for i in self.inventory["Potions"]:
                if type(i) == Potions:
                    potions_number += 1
            if potions_number >= 5:
                print(red,"\n\nYou've reached the potions limit in your inventory.", reset)
                sleep(1)
                self.print_inventory()
                choice = Choice("Do you want to take it and replace a potion in your inventory?", "Yes", "No")
                match choice:
                    case "Yes":
                        player_potions = []
                        for i in self.inventory["Potions"]:
                            if type(i) == Potions:
                                player_potions.append(i)
                        choice_2 = Choice("What potion do you want to replace?", *player_potions, "Go Back")
                        if choice_2 == "Go Back":
                            pass
                        else:
                            index = self.inventory["Potions"].index(choice_2)
                            self.inventory["Potions"][index]  = item
                    case "No":
                        pass

            else:
                for i in self.inventory["Potions"]:
                    if i == None:
                        index = self.inventory["Potions"].index(i)
                        self.inventory["Potions"][index] = item
                        t = 1
                        break
                if not t:
                    self.inventory["Potions"].append(item)
        else:
            n, coins = item.split(" ")
            if coins == "coins":
                n = int(n)
                if want_print:
                    print(f"{green}You took a {item}!!{reset}")
                    sleep(1)
                self.inventory["Money"] += n
            else:
                raise ValueError("\n\nThe item taken must be a Weapon, Potion or a number of coins")

#   This method increases the xp of the character, according to the n argument
#   Every time the get_xp method is called, the level_up method is also called, to check if the character leveled up
    def get_xp(self, n):
        self.inventory["XP"] += n
        self.level_up()

#   Lastly, this method performs an attack for the character, taking the oponnent as an argument
    def attack(self, oponnent, nk = False):

        damage = self.damage()
        pro = round(oponnent.protection/10)
        pro = int(pro)
        damage = int(damage)
        damage -=  pro
        if damage <= 0:
            damage = 0
        print(f"\n{self.name} tries to attack {oponnent.name}")
        sleep(1)

#   The method checks if the character has weapons, to then check if the attack hits

        if self.inventory["Weapon"]:
            if accuracy(self, self.inventory["Weapon"]):
                pass
            else:
                print(f"{self.name} failed")
                sleep(1)
                return None

#   This method then calls the take damage method, and prints the damage taken and the hp of the oponnent
        if nk:
            if damage >= oponnent.hp:
                damage = oponnent.hp - 1

        oponnent.take_damage(damage)



#   accuracy function execute the dice roll(being the dice dependent of the weapon type) for the chance of the attack hiting
#   accuracy is also dependent of the character's aim

def accuracy(character, weapon):
    d10 = Dice(10)
    d8 = Dice(8)
    d6 = Dice(6)
    d4 = Dice(4)

    weapon = weapon._type
    aim = character.stats["aim"]

    roll_10 = d10.roll()
    roll_8 = d8.roll()
    roll_6 = d6.roll()
    roll_4 = d4.roll()

#   returns True if Dice roll is greater than character's aim, and False else
#   that makes so the character's aim is an essential part of accuracy
#   The different dices for weapon is because of the range and difficulty of each weapon

    match weapon:
        case "Bow":
            return aim >= roll_10
        case "Fireball Scroll":
            return aim >= roll_8
        case "Sword":
            return aim >= roll_6
        case "Mace":
            return aim >= roll_6
        case "Knife":
            return aim >= roll_4
        case "Army Sword":
            return aim >= roll_8
#   Choice function receives multiple options and let player choose between them
def Choice(text: str, option_1, option_2, option_3 = None, option_4 = None, option_5 = None, option_6 = None):

#   The funcion firt checks how many options there are, and prompts the user
    while True:
        try:
            if option_6:
                choice = int(input(f"{text} \n[1] {option_1} \n[2] {option_2} \n[3] {option_3} \n[4] {option_4} \n[5] {option_5} \n[6] {option_6}\n\n"))
            elif option_5:
                choice = int(input(f"{text} \n[1] {option_1} \n[2] {option_2} \n[3] {option_3} \n[4] {option_4} \n[5] {option_5}\n\n"))
            elif option_4:
                choice = int(input(f"{text} \n[1] {option_1} \n[2] {option_2} \n[3] {option_3} \n[4] {option_4}\n\n"))
            elif option_3:
                choice = int(input(f"{text} \n[1] {option_1} \n[2] {option_2} \n[3] {option_3}\n\n"))
            else:
                choice = int(input(f"{text} \n[1] {option_1} \n[2] {option_2}\n\n"))

#   Now, the function returns the choice
            selected = None
            match choice:
                case 1: selected = option_1
                case 2: selected = option_2
                case 3: selected = option_3
                case 4: selected = option_4
                case 5: selected = option_5
                case 6: selected = option_6
                case _:
                    pass # Número fora de 1-6 cai aqui e selected continua None

            # O "Guard Clause": Se for None, é inválido. Não retorna, repete o loop.
            if selected is not None:
                return selected
            else:
                print("Number out of range.")
                sleep(1)
                continue

        except ValueError:
            print("Please enter a valid number.")
            sleep(1)
            continue
            
def unlister(*args):
    argument = str(args)
    argument = argument.replace("'", "")
    return argument.strip("()")


def print_slow(a, color=None):

    c = ""
    if color:
        match color:
            case "Red": c = red
            case "Green": c = green
            case "Orange": c = orange
            case "Magenta": c = magenta
            case "Cyan": c = cyan
            case "Blue": c = blue
            case _: raise ValueError("Color is not equivalent!")
    if DEBUG_MODE:
        if color:
            sys.stdout.write(f"{c}{a}{reset}")
        else:
            sys.stdout.write(a)
    elif not color:
        for _ in a:
            sys.stdout.write(_)
            sys.stdout.flush()
            sleep(0.04)
    else:
        for _ in a:
            sys.stdout.write(f"{c}{_}{reset}")
            sys.stdout.flush()
            sleep(0.04)
    print("\n")