from tkinter import Tk, Canvas
import random
from pynput import keyboard
import time

import threading

WIDTH = 500
HEIGHT = 500

def main_game_start(snake):
    # Make the final assignments..
    snake.snake_spawn()
    snake.food_spawn()

    listener = keyboard.Listener(on_press=snake.move)
    listener.start()

    while(snake.is_game_over()):
        snake.next_frame()
        if(snake.ate_food() == True):
            snake.food_spawn()

        time.sleep(0.2)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry(f"{HEIGHT}x{WIDTH}")

        self.board = Canvas(master, bg="white")
        self.board.pack()

        # Snake Game values
        self.food = [-1, -1, -1, -1]
        self.snake = []
        self.snake_rect = []
        self.size = 3
        self.directions = -1
        self.food_rect = -1

        # Start the Brain of the game
        brain = threading.Thread(target=main_game_start, args=(self,))
        brain.setDaemon(True)
        brain.start()

    def food_spawn(self):
        x = random.randint(20, HEIGHT)
        y = random.randint(20, WIDTH)

        self.food = [x-20, y-20, x, y]
        self.food_rect = self.board.create_rectangle(x-20, y-20, x, y, fill="red")

    def next_frame(self):
        x, y = self.snake[0]
        if(self.directions == -1):
            y = y + 20
        elif(self.directions == -2):
            x = x - 20
        elif(self.directions == 2):
            x = x + 20
        elif(self.directions == 1):
            y = y - 20

        self.snake.insert(0, [x, y])
        self.board.create_rectangle(x-20, y-20, x, y, fill="black")

        if(self.size < len(self.snake)):
            x, y = self.snake[-1]
            self.board.create_rectangle(x-20, y-20, x, y, fill="white", outline="white")
            del self.snake[-1]

    def snake_spawn(self):
        x = HEIGHT//3
        y = WIDTH//3

        for i in range(HEIGHT//150):
            self.snake.append([x, y])
            self.board.create_rectangle(x-20, y-20, x, y, fill="black")
            y = y - 20

    def is_game_over(self):
        if(self.snake[0][0] >= HEIGHT or self.snake[0][1] >= WIDTH or self.snake[0][0] <= 0 or self.snake[0][1] <= 0):
            self.master.quit()
            return False

        for i in range(0, len(self.snake)-1):
            for j in range(i+1, len(self.snake)):
                if(self.snake[i] == self.snake[j]):
                    self.master.quit()
                    return False
        return True

    def move(self, key):
        if(key == keyboard.Key.down):
            self.directions = -1
        elif(key == keyboard.Key.left):
            self.directions = -2
        elif(key == keyboard.Key.right):
            self.directions = 2
        elif(key == keyboard.Key.up):
            self.directions = 1

    def ate_food(self):
        x1, y1 = self.snake[0]

        if((x1 >= self.food[0] and x1 <= self.food[2]+20) and (y1 >= self.food[1]-10 and y1 <= self.food[3]+5)):
            self.board.delete(self.food_rect)
            self.size += 1
            return True
        return False

# Window Start..
win = Tk()
game = SnakeGame(win)
win.mainloop()