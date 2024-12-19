from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush
import sys
import random

class GameOfLife(QMainWindow):
    def __init__(self, grid_size=50, cell_size=10):
        super().__init__()

        self.grid_size = grid_size
        self.cell_size = cell_size
        self.running = False
        self.generation = 0

        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Game of Life")
        self.setGeometry(100, 100, self.grid_size * self.cell_size, self.grid_size * self.cell_size + 100)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.canvas = Canvas(self.grid, self.cell_size)
        self.layout.addWidget(self.canvas)

        self.controls = QWidget()
        self.controls_layout = QGridLayout()
        self.controls.setLayout(self.controls_layout)
        self.layout.addWidget(self.controls)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        self.controls_layout.addWidget(self.start_button, 0, 0)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.controls_layout.addWidget(self.stop_button, 0, 1)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)
        self.controls_layout.addWidget(self.clear_button, 0, 2)

        self.random_button = QPushButton("Randomize")
        self.random_button.clicked.connect(self.randomize)
        self.controls_layout.addWidget(self.random_button, 0, 3)

        self.generation_label = QLabel(f"Generation: {self.generation}")
        self.controls_layout.addWidget(self.generation_label, 1, 0, 1, 4)

        self.timer = QTimer()
        self.timer.timeout.connect(self.step)

    def start(self):
        if not self.running:
            self.running = True
            self.timer.start(100)

    def stop(self):
        self.running = False
        self.timer.stop()

    def clear(self):
        self.running = False
        self.timer.stop()
        self.generation = 0
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.grid)

    def randomize(self):
        self.running = False
        self.timer.stop()
        self.generation = 0
        self.grid = [[random.choice([0, 1]) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.grid)

    def step(self):
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
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.grid)

    def count_live_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                count += self.grid[ny][nx]
        return count

class Canvas(QWidget):
    def __init__(self, grid, cell_size):
        super().__init__()
        self.grid = grid
        self.cell_size = cell_size

    def set_grid(self, grid):
        self.grid = grid
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    painter.setBrush(QBrush(QColor(0, 0, 0)))
                else:
                    painter.setBrush(QBrush(QColor(255, 255, 255)))
                painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameOfLife()
    game.show()
    sys.exit(app.exec_())
