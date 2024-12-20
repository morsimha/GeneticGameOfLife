from genetic_algorithm import genetic_algorithm
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFileDialog, QPushButton, QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush
import sys
import random
import json
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting the graph


class GeneticGameOfLife(QMainWindow):
    def __init__(self, grid_size=50, cell_size=10):
        super().__init__()

        self.grid_size = grid_size
        self.cell_size = cell_size
        self.running = False
        self.generation = 0
        self.future_generation = 0
        self.fitness_data = []  # List to store fitness over generations

        self.population = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Genetic Game of Life")
        self.setGeometry(100, 100, 600, 1000)  # Fixed window size

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.canvas = Canvas(self.population, self.cell_size)
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

        self.save_button = QPushButton("Save Chromosome")
        self.save_button.clicked.connect(self.save_chromosome)
        self.controls_layout.addWidget(self.save_button, 1, 0)

        self.load_button = QPushButton("Load Chromosome")
        self.load_button.clicked.connect(self.load_chromosome)
        self.controls_layout.addWidget(self.load_button, 1, 1)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        self.controls_layout.addWidget(self.settings_button, 1, 2)

        self.optimize_button = QPushButton("Evolve Chromosome")
        self.optimize_button.clicked.connect(self.optimize_with_genetic_algorithm)
        self.controls_layout.addWidget(self.optimize_button, 1, 2)

        self.generation_label = QLabel(f"Generation: {self.generation}")
        self.controls_layout.addWidget(self.generation_label, 2, 0, 1, 1)

        self.future_generation_label = QLabel(f"Future Generation it will stabilize: {self.future_generation}")
        self.controls_layout.addWidget(self.future_generation_label, 2, 1, 1, 4)

        self.starting_cells_label = QLabel(f"Initial Cells: {self.population.count(1)}")
        self.controls_layout.addWidget(self.starting_cells_label, 2, 3, 1, 4)


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
        self.population = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.population)

    def randomize(self):
        self.running = False
        self.timer.stop()
        self.generation = 0
        self.population = [[random.choice([0, 1]) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.population)

    def save_chromosome(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Chromosome", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, "w") as f:
                json.dump(self.population, f)

    def load_chromosome(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Chromosome", "", "JSON Files (*.json)", options=options)
        if file_name:
            with open(file_name, "r") as f:
                self.population = json.load(f)
            self.grid_size = len(self.population)
            self.canvas.set_grid(self.population)

    def open_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def step(self):
        new_population = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.population[y][x] == 1:
                    if live_neighbors in [2, 3]:
                        new_population[y][x] = 1
                else:
                    if live_neighbors == 3:
                        new_population[y][x] = 1
        self.population = new_population
        self.generation += 1
        self.generation_label.setText(f"Generation: {self.generation}")
        self.canvas.set_grid(self.population)

    def count_live_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                count += self.population[ny][nx]
        return count

    def optimize_with_genetic_algorithm(self, _, pop_size=500, max_generations=500, generations_until_stop=10):
        best_chromosome, best_score, fitness_graph_data = genetic_algorithm(pop_size, self.grid_size, max_generations, generations_until_stop)
        self.population = best_chromosome
        self.future_generation = best_score[0]
        display_stats = best_score[2]

        self.fitness_data = fitness_graph_data
        
        # # Storing fitness data for graph plotting
        # self.fitness_data.append(best_score)

        curr_population = sum(cell == 1 for row in best_chromosome for cell in row)
        self.starting_cells_label.setText(f"Initial Cell number: {curr_population}, Peak happens at generation: {display_stats[2]}, with population of {curr_population + best_score[1]} cells and with max diff of {best_score[1]} cells.")
        
        self.plot_button = QPushButton("Plot Fitness Graph")
        self.plot_button.clicked.connect(self.plot_fitness_graph)
        self.controls_layout.addWidget(self.plot_button, 3, 0, 1, 4)

        
        self.canvas.set_grid(self.population)
        self.canvas.update()

    def plot_fitness_graph(self):
        generations = list(range(len(self.fitness_data)))  # Generation numbers from 0 to len(fitness_values)-1
        # Plotting the graph
        plt.plot(generations, self.fitness_data, marker='o', color='b')
        plt.title("Fitness over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.grid(True)
        plt.show()



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
        self.parent().population = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.parent().cell_size = 800 // grid_size
        self.parent().canvas.set_grid(self.parent().population)

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = GeneticGameOfLife()
    game.show()
    sys.exit(app.exec_())