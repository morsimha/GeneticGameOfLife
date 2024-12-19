import tkinter as tk
import random

class GameOfLife:
    def __init__(self, root, grid_size=50, cell_size=10):
        self.root = root
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.running = False
        self.generation = 0

        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        self.canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size, bg="white")
        self.canvas.pack()

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.start_button = tk.Button(self.controls_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.controls_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT)

        self.random_button = tk.Button(self.controls_frame, text="Randomize", command=self.randomize)
        self.random_button.pack(side=tk.LEFT)

        self.generation_label = tk.Label(root, text=f"Generation: {self.generation}")
        self.generation_label.pack()

        self.canvas.bind("<Button-1>", self.toggle_cell)

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.grid[y][x] = 1 - self.grid[y][x]
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == 1:
                    self.canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill="black"
                    )

    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.grid[y][x] == 1:
                    if live_neighbors in [2, 3]:
                        new_grid[y][x] = 1
                else:
                    if live_neighbors == 3:
                        new_grid[y][x] = 1
        self.grid = new_grid
        self.generation += 1
        self.generation_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()

    def count_live_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                count += self.grid[ny][nx]
        return count

    def step(self):
        if self.running:
            self.update_grid()
            self.root.after(100, self.step)

    def start(self):
        if not self.running:
            self.running = True
            self.step()

    def stop(self):
        self.running = False

    def clear(self):
        self.running = False
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation = 0
        self.generation_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()

    def randomize(self):
        self.running = False
        self.grid = [[random.choice([0, 1]) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation = 0
        self.generation_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    game = GameOfLife(root)
    root.mainloop()
