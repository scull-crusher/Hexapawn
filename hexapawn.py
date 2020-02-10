# Imports
import random
import sys


# Classes
class Game:
    def __init__(self):
        self.rows = 3
        self.cols = 3
        self.board = create_board()
        self.moves = 0
        self.bad_moves = []
        open_file = open("bad_moves")
        file = open_file.read().split("\n")
        if file[-1] == "":
            file.remove(file[-1])
        for i in file:
            ls = i.split(",")
            sl = []
            try:
                for j in ls:
                    sl.append(int(j))
            except ValueError:
                print("Error.")
                sys.exit()
            self.bad_moves.append(sl)
        open_file.close()
        self.old_move = None
        self.old_c_move = None
        self.run = True
        self.start_game()

    def start_game(self):
        while self.run:
            turn = self.moves % 2
            if self.is_win():
                self.save_bad_moves()
                sys.exit()
            if turn == 0:
                self.print_board()
                inp1 = input("Enter the piece you want to move: ")
                inp2 = input("Enter the place you want it to move: ")
                if inp1.lower() == "q" or inp2.lower() == "q":
                    sys.exit()
                if inp1 == 'l' or inp2 == 'l':
                    print("X wins!")
                    sys.exit()
                coors1 = inp1.split(",")
                old_coors = []
                for i in coors1:
                    old_coors.append(int(i) - 1)
                coors2 = inp2.split(",")
                new_coors = []
                for i in coors2:
                    new_coors.append(int(i) - 1)
                self.move(old_coors, new_coors)
            else:
                self.get_computer_move()

    def print_board(self):
        print("  1 2 3")
        e = 0
        for c in self.board:
            i = 0
            e += 1
            print(e, end=" ")
            for r in c:
                if i >= 2:
                    print(r)
                else:
                    print(r, end=" ")
                i += 1

    def move(self, old_coors, new_coors):
        piece = self.board[old_coors[0]][old_coors[1]]
        space = self.board[new_coors[0]][new_coors[1]]
        if is_valid(piece, space, old_coors, new_coors):
            self.board[old_coors[0]][old_coors[1]] = "."
            self.board[new_coors[0]][new_coors[1]] = piece
            self.print_board()
            self.old_move = [old_coors[0], old_coors[1], new_coors[0], new_coors[1]]
            print("\n")
            self.moves += 1
        else:
            print("The move was not valid")

    def get_computer_move(self):
        moves = []
        r = -1
        for rows in self.board:
            r += 1
            c = -1
            for item in rows:
                c += 1
                if item == "X":
                    if self.board[r+1][c] == ".":
                        moves.append([r, c, r+1, c])
                    if c == 2:
                        if self.board[r + 1][c - 1] == "O":
                            moves.append([r, c, r + 1, c - 1])
                    if c == 0:
                        if self.board[r + 1][c + 1] == "O":
                            moves.append([r, c, r + 1, c + 1])
                    if c == 1:
                        if self.board[r+1][c+1] == "O":
                            moves.append([r, c, r+1, c+1])
                        if self.board[r+1][c-1] == "O":
                            moves.append([r, c, r+1, c-1])
        for move in moves:
            move.append(self.old_move[0])
            move.append(self.old_move[1])
            move.append(self.old_move[2])
            move.append(self.old_move[3])
        for j in self.bad_moves:
            if j in moves:
                moves.remove(j)
        if not moves:
            print("O wins!")
            self.bad_moves.append(self.old_c_move)
            self.save_bad_moves()
            sys.exit()
        print(moves)
        move = random.choice(moves)
        self.old_c_move = move
        piece = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = "."
        self.board[move[2]][move[3]] = piece
        self.moves += 1

    def is_win(self):
        i = -1
        for rows in self.board:
            i += 1
            for cols in rows:
                if i == 0:
                    if cols == "O":
                        print("O wins!")
                        self.bad_moves.append(self.old_c_move)
                        return True
                elif i == 2:
                    if cols == "X":
                        print("X wins!")
                        return True
                else:
                    return False

    def save_bad_moves(self):
        file = open("bad_moves", "w")
        for moves in self.bad_moves:
            i = 0
            for coors in moves:
                if i == 7:
                    file.write(str(coors) + '\n')
                else:
                    file.write(str(coors) + ',')
                i += 1
        file.close()


# Functions
def create_board():
    board = [["X", "X", "X"],
             [".", ".", "."],
             ["O", "O", "O"]]
    return board


def is_valid(piece, space, old_coors, new_coors):
    if piece == "X":
        return False
    else:
        if space == "X":
            if old_coors[0] - 1 == new_coors[0]:
                if old_coors[1] == new_coors[1]:
                    return False
                elif old_coors[1] == new_coors[1] - 1:
                    return True
                elif old_coors[1] == new_coors[1] + 1:
                    return True
                else:
                    return False
            else:
                return False
        elif space == ".":
            if old_coors[0] - 1 == new_coors[0]:
                if old_coors[1] == new_coors[1]:
                    return True
                elif old_coors[1] == new_coors[1] - 1:
                    return False
                elif old_coors[1] == new_coors[1] + 1:
                    return False
                else:
                    return False
            else:
                return False
        else:
            return False


# Main
if __name__ == "__main__":
    start_game = Game()
