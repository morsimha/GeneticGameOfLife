from genetic_algorithm import genetic_algorithm
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFileDialog, QPushButton, QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush
import sys
import random
import json


class GameOfLife(QMainWindow):
    def __init__(self, grid_size=20, cell_size=30):
        super().__init__()

        self.grid_size = grid_size
        self.cell_size = cell_size
        self.running = False
        self.generation = 0

        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Game of Life")
        self.setGeometry(100, 100, 600, 1300)  # Fixed window size

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

        self.save_button = QPushButton("Save Grid")
        self.save_button.clicked.connect(self.save_grid)
        self.controls_layout.addWidget(self.save_button, 1, 0)

        self.load_button = QPushButton("Load Grid")
        self.load_button.clicked.connect(self.load_grid)
        self.controls_layout.addWidget(self.load_button, 1, 1)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        self.controls_layout.addWidget(self.settings_button, 1, 2)

        self.optimize_button = QPushButton("Optimize Grid")
        self.optimize_button.clicked.connect(self.optimize_with_genetic_algorithm)
        self.controls_layout.addWidget(self.optimize_button, 1, 2)

        self.generation_label = QLabel(f"Generation: {self.generation}")
        self.controls_layout.addWidget(self.generation_label, 2, 0, 1, 4)

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

    def save_grid(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Grid", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, "w") as f:
                json.dump(self.grid, f)

    def load_grid(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Grid", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, "r") as f:
                self.grid = json.load(f)
            # Update grid_size to match the loaded grid's size
            self.grid_size = len(self.grid)
            self.canvas.set_grid(self.grid)
    #        self.setGeometry(100, 100, self.grid_size * self.cell_size, self.grid_size * self.cell_size + 100)


    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

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
            # Check if the neighbor indices are within bounds
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                count += self.grid[ny][nx]
        return count
    
    
    def optimize_with_genetic_algorithm(self,_, pop_size=20, max_generations=100, generations_until_stop=200):
    #    pop_size = 20
        best_grid, best_score = genetic_algorithm(pop_size, self.grid_size, max_generations, generations_until_stop)
        self.grid = best_grid
        self.generation = best_score[0]
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.grid)


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


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Simulation Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.grid_size_input = QLineEdit(str(parent.grid_size))
        self.layout.addWidget(QLabel("Grid Size:"))
        self.layout.addWidget(self.grid_size_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def save_settings(self):
        grid_size = int(self.grid_size_input.text())
        self.parent().grid_size = grid_size
        self.parent().grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Adjust cell size based on the grid size and fixed window size
        self.parent().cell_size = 800 // grid_size  # Adjust cell size to fit the fixed window size
        self.parent().canvas.set_grid(self.parent().grid)

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GameOfLife()
    game.show()
    sys.exit(app.exec_())
