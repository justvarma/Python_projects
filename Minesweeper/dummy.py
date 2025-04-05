import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == '*':
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.dim_size, row + 2)):
            for c in range(max(0, col - 1), min(self.dim_size, col + 2)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    count += 1
        return count

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size, row + 2)):
            for c in range(max(0, col - 1), min(self.dim_size, col + 2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r, c) in self.dug:
                    visible_board[r][c] = str(self.board[r][c])

        widths = []
        for idx in range(self.dim_size):
            col_vals = [visible_board[row][idx] for row in range(self.dim_size)]
            widths.append(len(max(col_vals, key=len)))

        indices_row = '   ' + '  '.join(str(i).ljust(widths[i]) for i in range(self.dim_size)) + '\n'
        separator = '-' * (len(indices_row) - 1) + '\n'

        board_str = ''
        for i, row in enumerate(visible_board):
            row_str = f"{i} |" + '|'.join(str(cell).ljust(widths[j]) for j, cell in enumerate(row)) + '|\n'
            board_str += row_str

        return indices_row + separator + board_str + separator

def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        valid_input = False
        while not valid_input:
            user_input = input("Where would you like to dig? Input as row,col: ")
            try:
                row, col = map(int, user_input.split(','))
                if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
                    print("Invalid location. Try again.")
                    continue
                valid_input = True
            except Exception:
                print("❌ Invalid input format. Use row,col (e.g. 3,4)")
                continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("🎉 CONGRATULATIONS!!!! YOU ARE VICTORIOUS!\n")
    else:
        print("💥 SORRY GAME OVER :(\n")

    # Reveal full board
    board.dug = {(r, c) for r in range(board.dim_size) for c in range(board.dim_size)}
    print("Final board:")
    print(board)

if __name__ == '__main__':
    while True:
        play()
        again = input("Play again? (y/n): ")
        if again.lower() != 'y':
            print("👋 Thanks for playing Minesweeper!")
            break