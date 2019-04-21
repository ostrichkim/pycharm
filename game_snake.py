import time, os, random, click
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
                if self.pixel > 3:
                    break
            except TypeError:
                print("Please type an integer.")

        self.screen = [list(' '*self.pixel) for a in range(self.pixel)]

        center_coordinate = self.pixel//2
        snake_head = Snake_piece([center_coordinate, center_coordinate])
        snake_body = Snake_piece([center_coordinate + 1, center_coordinate])
        snake_tail = Snake_piece([center_coordinate + 2, center_coordinate])
        self.head = snake_head
        self.tail = snake_tail
        self.head.next = snake_body
        self.head.next.next = self.tail
        self.body_size = 3
        self.direction = 'up'

        self.alive = True

        Snake_game.apple_regen(self)
        Snake_game.print_screen(self)
        t = threading.Thread(target=Snake_game.auto_move, args=(self,))
        t.start()
        Snake_game.user_move(self)
        t.join()

    def print_screen(self):
        # 기존화면 지우고, self.screen 좌표에 뱀과 사과를 넣고 line by line print
        clear()
        current_body = self.head
        self.screen = [list('#' + ' ' * self.pixel + '#') for a in range(self.pixel)]
        self.screen.insert(0,'#' * (self.pixel+2))
        self.screen.append('#' * (self.pixel+2))

        self.screen[current_body.coordinate[0]+1][current_body.coordinate[1]+1] = 'o'

        while current_body.next is not None:
            current_body = current_body.next
            self.screen[current_body.coordinate[0]+1][current_body.coordinate[1]+1] = '*'

        self.screen[self.apple[0]+1][self.apple[1]+1] = 'a'

        for line in self.screen:
            line = ''.join(line)
            print(line)

    # 머리만 앞으로가고 나머지는 따라와!
    # 갈 방향에 사과가 있으면 eat_apple 실행, 벽이나 자기 몸에 부딪히게 생겼으면 self.alive = False, 그게 아니면 그냥 ㄱㄱ
    def single_move(self, row, column):
        current_body = self.head
        snake_linked_coordinate = [current_body.coordinate]
        while current_body.next is not None:
            current_body = current_body.next
            snake_linked_coordinate.append(current_body.coordinate)

        if self.apple == [self.head.coordinate[0] + row, self.head.coordinate[1] + column]:
            Snake_game.eat_apple(self)

        elif self.head.coordinate[0] + row + 1 >= self.pixel or self.head.coordinate[1] + column >= self.pixel \
                or self.head.coordinate[0] + row + 1 < 0 or self.head.coordinate[1] + column < 0:
            print("Ouch! Your snake crashed into a wall.")
            print("Game Over")
            self.alive = False
            quit()

        elif [self.head.coordinate[0] + row, self.head.coordinate[1] + column] in snake_linked_coordinate:
            print("Ouch! Your snake stepped on its own body.")
            print("Game Over")
            self.alive = False
            quit()

        else:
            temp = self.head.coordinate
            self.head.coordinate = [self.head.coordinate[0] + row, self.head.coordinate[1] + column]
            current_body = self.head
            while current_body.next is not None:
                current_body = current_body.next
                current_body.coordinate, temp = temp, current_body.coordinate

        Snake_game.print_screen(self)

    # 1초에 한 번 자동으로 움직이고 계속 반복(single_move에서 벽에 부딪힐 때까지)
    def auto_move(self):
        if self.direction == 'up':
            Snake_game.single_move(self, -1, 0)
        elif self.direction == 'down':
            Snake_game.single_move(self, +1, 0)
        elif self.direction == 'left':
            Snake_game.single_move(self, 0, -1)
        else:
            Snake_game.single_move(self, 0, +1)

        time.sleep(1)
        if self.alive:
            Snake_game.auto_move(self)

    # 방향에 따라 상/하/좌/우 바꾸고 1번씩 이동함수 실행
    def user_move(self):
        k = click.getchar()
        if k == "w":
            self.direction = 'up'
            Snake_game.single_move(self, -1, 0)
        elif k == "s":
            self.direction = 'down'
            Snake_game.single_move(self, +1, 0)
        elif k == "a":
            self.direction = 'left'
            Snake_game.single_move(self, 0, -1)
        elif k == "d":
            self.direction = 'right'
            Snake_game.single_move(self, 0, +1)
        else:
            pass

        if self.alive:
            Snake_game.user_move(self)

    # 사과먹을 때. 이때 사과의 좌표 = 새로운 head 좌표
    def eat_apple(self):
        new_head = Snake_piece(self.apple)
        new_head.next = self.head
        self.head = new_head
        self.body_size += 1

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
