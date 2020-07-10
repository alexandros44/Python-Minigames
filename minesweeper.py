from tkinter import *
import random
import time

MINES = 10
TABLE = 6

class GameSense:
    def __init__(self):
        # Board initialization..
        self.board = []
        self.board_setup()

    def board_setup(self):
        # Make a 2dim table made of 0's
        self.board = [[1 for _ in range(TABLE)] for _ in range(TABLE)]

        # Add the MINES..
        for _ in range(MINES):
            x = random.randint(0, TABLE-1)
            y = random.randint(0, TABLE-1)
            while(self.board[x][y] == -1):
                x = random.randint(0, TABLE-1)
                y = random.randint(0, TABLE-1)

            self.board[x][y] = -1

    def find_nearest_mines(self, x, y):
        mines = 0
        mines = [self.board[x_][y_] for x_ in range(x-1,x+2) for y_ in range(y-1,y+2)
                       if (0 <= x_ < len(self.board) and 0 <= y_ < len(self.board) and (x_ != x or y_ != y))]

        return mines.count(-1)

    def game_over_check(self, x, y):
        if(self.board[x][y] == -1):
            return -1
        self.board[x][y] = 0
        return self.find_nearest_mines(x, y)

    def player_won(self):
        won = [self.board[i].count(1) for i in range(TABLE)]
        if(won.count(0) == TABLE):
            return True
        return False


class MainWindow:
    def __init__(self, master, game):
        self.game = game
        self.master = master
        self.master.title("MineSweeper")

        self.button_layout = [[] for _ in range(TABLE)]
        self.adding_mines()

    def adding_mines(self):
        for i in range(TABLE):
            for j in range(TABLE):
                btn = Button(self.master, height=2, width=4, text ="    ", command=lambda x=i, y=j:self.onclick(x, y))
                self.button_layout[i].append(btn)

                btn.grid(row=i, column=j)

    def onclick(self, x, y):
        mines = self.game.game_over_check(x, y)

        # Exiting if lost..
        if(mines == -1):
            self.button_layout[x][y]['text'] = " X "
            self.master.quit()

        self.button_layout[x][y]['text'] = f" {mines} "

        # Show all the table after Winning
        if(self.game.player_won() == True):
            for i in range(TABLE):
                for j in range(TABLE):
                    if(self.game.board[i][j] == -1):
                        self.button_layout[i][j]['text'] = " X "


# Init the functions..
win = Tk()
game = GameSense()

# Start the View's mainloop
main_window = MainWindow(win, game)
win.mainloop()