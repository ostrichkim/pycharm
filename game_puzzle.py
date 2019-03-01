from random import randint

goal = []

def array_setup(data):
    while True:
        try:
            row = int(input("Number of rows?: "))
            col = int(input("Number of columns?: "))
            break
        except ValueError:
            print("Please insert an integer for each question.")
    figure = [str(x) for x in range(1, row * col + 1)]

    for r in range(row):
        col_list = []
        for c in range(col):
            num = figure.pop(0)
            col_list.append(num)
        data.append(col_list)

    return data

array_setup(goal)
arry = []
for a in goal:
    col_list = []
    for b in a:
        col_list.append(b)
    arry.append(col_list)

goal[-1][-1] = ''
arry[-1][-1] = ''

def return_index(data, val):
    a = 0
    while a <= len(data):
        try:
            col = data[a].index(val)
            row = a
            break
        except ValueError:
            a += 1
    return row, col

def shuffle(data):
    count = 0
    while count < 50:
        empty_idx = return_index(data, '')
        row_or_col = randint(0, 1)

        if row_or_col == 0:
            target_idx = (randint(max(0, empty_idx[0]-1), min(len(data) - 1, empty_idx[0]+1)), empty_idx[1])
            data[target_idx[0]][target_idx[1]], data[empty_idx[0]][empty_idx[1]] = data[empty_idx[0]][empty_idx[1]], data[target_idx[0]][target_idx[1]]
            count += 1
        elif row_or_col == 1:
            target_idx = (empty_idx[0], randint(max(0, empty_idx[1]-1), min(len(data[0]) - 1, empty_idx[1]+1)))
            data[target_idx[0]][target_idx[1]], data[empty_idx[0]][empty_idx[1]] = data[empty_idx[0]][empty_idx[1]], data[target_idx[0]][target_idx[1]]
            count += 1

    return data

shuffle(arry)

def move(data):
    if data == goal:
        print("*"*20)
        for line in data:
            print(line)
        print("Congratulations! You made it!")
        return

    while True:
        empty_idx = return_index(data, '')
        for line in data:
            print(line)
        try:
            target_val = str(input("Which block do you want to move?: "))
            target_idx = return_index(data, target_val)
            if target_idx[0] == empty_idx[0] and (abs(target_idx[1] - empty_idx[1]) == 1):
                data[target_idx[0]][target_idx[1]], data[empty_idx[0]][empty_idx[1]] = data[empty_idx[0]][empty_idx[1]], \
                                                                                       data[target_idx[0]][
                                                                                           target_idx[1]]
                break
            elif target_idx[1] == empty_idx[1] and (abs(target_idx[0] - empty_idx[0]) == 1):
                data[target_idx[0]][target_idx[1]], data[empty_idx[0]][empty_idx[1]] = data[empty_idx[0]][empty_idx[1]], \
                                                                                       data[target_idx[0]][
                                                                                           target_idx[1]]
                break
            print("Please choose a block next to the empty block.")
        except IndexError:
            print("Please enter a valid value.")

    return move(data)

test = move(arry)