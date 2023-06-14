import cv2
import random
import time
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()

ports_list = []

for port in ports:
    ports_list.append(str(port))
    print(str(port))

val: str = input('Select Port: COM')

for i in range(len(ports_list)):
    if ports_list[i].startswith(f'COM{val}'):
        port_var = f'COM{val}'
        print(port_var)

serial_inst.baudrate = 9600
serial_inst.port = port_var
serial_inst.open()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print(' _______________________________________________________________ ')
print("|  _____  _  ____     _____  ____  ____     _____  ____  _____  |")
print("| /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/  |")
print("|   / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \    |")
print("|   | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_   |")
print("|   \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\  |")
print('|_______________________________________________________________|\n')
print(20 * ' ', "   reference:    ")
print(20 * ' ', '     |    |      ')
print(20 * ' ', '  1  | 2  | 3    ')
print(20 * ' ', "-----+----+----- ")
print(20 * ' ', "     |    |      ")
print(20 * ' ', "  4  | 5  | 6    ")
print(20 * ' ', "-----+----+----- ")
print(20 * ' ', "     |    |      ")
print(20 * ' ', "  7  | 8  | 9    \n")


def display_board():
    print()
    print('                               reference:')
    print('     |    |     ', 10 * ' ', '     |    |   ', )
    print('  ' + board[1] + '  | ' + board[2] + '  | ' + board[3] + '   ', 10 * ' ', '  1  | 2  | 3  ')
    print('-----+----+-----', 10 * ' ', "-----+----+-----")
    print('     |    |     ', 10 * ' ', "     |    |     ")
    print('  ' + board[4] + '  | ' + board[5] + '  | ' + board[6] + '   ', 10 * ' ', "  4  | 5  | 6   ")
    print('-----+----+-----', 10 * ' ', "-----+----+-----")
    print('     |    |     ', 10 * ' ', "     |    |      ")
    print('  ' + board[7] + '  | ' + board[8] + '  | ' + board[9] + '   ', 10 * ' ', "  7  | 8  | 9    \n\n")


num_list = []
blue_actual = 0
red_actual = 0


def add_grid_to_frame(frame):
    height, width, _ = frame.shape

    cell_width = width // 3
    cell_height = height // 3

    cv2.line(frame, (cell_width, 0), (cell_width, height), (0, 255, 0), 2)
    cv2.line(frame, (2 * cell_width, 0), (2 * cell_width, height), (0, 255, 0), 2)

    cv2.line(frame, (0, cell_height), (width, cell_height), (0, 255, 0), 2)
    cv2.line(frame, (0, 2 * cell_height), (width, 2 * cell_height), (0, 255, 0), 2)

    return frame


def take_screenshot():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open camera")
        return

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        return

    frame_with_grid = add_grid_to_frame(frame)

    cv2.imwrite("screenshot.png", frame_with_grid)
    print("Screenshot saved as screenshot.png")


def main_game(win, pair, p1, p2, p3):
    flag = 1

    if win == 1:
        time.sleep(10)

    while flag:
        b_count = 0
        r_count = 0
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, w, _ = frame.shape

        cx = int(w / 2)
        cy = int(h / 2)

        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]

        color = "Undefined"

        if hue_value < 131 and hue_value > 78:
            color = "BLUE"
        elif hue_value > 170:
            color = "RED"

        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        cell_width = w // 3
        cell_height = h // 3

        for i in range(1, 3):
            cv2.line(frame, (i * cell_width, 0), (i * cell_width, h), (0, 255, 0), 2)
            cv2.line(frame, (0, i * cell_height), (w, i * cell_height), (0, 255, 0), 2)

        blue = 0
        red = 0

        global num_list
        global blue_actual
        global red_actual
        length = 0

        blue_actual = 0
        red_actual = 0

        for i in range(3):
            for j in range(3):
                cell_center_x = int((2 * j + 1) * cell_width / 2)
                cell_center_y = int((2 * i + 1) * cell_height / 2)
                cv2.circle(frame, (cell_center_x, cell_center_y), 25, (0, 255, 0), -1)

                cell_center_pixel = hsv_frame[cell_center_y, cell_center_x]
                cell_hue_value = cell_center_pixel[0]
                cell_color = "Undefined"

                if cell_hue_value > 110 and cell_hue_value < 150:
                    cell_color = "BLUE"
                elif cell_hue_value < 30 or cell_hue_value > 170:
                # elif cell_hue_value > 170:
                    cell_color = "RED"

                center_number = i * 3 + j + 1

                if cell_color == "BLUE":
                    center = (cell_center_x, cell_center_y)
                    radius = 50

                    cv2.circle(frame, center, radius, (255, 0, 0), 3)

                if cell_color == "RED":
                    height, width, _ = frame.shape

                    desired_cell_row = i
                    desired_cell_col = j

                    cell_width = width // 3
                    cell_height = height // 3
                    cell_x = (desired_cell_col * cell_width) + (cell_width // 2)
                    cell_y = (desired_cell_row * cell_height) + (cell_height // 2)

                    start_point1 = (cell_x - 50, cell_y - 50)
                    end_point1 = (cell_x + 50, cell_y + 50)
                    start_point2 = (cell_x + 50, cell_y - 50)
                    end_point2 = (cell_x - 50, cell_y + 50)

                    cv2.line(frame, start_point1, end_point1, (0, 0, 255), 3)
                    cv2.line(frame, start_point2, end_point2, (0, 0, 255), 3)

                if cell_color == "BLUE":
                    blue += 1
                    if center_number in num_list:
                        pass
                    else:
                        num_list.insert(0, center_number)

                elif cell_color == "RED":
                    red += 1
                    if center_number in num_list:
                        pass
                    else:
                        num_list.insert(0, center_number)

                print(f"Center {center_number}: {cell_color}")

        # cv2.putText(frame, color, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 2)
        # cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

        if pair:
            center_mapping = {
                '1': (int(cell_width / 2), int(cell_height / 2)),
                '2': (int(cell_width * 3 / 2), int(cell_height / 2)),
                '3': (int(cell_width * 5 / 2), int(cell_height / 2)),
                '4': (int(cell_width / 2), int(cell_height * 3 / 2)),
                '5': (int(cell_width * 3 / 2), int(cell_height * 3 / 2)),
                '6': (int(cell_width * 5 / 2), int(cell_height * 3 / 2)),
                '7': (int(cell_width / 2), int(cell_height * 5 / 2)),
                '8': (int(cell_width * 3 / 2), int(cell_height * 5 / 2)),
                '9': (int(cell_width * 5 / 2), int(cell_height * 5 / 2))
            }

            p1 = str(p1)
            p2 = str(p2)
            p3 = str(p3)

            center1 = center_mapping.get(p1)
            center2 = center_mapping.get(p2)
            center3 = center_mapping.get(p3)
            cv2.line(frame, center1, center3, (0, 255, 0), 3)
            print(f"Line drawn between center {p1} and center {p3}")

        if blue_actual < blue:
            blue_actual = blue
            # time.sleep(5)
            flag = 0
            b_count = 1
        else:
            pass

        if red_actual < red:
            red_actual = red
            # time.sleep(5)
            flag = 0
            r_count = 1
        else:
            pass

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == 27:
            break

    if win == 1:
        if b_count == 1:
            print(num_list)
            return num_list[0]
        else:
            return 0
    else:
        if r_count == 1:
            print(num_list)
            return num_list[0]
        else:
            return 0


def human_input(mark, win):
    while True:
        inp = main_game(win, 0, 0, 0, 0)
        if int(inp) < 10 and int(inp) > 0:
            inp = int(inp)
            if board[inp] == " ":
                return inp
            else:
                print(f"[USER]/{mark} ERROR: place already taken.")
                time.sleep(5)
        else:
            print(f"[USER]/{mark} ERROR: INVALID COIN / TAKE YOUR MOVE.")
            time.sleep(5)


def winning(mark, board):
    winning_place = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for win_place in winning_place:
        if board[win_place[0]] == board[win_place[1]] == board[win_place[2]] == mark:
            return True


def win_move(i, board, mark):
    temp_board = list(board)
    temp_board[i] = mark
    if winning(mark, temp_board):
        return True
    else:
        return False


def cpu_input(cpu, human, board):
    for i in range(1, 10):
        if board[i] == ' ' and win_move(i, board, cpu):
            return i
    for i in range(1, 10):
        if board[i] == ' ' and win_move(i, board, human):
            return i
    for i in [5, 1, 7, 3, 2, 9, 8, 6, 4]:
        if board[i] == ' ':
            return i


def new_game():
    while True:
        nxt = input('[USER] Do you want to play again?(y/n):')
        if nxt in ['y', 'Y']:
            global num_list
            num_list = []
            again = True
            break
        elif nxt in ['n', 'N']:
            print('GAME OVER!')
            again = False
            break
        else:
            print('Enter correct input')
    if again:
        print('__________NEW GAME__________')
        main_game1()
    else:
        return False


def win_check(human, cpu):
    winning_place = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for win_place in winning_place:
        if board[win_place[0]] == board[win_place[1]] == board[win_place[2]] == human:
            print('[USER] wins the match!')
            if not new_game():
                return False
        elif board[win_place[0]] == board[win_place[1]] == board[win_place[2]] == cpu:
            main_game(0, 1, win_place[0], win_place[1], win_place[2])
            print('[CPU] wins the match!')
            if not new_game():
                return False
    if ' ' not in board:
        print('MATCH DRAW!!')
        if not new_game():
            return False
    return True


def user_choice():
    while True:
        coin_toss = 0
        play = int(input("TOSS- 0 / 1: "))
        win = 0
        if play == coin_toss:
            print("You won the Toss, make your 1st move - BLUE!")
            win = 1
            return 'o', 'x', win
        elif play != 1 and play != 0:
            print('[USER] Enter correct input!')
        else:
            print("Computer won the Toss and I will make the 1st move - BLUE!")
            return 'x', 'o', win


def main_game1():
    global board
    play = True
    board = ['', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    human, cpu, win = user_choice()
    display_board()
    while play:
        if human == 'o':
            o = human_input(human, win)
            print("YOUR POINT", o)
            board[o] = human
            display_board()
            play = win_check(human, cpu)
            time.sleep(5)

            if play:
                x = cpu_input(cpu, human, board)
                command: str = str(x)
                serial_inst.write(command.encode('utf-8'))
                time.sleep(50)
                num_list.insert(0, x)
                print(num_list)
                print(f'[CPU] Entered:{x}')
                board[x] = cpu
                display_board()
                play = win_check(human, cpu)
        else:
            o = cpu_input(cpu, human, board)
            command: str = str(o)
            serial_inst.write(command.encode('utf-8'))
            time.sleep(50)
            num_list.insert(0, o)
            print(num_list)
            print(f'[CPU] Entered:{o}')
            board[o] = cpu
            display_board()
            play = win_check(human, cpu)
            time.sleep(10)

            if play:
                x = human_input(human, win)
                print("YOUR POINT", x)
                board[x] = human
                display_board()
                play = win_check(human, cpu)
                time.sleep(5)


if __name__ == '__main__':
    take_screenshot()
    main_game1()

cap.release()
cv2.destroyAllWindows()
