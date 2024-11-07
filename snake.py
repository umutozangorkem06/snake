import tkinter as tk
import random


WIDTH = 20
HEIGHT = 10
SNAKE_SPEED = 0.5
SPEED_FACTOR = 200


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=WIDTH * 20, height=HEIGHT * 20, bg='black')
        self.canvas.pack()
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -1)
        self.food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        self.score = 5
        self.draw_board()

        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game)
        self.quit_button = tk.Button(master, text="Quit", command=self.master.destroy)

        self.start_button.pack(side=tk.TOP)
        self.restart_button.pack(side=tk.TOP)
        self.quit_button.pack(side=tk.TOP)

        self.running = False

        self.master.bind('<KeyPress-Up>', lambda event: self.handle_input('Up'))
        self.master.bind('<KeyPress-Down>', lambda event: self.handle_input('Down'))
        self.master.bind('<KeyPress-Left>', lambda event: self.handle_input('Left'))
        self.master.bind('<KeyPress-Right>', lambda event: self.handle_input('Right'))

    def draw_board(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill='green')

        self.canvas.create_rectangle(self.food[0] * 20, self.food[1] * 20, (self.food[0] + 1) * 20, (self.food[1] + 1) * 20, fill='red')

        self.canvas.create_text(WIDTH * 10, HEIGHT * 20 + 10, text="Score: {}".format(self.score), fill='white', font=("Arial", 12))

        self.canvas.update()

    def start_game(self):
        if not self.running:
            self.canvas.create_text(WIDTH * 10, HEIGHT * 10, text="Snake Game", fill='white', font=("Arial", 20), tags="title")

            self.canvas.update()
            
            self.master.after(1000, self.remove_title_and_start_countdown)

    def remove_title_and_start_countdown(self):
        self.canvas.delete("title")  
        self.start_countdown(3)      

    def start_countdown(self, count):
        if count > 0:
            self.canvas.delete("countdown")  
            self.canvas.create_text(WIDTH * 10, HEIGHT * 10, text=str(count), fill='white', font=("Arial", 20), tags="countdown")
            self.canvas.update()
            self.master.after(1000, self.start_countdown, count - 1)
        else:
            self.canvas.delete("countdown")
            self.running = True
            self.move_snake()

    def restart_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -1)
        self.food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        self.score = 0
        self.running = False
        self.draw_board()

    def move_snake(self):
        if not self.running:
            return

        head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        if head == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])
            self.food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))

        self.snake = [head] + self.snake[:-1]

        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.snake[1:]:
            self.canvas.create_text(WIDTH * 10, HEIGHT * 10, text="Game Over! Your score: {}".format(self.score), fill='white', font=("Arial", 20))
            self.running = False  # Stop the game
            return

        self.draw_board()
        self.master.after(int(SNAKE_SPEED * (self.score + SPEED_FACTOR)), self.move_snake)

    def handle_input(self, direction):
        if direction == 'Up':
            if self.direction != (0, 1):
                self.direction = (0, -1)
        elif direction == 'Down':
            if self.direction != (0, -1):
                self.direction = (0, 1)
        elif direction == 'Left':
            if self.direction != (1, 0):
                self.direction = (-1, 0)
        elif direction == 'Right':
            if self.direction != (-1, 0):
                self.direction = (1, 0)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
