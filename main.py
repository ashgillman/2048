import sys
import tty
import termios
import random
import copy

N = 4
PIPES = {
    'h': '═',
    'v': '║',
    'tl': '╔',
    't': '╦',
    'tr': '╗',
    'l': '╠',
    'm': '╬',
    'r': '╣',
    'bl': '╚',
    'b': '╩',
    'br': '╝',
}


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def make_new_board():
    return [[0 for _ in range(N)] for _ in range(N)]


def print_board(board):
    width = 4
    h = PIPES['h']*width
    top = PIPES['tl'] + h + h.join([PIPES['t']] * (N - 1)) + h + PIPES['tr']
    v = PIPES['l'] + h + h.join([PIPES['m']] * (N - 1)) + h + PIPES['r']
    bottom = PIPES['bl'] + h + h.join([PIPES['b']] * (N - 1)) + h + PIPES['br']
    rows = [
        (PIPES['v']
         + PIPES['v'].join('{{:^{}}}'.format(width).format(x)
                           if x
                           else ' ' * width
                           for x in row)
         + PIPES['v'])
        for row in board
    ]
    string = '\n'.join([top, '\n{}\n'.format(v).join(rows), bottom])
    print(string)


def get_empty(board):
    empty = []
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                empty.append((i, j))
    return empty


def collapse_board(board):
    new_board = []
    for row in board:
        new_row = []
        elem_last = 0
        for elem in row:
            if elem != 0:
                if elem == elem_last:
                    new_row[-1] = 2 * elem
                    elem_last = 0  # reset
                else:
                    new_row.append(elem)
                    elem_last = elem
        new_row.extend([0] * (N - len(new_row)))
        new_board.append(new_row)
    return new_board


def rotate_board(board, n):
    if n == 0:
        return board
    elif n < 0:
        return rotate_board(board, n % 4)
    else:
        return rotate_board(
            [[board[j][N - i - 1] for j in range(N)] for i in range(N)],
            n - 1)


def are_boards_equal(a, b):
    return all(x == y for rowa, rowb in zip(a, b) for x, y in zip(rowa, rowb))


if __name__ == '__main__':
    board = make_new_board()
    while True:
        # update new random
        try:
            new_pos = random.choice(get_empty(board))
        except IndexError:
            # no empty spots, game over
            break
        new_val = 2 if random.random() > 0.1 else 4
        board[new_pos[0]][new_pos[1]] = new_val

        # print to screen
        print()
        print_board(board)

        # get a valid move
        while True:
            try:
                rotation = 'awdsq'.index(getch())
            except ValueError:
                # invalid input
                print('Use WASD to make a move or Q to quit.')
                continue

            if rotation == 4:
                sys.exit()

            new_board = rotate_board(
                collapse_board(
                    rotate_board(
                        board, rotation)),
                -rotation)
            if not are_boards_equal(new_board, board):
                # valid move :)
                board = new_board
                break
            else:
                print('Invalid move')

    print('Game over')
