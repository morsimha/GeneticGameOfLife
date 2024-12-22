import random
import copy
import math

# Function to count live neighbors of a cell
def count_live_neighbors(grid, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    grid_size = len(grid)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            count += grid[ny][nx]
    return count

# Function to simulate one step of the Game of Life
def step(grid):
    grid_size = len(grid)
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for y in range(grid_size):
        for x in range(grid_size):
            live_neighbors = count_live_neighbors(grid, x, y)
            if grid[y][x] == 1:
                if live_neighbors in [2, 3]:
                    new_grid[y][x] = 1
            else:
                if live_neighbors == 3:
                    new_grid[y][x] = 1
    return new_grid

# Fitness function: we maximize the number of generations before the grid stabilizes or dies
# and also maximize the number of live cells at the end minus at the beginning
# seen feature is added to recognize the stabilization of the grid
def fitness(grid, max_generations):
    generations = 0
    seen = set()
    
    # Count the number of live cells at the start
    initial_alive_cells = sum(sum(row) for row in grid)
    max_diff = 0
    max_diff_gen = 0
    while generations < max_generations:
        grid_tuple = tuple(tuple(row) for row in grid)
        if grid_tuple in seen:
            break
        seen.add(grid_tuple)
        grid = step(grid)
        generations += 1

        alive_cells = sum(sum(row) for row in grid)
        # updating the max size of the Metuselah
        if alive_cells - initial_alive_cells > max_diff:
            max_diff = alive_cells - initial_alive_cells
            max_diff_gen = generations


    # Count the number of live cells at the end
    final_alive_cells = sum(sum(row) for row in grid)
    
    # The fitness is the difference between the final and initial live cells, along with generations

    #(initial_alive_cells, final_alive_cells) is a tuple of the number of live cells at the start and end
    # Ensure we only return valid fitness when max_diff > 0
    if max_diff == 0:
        generations = 0  # Indicate invalid solution
    return generations, max_diff, (initial_alive_cells, final_alive_cells, max_diff_gen)

# Function to create an initial population of grids
# each inital configuration will contain a random 5x5 grid with 0s and 1s
def create_initial_population(population_size, grid_size, initial_alive_cells=5):
    population = []
    for _ in range(population_size):
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        start_x = random.randint(0, grid_size - initial_alive_cells)
        start_y = random.randint(0, grid_size - initial_alive_cells)
        for y in range(start_y, start_y + initial_alive_cells):
            for x in range(start_x, start_x + initial_alive_cells):
                grid[y][x] = random.choice([0, 1])
        population.append(grid)
    return population

# Selection function using tournament selection method
# Selects the best individual from a random subset of the population
def tournament_selection(population, fitness_scores, tournament_size=3):
    selected = []
    # Repeat the tournament selection process to select the entire population
    for _ in range(len(population)):
        # Randomly select 'tournament_size' number (3) of individuals from the given population
        # and sort them based on their fitness scores
        if len(population) >= tournament_size:
            tournament = sorted(list(zip(population, fitness_scores)), key=lambda x: x[1][0], reverse=True)
            # Select the winner of the tournament based on the maximum fitness score
            winner = max(tournament, key=lambda x: x[1])[0]
            selected.append(winner)
        else:
            for chromosome in population:
                selected.append(chromosome)
            break
    return selected

# Selection function using roulette wheel selection method
# Selects individuals based on their fitness scores

def roulette_wheel_selection(population, fitness_scores):
    selected = []
    population_size = len(population)
    
    # Rank individuals by fitness (ascending order, worst to best)
    sorted_population = sorted(zip(population, fitness_scores), key=lambda x: x[1][1])
    
    # Assign ranks (1 is the worst, N is the best)
    ranks = list(range(1, population_size + 1))
    
    # Calculate rank-based probabilities
    total_rank = sum(ranks)
    probabilities = [rank / total_rank for rank in ranks]
    
    # Apply a bias for top ranks 
    # using 2 as the bias factor, but can be adjusted
    bias_factor = 2 
    probabilities = [p ** bias_factor for p in probabilities]
    
    # Normalize probabilities
    total_prob = sum(probabilities)
    probabilities = [prob / total_prob for prob in probabilities]
    
    # Create cumulative distribution
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    
    # Perform selection
    for _ in range(population_size):
        random_number = random.uniform(0, 1)
        for i, cumulative_prob in enumerate(cumulative_probabilities):
            if random_number <= cumulative_prob:
                selected.append(sorted_population[i][0])
                break
    
    return selected


def crossover(parent1, parent2):
    """
    Perform crossover by replacing between 1 to 5 rows from the bottom of parent1
    with rows from parent2, starting at the first row containing at least one '1'.
    """
    rows = len(parent1)
    
    # Find the first row from the bottom with at least one '1' in parent1
    start_row = None
    for i in range(rows - 1, -1, -1):
        if 1 in parent1[i]:
            start_row = i
            break
    
    # If no '1' is found, return the original parent1
    if start_row is None:
        return parent1
    
    # Randomly select the number of rows to replace (1 to 5)
    num_rows = random.randint(1, min(5, rows - start_row))
    
    # Perform the row replacement
    child = [row[:] for row in parent1]  # Create a copy of parent1
    for i in range(num_rows):
        if start_row + i < rows:
            child[start_row + i] = parent2[start_row + i]
    
    return child

# Mutation function: randomly flip cell's state
# 50% chance to flip a 1 to 0 or a 0 to 1 (killing a cell or reviving a dead cell)
# relying on the mutation rate and 1's amount to decide how many cells to flip
def mutate(grid, MUTATION_RATE):
    grid_size = len(grid)
    ones_positions = [(y, x) for y in range(grid_size) for x in range(grid_size) if grid[y][x] == 1]
    for _ in range(random.randint(0, int(MUTATION_RATE * len(ones_positions)))):
        if random.random() > 0.5 and ones_positions:
            y, x = random.choice(ones_positions)
            grid[y][x] = 0
        else:
            y, x = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            grid[y][x] = 1
    return grid

# Main function for the genetic algorithm
def genetic_algorithm(population_size, grid_size, max_generations, stabilization_generations, MUTATION_RATE):
    # Generate initial random population, each grid is a 2D array of 0s and 1s
    population = create_initial_population(population_size, grid_size)

    avg_fitness_graph_data = []  # List to store averagefitness over generations
    best_fitness_graph_data = []  # List to store best fitness over generations

    # Calculate fitness scores for each grid, using game of life simulation for each grid
    # returns a tuple of (generations, alive_cells), for each grid
    fitness_scores = []
    for chromosome in population:
        curr_fitness = fitness(chromosome, max_generations)
        fitness_scores.append(curr_fitness)

    average_fitness = int(sum(score[1] for score in fitness_scores) / len(fitness_scores))
    avg_fitness_graph_data.append(average_fitness)
    print(f"Initial Average Fitness: {average_fitness}")
    # Find the best solution (the chromosome with the highest fitness score, based on cell difference between start and end)
    best_solution = max(zip(population, fitness_scores), key=lambda x: x[1][0])
    best_chromosome = best_solution[0]
    best_fitness = best_solution[1]

    best_fitness_graph_data.append(best_fitness[1])
    print(f"Initial Best Fitness: {best_fitness[1]}")   
    
    # Iterate through generations
    for generation in range(stabilization_generations):
        # Remove elements from population and fitness_scores if they have reached the max_generations or have a fitness score of 0
        try:
            population, fitness_scores = zip(*[(chromosome, score) for chromosome, score in zip(population, fitness_scores) if score[0] < max_generations and score[1] != 0])
        except ValueError:
            break
        population, fitness_scores = list(population), list(fitness_scores)
        # we decide to use roulette wheel selection with 70% probability, for better results
        if random.random() < 0.7:
            selected = roulette_wheel_selection(population, fitness_scores)
        else:
            selected = tournament_selection(population, fitness_scores)
        offspring_population = []
        
        # Crossover and mutation
        # we decide to duplicate 70% probability, for better results
        for _ in range(len(population)):
            fitness_scores = []
            # taking 2 parents from the selected population, after the selection process
            parent1 = random.choice(selected)
            if random.random() < 0.7:
                offspring = copy.deepcopy(parent1)
                offspring = mutate(offspring, MUTATION_RATE)
            else:
                offspring1 = copy.deepcopy(parent1)
                parent2 = random.choice(selected)
                offspring2 = copy.deepcopy(parent2)
                offspring = crossover(offspring1, offspring2)
            offspring_population.append(offspring)
        
        #always keep the best chromosome from the previous generation
        offspring_population.append(best_chromosome)

        population = offspring_population
        for chromosome in population:
            curr_fitness = fitness(chromosome, max_generations)
            fitness_scores.append(curr_fitness)


        fitness_values = [score[1] for score in fitness_scores]

        # Calculate the average fitness of the current generation
        average_fitness = int(sum(score[1] for score in fitness_scores) / len(fitness_scores))
        avg_fitness_graph_data.append(average_fitness)


        # Track the best solution
        best_fitness_value = 0
        for i in range(len(population)):
            if fitness_scores[i][1] > best_fitness_value:
                best_chromosome = population[i]
                best_fitness_value = fitness_scores[i][1]
                best_fitness = fitness_scores[i]

        best_fitness_graph_data.append(best_fitness_value)

        print(f"Generation {generation} Fitness Scores: {fitness_values} ")
        print(f"Generation {generation} best_chromosome's fitness: {best_fitness[1]}")
        print(f"Generation {generation} Average Fitness: {average_fitness}\n")
        print("Average Fitness over generations: ",avg_fitness_graph_data)
        print(f"Best Fitness over generations: {best_fitness_graph_data}\n\n")

        # Return the best grid and its fitness score if the population size is less than 3 (tournament size)
        if len(population) < 3:
            break

    
    return best_chromosome, best_fitness, avg_fitness_graph_data, best_fitness_graph_data
