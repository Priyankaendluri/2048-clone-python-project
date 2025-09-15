import random
import os

SIZE = 4  # 4x4 board

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def init_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if board[i][j] == 0]
    if empty:
        i, j = random.choice(empty)
        board[i][j] = 4 if random.random() < 0.1 else 2

def print_board(board, score):
    clear_screen()
    print("2048 Game".center(20))
    print(f"Score: {score}")
    for row in board:
        print("+------+------+------+------+")

        for cell in row:
            print("|{: ^6}".format(cell if cell != 0 else " "), end="")
        print("|")
    print("+------+------+------+------+")

def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row

def merge(row):
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(board):
    new_board = []
    score_gain = 0
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        compressed = compress(merged)
        new_board.append(compressed)
        score_gain += sum([cell for cell in compressed if cell != 0])
    return new_board, score_gain

def reverse(board):
    return [row[::-1] for row in board]

def transpose(board):
    return [list(row) for row in zip(*board)]

def move(board, direction):
    if direction == 'left':
        return move_left(board)
    elif direction == 'right':
        reversed_board = reverse(board)
        new_board, score = move_left(reversed_board)
        return reverse(new_board), score
    elif direction == 'up':
        transposed = transpose(board)
        new_board, score = move_left(transposed)
        return transpose(new_board), score
    elif direction == 'down':
        transposed = transpose(board)
        reversed_board = reverse(transposed)
        new_board, score = move_left(reversed_board)
        return transpose(reverse(new_board)), score
    return board, 0

def has_moves(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == 0:
                return True
            if i < SIZE - 1 and board[i][j] == board[i+1][j]:
                return True
            if j < SIZE - 1 and board[i][j] == board[i][j+1]:
                return True
    return False

def play():
    board = init_board()
    score = 0

    while True:
        print_board(board, score)
        move_input = input("Move (WASD or Q to quit): ").lower()

        if move_input == 'q':
            print("Game Over. Final Score:", score)
            break

        move_map = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}
        if move_input not in move_map:
            continue

        direction = move_map[move_input]
        new_board, gained = move(board, direction)

        if new_board != board:
            add_new_tile(new_board)
            score += gained
            board = new_board

        if any(2048 in row for row in board):
            print_board(board, score)
            print("🎉 You win!")
            break

        if not has_moves(board):
            print_board(board, score)
            print("❌ No moves left. Game Over.")
            break

if __name__ == "__main__":
    play()

