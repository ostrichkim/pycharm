class Fancy:

    def __init__(self, secret):
        self.__secret = secret
        self.count = 0
        """
            but secret isn't very secret, is it?
            TODO: make secrete more... secretive!
        """
    @property
    def message(self):
        return self.__secret

        """
            TODO: now, define a property called message
            that outputs secret's value
        """

    @message.setter
    def set_secret(self, secret):
        print("I hope you know what you're doing")
        self.__secret = secret
        self.count += 1

        """
            TODO: Allow someone to change secret using the
            message property, but print "I hope you
            know what you're doing" before making the
            change
            (Don't forget to remove pass)
        """

    @classmethod
    def count_total_secret_changes(cls):
        return self.count

        """
            TODO: Change this to a class method, and have it
            return the total number of times that secret
            has been changed. (Hint, you may need to
            add a new class variable and change set_secret)
        """

    def __eq__(self, other):
        pass

    def __add__(self, other):
        self.__secret += other.secret
        return self

    @staticmethod
    def secret_saying(self, parameter):
        return "Secrets don't make friends, but",parameter,"might!"

    """
        TODO: Change this to a static method. Have it take in
        one parameter, and have it output the string
        "Secrets don't make friends, but <parameter>
        might!" where <parameter> is the given parameter.
    """

    """
        TODO: Add what's necessary for two Fancy objects to be
        considered equivalent when you compare them with ==
    """

    """
        TODO: Alter things such that adding two Fancy objects
        together creates a new Fancy object whose secret
        value is the first concatenated with the second
    """


one_fancy = Fancy("You thought this was a secret")
two_fancy = Fancy("The secret is that you were correct")
print("What was the secret?", two_fancy.message)
two_fancy.message = "Or were you?"
red_fancy = Fancy("You thought this was a secret")

one_and_red_fancy_equal = one_fancy == red_fancy
print('one_and_red_fancy_equal:', one_and_red_fancy_equal)

blue_fancy = one_fancy + two_fancy

"""
    TODO: Okay, slick. Now, create a new class called Outfit,
    composed of Fancy and a new class called Stylish.
    TODO: Stylish should have a message property. No need
    to underscore it.
"""

your_outfit = Outfit(Fancy("Thrift stores"), Stylish("But not trendy"))
