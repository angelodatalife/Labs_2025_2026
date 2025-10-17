import random

class Soldier:
    def __init__(self, health, strength):
        self.health = health
        self.strength = strength

    def attack(self):
        return self.strength

    def receiveDamage(self, damage):
        self.health -= damage

class Viking(Soldier):
    def __init__(self, name, health, strength):
        super().__init__(health, strength)
        self.name = name

    def receiveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"{self.name} has received {damage} points of damage"
        else:
            return f"{self.name} has died in act of combat"

    def battleCry(self):
        return "Odin Owns You All!"

class Saxon(Soldier):
    def __init__(self, health, strength):
        super().__init__(health, strength)

    def receiveDamage(self, damage):
        self.health -= damage
        if self.health > 0:
            return f"A Saxon has received {damage} points of damage"
        else:
            return "A Saxon has died in combat"

class War:
    def __init__(self):
        self.vikingArmy = []
        self.saxonArmy = []

    def addViking(self, viking):
        self.vikingArmy.append(viking)

    def addSaxon(self, saxon):
        self.saxonArmy.append(saxon)

    def vikingAttack(self):
        saxon = random.choice(self.saxonArmy)
        viking = random.choice(self.vikingArmy)
        result = saxon.receiveDamage(viking.strength)
        if saxon.health <= 0:
            self.saxonArmy.remove(saxon)
        return result

    def saxonAttack(self):
        viking = random.choice(self.vikingArmy)
        saxon = random.choice(self.saxonArmy)
        result = viking.receiveDamage(saxon.strength)
        if viking.health <= 0:
            self.vikingArmy.remove(viking)
        return result

    def showStatus(self):
        if not self.saxonArmy:
            return "Vikings have won the war of the century!"
        elif not self.vikingArmy:
            return "Saxons have fought for their lives and survive another day..."
        else:
            return "Vikings and Saxons are still in the thick of battle."



# BONUS

# Import necessary classes and modules
import random
from vikingsClasses import Viking, Saxon, War

# === NAME POOLS ===
# These lists are used to give random names to Vikings and Saxons
viking_names = ["Thor", "Loki", "Odin", "Freya", "Ragnar", "Bjorn", "Ivar", "Harald", "Astrid", "Siv"]
saxon_names = ["Aelfric", "Beowulf", "Cedric", "Eadric", "Godric", "Hengist", "Oswin", "Penda", "Wulfric", "Edgar"]

# === FUNCTION: CREATE VIKING TEAM ===
# Creates a list of Viking objects with random stats
def create_vikings(amount):
    army = []
    for _ in range(amount):
        name = random.choice(viking_names)     # Pick a random Viking name
        health = random.randint(80, 120)       # Random health between 80 and 120
        strength = random.randint(20, 40)      # Random strength between 20 and 40
        viking = Viking(name, health, strength) # Create the Viking
        army.append(viking)                    # Add to the army list
    return army

# === FUNCTION: CREATE SAXON TEAM ===
# Creates a list of Saxon objects with random stats
def create_saxons(amount):
    army = []
    for _ in range(amount):
        health = random.randint(60, 100)       # Random health between 60 and 100
        strength = random.randint(15, 35)      # Random strength between 15 and 35
        saxon = Saxon(health, strength)        # Create the Saxon
        army.append(saxon)                     # Add to the army list
    return army

# === FUNCTION: MAIN GAME ===
# Runs the full battle simulation
def play_game():
    print("⚔️  The Viking War Begins! ⚔️\n")

    # Create a new war (empty armies at start)
    war = War()

    # Generate 5 Vikings and 5 Saxons
    vikings = create_vikings(5)
    saxons = create_saxons(5)

    # Add Vikings to the war
    for v in vikings:
        war.addViking(v)

    # Add Saxons to the war
    for s in saxons:
        war.addSaxon(s)

    round = 1  # Round counter

    # === MAIN BATTLE LOOP ===
    # Keep fighting until one army is dead
    while war.showStatus() == "Vikings and Saxons are still in the thick of battle.":

        print(f"--- Round {round} ---")

        # === VIKING ATTACK TURN ===
        if war.vikingArmy and war.saxonArmy:
            viking_result = war.vikingAttack()  # A Viking attacks a random Saxon
            print("🔥 Viking attacks:", viking_result)

        # === SAXON ATTACK TURN ===
        if war.vikingArmy and war.saxonArmy:
            saxon_result = war.saxonAttack()    # A Saxon attacks a random Viking
            print("🛡️  Saxon attacks:", saxon_result)

        # === SHOW ARMY STATUS ===
        print("Status:")
        print(f"  🧔 Vikings alive: {len(war.vikingArmy)}")
        print(f"  🏰 Saxons alive: {len(war.saxonArmy)}")
        print()

        round += 1  # Increase round number

    # === END OF GAME ===
    print("🏁 GAME OVER")
    print(war.showStatus())  # Show who won

# === RUN THE GAME ===
# This line makes sure the game only runs when this file is executed directly
if __name__ == "__main__":
    play_game()





