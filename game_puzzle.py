from random import randint

"""
이제 직사각형도 가능하게, array 수를 정할 수 있게 하자.
행과 열을 input으로 받는다.
0~(행 x 열)까지의 수를 iterate 하면서 str으로 변환해 넣고 마지막은 ''을 넣기
행만큼 for문 돌려서 그 안에서 열만큼 for문 돌려 값 넣기.
"""

goal = [['1','2','3'],['4','5','6'],['7','8','']]
arry = [['1','2','3'],['4','5','6'],['7','8','']]

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

        # row_or_col이 0이면 row 변경, 1이면 col 변경. 근데 똑같은자리에다가 해버리면?변경안되면?
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
        print("Congratulations! You made it!")
        print(data[0])
        print(data[1])
        print(data[2])
        return

    while True:
        empty_idx = return_index(data, '')
        print(data[0])
        print(data[1])
        print(data[2])
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

a = move(arry)
