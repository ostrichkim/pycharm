import time, os, keyboard
#import threading

# Linked list로 size만큼 몸통연결
class Snake_piece:

    # 데이터는 좌표값
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.next = None

class Snake_game:

    def __init__(self):
        print("Snake game gets started!")

        while True:
            try:
                self.pixel = int(input("How many pixels?: "))
                break
            except TypeError:
                print("Please type an integer.")

        self.screen = [' '*self.pixel for a in range(self.pixel)]

        center_coordinate = self.pixel//2
        snake_head = Snake_piece([center_coordinate, center_coordinate])
        self.head = snake_head
        self.tail = snake_head
        self.body_size = 1
        self.direction = 'up'

    def print_screen(self):
        # self.screen 좌표에 뱀과 사과를 넣고 line by line print
        current_body = self.head
        for body in range(self.body_size):
            self.screen[current_body.coordinate[0]][current_body.coordinate[1]] = '*'
            current_body = current_body.next

        for line in self.screen:
            print(line)

    def auto_move(self):
        if self.direction = 'up':

        # 앞으로만 자동이동. 벽에 부딪히면 쥬금
        pass

    def user_move(self):
        # 방향에 따라 상/하/좌/우 함수를 실행시키고 거기서 계속 변경
        while True:
            try:
                if keyboard.is_pressed('up'):
                    print('up')
                elif keyboard.is_pressed('down'):
                    print('down')
                elif keyboard.is_pressed('left'):
                    print('left')
                elif keyboard.is_pressed('right'):
                    print('right')
                else:
                    pass
            except:
                pass

    def add_body(self):
        # 추가된 몸통 좌표값은 앞 몸통의 좌표값을 이어받는 걸로, 앞에는 그냥 한 칸 앞으로 나가는 걸로 만들기
        added_snake_body = Snake_piece(self.tail.coordinate)
        self.tail.next = added_snake_body
        self.tail = added_snake_body
        self.body_size += 1

    def eat_apple(self):
        # 사과먹을 때. 이때 사과의 좌표 = head 좌표로 하고, 몸통도 하나씩 앞으로 이동시킨 다음, add_body()를 실행시킨다
        # 그리고 사과 먹고나면 랜덤으로 사과생성. 다만 뱀 몸 위에는 생기지 않도록 한다.
        pass

user1 = Snake_game()




#t = threading.Thread(target= display, args=(10))
#t.start()


