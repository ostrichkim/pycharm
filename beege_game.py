def main():
    adventurer = Adventurer()
    boar = Boar()
    battle(adventurer, boar)

    dragon = Dragon()
    battle(adventurer, dragon)

    demon = Demon()
    battle(adventurer, demon)

    print('You win!')


def battle(player, opponent):
    print("You're battling a", opponent)
    while player.health > 0 and opponent.health > 0:
        action = None
        while action not in ('attack', 'check_inventory', 'check_health'):
            action = input("""What would you like to do?
            attack
            check_inventory
            check_health\n""")
            if action == "a":
                player.attack(opponent)
            elif action == "i":
                player.print_inventory()
            elif action == "h":
                player.print_health()
            else:
                print("The command is invalid and you should try again.")
        opponent.attack(player)
    if opponent.health <= 0:
        player.loot(opponent)
        print('Congratulations! You slayed', opponent)
    if player.health <= 0:
        print("You died")
        from sys import exit
        exit(0)


class Creature:

    def __init__(self, health, armor, damage):
        self.health = health
        self.armor = armor
        self.damage = damage

    def take_damage(self, damage):
        calculated_damage = damage - self.armor
        print(self, 'lost', calculated_damage, 'health points in damage')
        self.health -= calculated_damage

    def attack(self, target):
        print("The creature is attacking the target.")
        target.take_damage(self.damage)


class Adventurer(Creature):
    def __init__(self):
        super(Adventurer, self).__init__(30, 5, 30)
        self.inventory = []

    def __str__(self):
        return "Noble Adventurer"

    def loot(self, dead_creature):
        # Add the dead creature's loot to the adventurer's inventory
        for item in dead_creature.loot:
            print("The player looted", item)
            self.inventory.append(item)
        self.update_stats()

    def update_stats(self):
        self.armor = 5
        self.damage = 10
        for item in self.inventory:
            if 'armor' in item.attributes:
                self.armor += item.attributes['armor']
            elif 'damage' in item.attributes:
                self.damage += item.attributes['damage']

    def print_inventory(self):
        print('The adventurer is currently carrying:')
        if len(self.inventory) == 0:
            print("\tNothing")
        else:
            for item in self.inventory:
                print("\t", item)

    def print_health(self):
        print('The adventurer currently has', self.health, 'health')


class Monster(Creature):
    def __init__(self, health, armor, damage, loot):
        super(Monster, self).__init__(health, armor, damage)
        self.loot = loot


class Dragon(Monster):
    def __init__(self):
        sword_of_dragon_slaying = Item('Sword of Dragon Slaying', {
            'damage': 10
        })
        helm_of_glory = Item('Helm of Glory', {
            'armor': 5
        })
        super(Dragon, self).__init__(40, 0, 20, [sword_of_dragon_slaying, helm_of_glory])

    def __str__(self):
        return 'Dragon'


class Boar(Monster):
    def __init__(self):
        shield_of_the_wild = Item('Shield of the Wild', {
            'armor': 10
        })
        super(Boar, self).__init__(30, 0, 6, [shield_of_the_wild])

    def __str__(self):
        return 'Boar'


class Demon(Monster):
    def __init__(self):
        hammer = Item('Heavenly Hammer of Hammertime', {'damage': 15})
        super(Demon, self).__init__(health=80, armor=5, damage=20, loot=[hammer])

"""
    TODO: Extra goal!
    Create a new monster called a Demon. It should inherit from Monster.
    A Demon should have 80 health, 5 armor, and do 20 damage.
    A Demon should carry one item as loot. This item should be called
    the Heavenly Hammer of Hammertime and should provide 15 damage.
    Make sure the player fights the Demon.
    Can you adjust the player's stats such that it's possible to win
    the game but not guaranteed?
    (I haven't actually done the math. Seriously, is it possible?)
"""


class Item:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return self.name


if __name__ == "__main__":
    main()