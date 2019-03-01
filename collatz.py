def collatz(number):
    if number % 2 == 0:
        print(number // 2)
        return number // 2
    print(3 * number + 1)
    return 3 * number + 1

isInteger = False
while not isInteger:
    number = input("Type in an integer\n")  # \n, \t...
    try:
        number = int(number)
    except ValueError as e:
        print("Didn't give me an integer!")
        continue
    isInteger = True

while number != 1:
    number = collatz(number)
