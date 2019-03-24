import time, os, keyboard, random
import threading

clear = lambda: os.system('cls')

# 데이터는 좌표값
class Snake_piece:

    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.next = None

# Linked list로 size만큼 몸통연결
class Snake_game:

    def __init__(self):
        print("Snake game gets started!")

        while True:
            try:
                self.pixel = int(input("How many pixels?: "))
                break
            except TypeError:
                print("Please type an integer.")

        self.screen = [list(' '*self.pixel) for a in range(self.pixel)]

        center_coordinate = self.pixel//2
        snake_head = Snake_piece([center_coordinate, center_coordinate])
        self.head = snake_head
        self.tail = snake_head
        self.body_size = 1
        self.direction = 'up'

        Snake_game.apple_regen(self)
        Snake_game.auto_move(self)

    def print_screen(self):
        # 기존화면 지우고, self.screen 좌표에 뱀과 사과를 넣고 line by line print
        clear()
        current_body = self.head
        self.screen[current_body.coordinate[0]][current_body.coordinate[1]] = '*'

        while current_body.next is not None:
            current_body = current_body.next
            self.screen[current_body.coordinate[0]][current_body.coordinate[1]] = '*'

        self.screen[self.apple[0]][self.apple[1]] = 'a'

        for line in self.screen:
            line = ''.join(line)
            print(line)

    # 1초에 한 번 자동으로 움직이고 계속 반복(single_move에서 벽에 부딪힐 때까지)
    def auto_move(self):
        print("auto_move 실행")
        if self.direction == 'up':
            Snake_game.single_move(self, -1, 0)
        elif self.direction == 'down':
            Snake_game.single_move(self, +1, 0)
        elif self.direction == 'left':
            Snake_game.single_move(self, 0, -1)
        else:
            Snake_game.single_move(self, 0, +1)

        if self.head.coordinate == self.apple:
            Snake_game.eat_apple(self)

        Snake_game.print_screen(self)
        time.sleep(1)
        Snake_game.auto_move(self)

    # 머리만 앞으로가고 나머지는 따라와!
    def single_move(self, row, column):
        current_body = self.head
        temp = current_body.coordinate
        current_body.coordinate = [current_body.coordinate[0] + row, current_body.coordinate[1] + column]

        while current_body.next is not None:
            current_body = current_body.next
            current_body.coordinate, temp = temp, current_body.coordinate
        quit()

    # 방향에 따라 상/하/좌/우 바꾸고 1번씩 이동함수 실행
    def user_move(self):
        while True:
            try:
                if keyboard.is_pressed('up'):
                    self.direction = 'up'
                    Snake_game.single_move(self, -1, 0)
                elif keyboard.is_pressed('down'):
                    self.direction = 'down'
                    Snake_game.single_move(self, +1, 0)
                elif keyboard.is_pressed('left'):
                    self.direction = 'left'
                    Snake_game.single_move(self, 0, -1)
                elif keyboard.is_pressed('right'):
                    self.direction = 'right'
                    Snake_game.single_move(self, 0, +1)
                else:
                    pass
            except:
                pass

        if self.head.coordinate == self.apple:
            Snake_game.eat_apple(self)

        Snake_game.user_move(self)

    # 사과먹을 때. 이때 사과의 좌표 = 새로운 head 좌표
    def eat_apple(self):
        new_head = Snake_piece(self.apple)
        self.head.next = self.head
        self.head = new_head
        self.body_size += 1
        time.sleep(1)

        Snake_game.apple_regen(self)

    # 사과 먹고나면 뱀 몸 위에 생기지 않도록 랜덤으로 사과생성
    def apple_regen(self):
        current_body = self.head
        snake_linked_coordinate = [current_body.coordinate]

        while current_body.next is not None:
            current_body = current_body.next
            snake_linked_coordinate.append(current_body.coordinate)

        self.apple = self.head.coordinate
        while self.apple in snake_linked_coordinate:
            self.apple = [random.randrange(0, self.pixel), random.randrange(0, self.pixel)]


user1 = Snake_game()
