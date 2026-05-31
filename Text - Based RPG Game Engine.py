import random 
import json
import logging
from abc import ABC, abstractmethod

logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

class PlayerState(ABC):
    @abstractmethod
    def state_name(self):
        pass

    @abstractmethod
    def health_effect(self):
        pass

class Healthy(PlayerState):
    def state_name(self):
        return "Healthy"
    
    def health_effect(self):
        return 1.0
    
class Poisoned(PlayerState):
    def state_name(self):
        return "Poisoned"
    
    def health_effect(self):
        return 0.7
    
class Dead(PlayerState):
    def state_name(self):
        return "Dead"
    
    def health_effect(self):
        return 0
    
class Item:
    def __init__(self, name, heal):
        self.name = name
        self.heal = heal

class Character:
    def __init__(self, name, health, attack_power, defense):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        
    def attack(self, target):
        damage = self.attack_power - target.defense
        if damage < 0:
            damage = 0

        target.health -= damage
        print(f"{self.name} attacked {target.name}")
        print(f"Damage: {damage}")
        logging.info(f"{self.name} attacked {target.name} ({damage})")

    def defend(self):
       self.defense += 5
       print(f"{self.name} increased defense")
       logging.info(f"{self.name} defended")


class Player(Character):
    def __init__(self,name,health,attack_power,defense):
         super().__init__(name, health, attack_power, defense)
         self.inventory = []
         self.state = Healthy()


    def use_item(self, item):
        self.health += item.heal
        print(f"{self.name} used {item.name}")
        logging.info(f"{self.name} used {item.name}")

  
    def change_state(self, new_state):
        self.state = new_state
        print(f"{self.name} state: " f"{self.state.state_name()}")
        logging.info(f"{self.name} changed state " f"to {self.state.state_name()}")


class Enemy(Character):
    def choose_action(self):
        if self.health < 20:
            return "retreat"
        return "attack"


class Quest:
    def __init__(self):
        quest_types = ["Kill Monster","Find Item","Explore Zone"]

        self.quest = random.choice(quest_types)
    def show_quest(self):
        print(f"Quest: {self.quest}")


class World:
    def __init__(self):
        self.players = []
        self.enemies = []
        self.quests = []

    def add_player(self, player):
        self.players.append(player)
    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def save_game(self):
        data = {"players": [{"name": p.name,"health": p.health,"attack": p.attack_power,
            "defense": p.defense,"state": p.state.state_name()} for p in self.players]}

        with open("savegame.json","w") as file:
            json.dump(data, file, indent=4)
        print("Game saved")


    def load_game(self):
        with open("savegame.json","r") as file:
            data = json.load(file)
        print(data)


world = World()
player = Player("Knight",100,25,10)


enemy = Enemy("Goblin",50,15,5)


potion = Item("Health Potion",30)


world.add_player(player)
world.add_enemy(enemy)



player.attack(enemy)
enemy.attack(player)


player.use_item(potion)
player.change_state(Poisoned())

print(enemy.choose_action())

world.save_game()
world.load_game()    