class Pastry:

    def __init__(self, flavor):
        print("Created new", flavor, "pastry")
        self.flavor = flavor

    def print_flavor(self):
        print(self.flavor)


class Cake(Pastry):
    num_cakes = 0

    def __init__(self, size):
        super(Cake, self).__init__("sweet")
        print("This pastry is a cake")
        self.__size = size  # if you put __ in front of a variable name, users can't read or write the variable.
        self.count = 0
        Cake.num_cakes += 1  # class's variable

    @property  # By using property method, you can do anything here
    def size(self):
        self.count += 1
        print("someone retrieved the cake size!")
        return self.__size

    @size.setter
    def size(self, new_size):
        self.__size = new_size

    @classmethod  # It has access to class methods
    def print_cake_count(cls):
        print("There are currently", cls.num_cakes,\
              "cakes!")

    @staticmethod  # It isn't associated with the class at all. Completely independent
    def is_cake_delicious():
        return True

    def print_flavor(self):
        print(self.flavor)


class House:

    def __init__(self, wall=None, door=None):
        self.flavor = 1000
        self.Wall = wall
        self.Door = door

    def __str__(self):
        return "A House"

    def __add__(self, other):
        print("WHY WOULD YOU ADD A HOUSE?!")
        self.flavor += other.flavor
        return self


class Wall:
    pass


my_pastry = Pastry("sweet")
your_pastry = Pastry("savory")

my_pastry.print_flavor()

new_cake = Cake(3)
print(new_cake.size)
# new_cake.size = 10
print(new_cake.size)  # It looks like a property, but it is actually calling "def size(self)" method.
print("cake size access count:", new_cake.count)

another_cake = Cake(10)
another_cake.size
another_cake.size
another_cake.size
another_cake.size
another_cake.size

print("Another cake:", another_cake.count)

another_new_cake = Cake(8)
another_new_cake.size = 89
print(another_new_cake.size)

Cake(1)
Cake(1)
print("num_cakes:", Cake.num_cakes)

Cake.print_cake_count()

cake_delicious = Cake.is_cake_delicious()

flavor_things = [Cake(10), Pastry("Yum"), House()]  # Duck typing
for thing in flavor_things:
    print(thing.flavor)

my_house = House()
print(my_house)
other_house = House()

my_house = my_house + other_house
print(my_house.flavor)

new_house = House(wall=Wall(), door=Door())