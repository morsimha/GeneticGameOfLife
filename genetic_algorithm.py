import random
import copy

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
def fitness(grid, max_generations=100):
    generations = 0
    seen = set()
    
    while generations < max_generations:
        grid_tuple = tuple(tuple(row) for row in grid)
        if grid_tuple in seen:
            break
        seen.add(grid_tuple)
        grid = step(grid)
        generations += 1

    alive_cells = sum(sum(row) for row in grid)
    return generations, alive_cells

# Function to create an initial population of grids
def create_population(pop_size, grid_size):
    # Create a population with 'pop_size' number of grids, each grid is 'grid_size' x 'grid_size'.
    population = [
        [[random.choice([0, 1]) for _ in range(grid_size)] for _ in range(grid_size)]
        for _ in range(pop_size)
    ]
    return population

# Selection function using tournament selection method
# Selects the best individual from a random subset of the population
def tournament_selection(population, fitness_scores, tournament_size=3):
    selected = []
    # Repeat the tournament selection process to select the entire population
    for _ in range(len(population)):
        # Randomly select 'tournament_size' number (3) of individuals from the given population
        tournament = random.sample(list(zip(population, fitness_scores)), tournament_size)
        # print("tournament: ",tournament)
        # Select the winner of the tournament based on the maximum fitness score
        winner = max(tournament, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

# Crossover function to combine two grids (simple 2D array crossover)
def crossover(grid1, grid2):
    grid_size = len(grid1)
    crossover_point = random.randint(0, grid_size - 1)
    new_grid = []
    for y in range(grid_size):
        if y < crossover_point:
            new_grid.append(copy.deepcopy(grid1[y]))
        else:
            new_grid.append(copy.deepcopy(grid2[y]))
    return new_grid

# Mutation function: randomly flip a cell's state
def mutate(grid, mutation_rate=0.01):
    grid_size = len(grid)
    for y in range(grid_size):
        for x in range(grid_size):
            if random.random() < mutation_rate:
                grid[y][x] = 1 - grid[y][x]  # Flip the cell state
    return grid

# Main function for the genetic algorithm
def genetic_algorithm(pop_size, grid_size, max_generations=100, generations_until_stop=200):
    # Generate initial random population, each grid is a 2D array of 0s and 1s
    population = create_population(pop_size, grid_size)

    # Print population to check
    print(f"Initial Population: {len(population)} grids")

    # Calculate fitness scores for each grid, using game of life simulation for each grid
    #returns a tuple of (generations, alive_cells), for each grid
    fitness_scores = [fitness(grid, max_generations) for grid in population]
    
    # Print fitness scores for debugging
    print(f"Fitness Scores (generations, alive_cells): {fitness_scores}")

    # Check if the fitness_scores is not empty
    if not fitness_scores:
        raise ValueError("Fitness scores are empty. Ensure the population is correctly initialized and the fitness function is returning valid scores.")

    # Find the best solution (the grid with the highest fitness score)
    best_solution = max(zip(population, fitness_scores), key=lambda x: x[1][0])
    best_grid = best_solution[0]
    best_score = best_solution[1]
    print(best_grid)
    print(best_score)
    # return best_grid, best_score

    # עד פה חקרנו 10 גרידים, כל אחד מהם עשה סימולציה של משחק החיים וקיבל ציון של כמה דורות שרד וכמה תאים חיים       
    
    # Iterate through generations
    for generation in range(generations_until_stop):
        selected = tournament_selection(population, fitness_scores)
        next_population = []

        # Ensure selected has an even number of individuals
        if len(selected) % 2 != 0:
            selected.append(random.choice(population))  # Add a random individual to make it even
        
        
        # Crossover and mutation
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_population.append(child)

        population = next_population
        fitness_scores = [fitness(grid, max_generations) for grid in population]
        
        # Print the new fitness scores for debugging
        print(f"Generation {generation} Fitness Scores: {fitness_scores}")

        # Track the best solution
        current_best_solution = max(zip(population, fitness_scores), key=lambda x: x[1][0])
        if current_best_solution[1][0] > best_score[0]:
            best_grid = current_best_solution[0]
            best_score = current_best_solution[1]

        # Return the best grid and its fitness score if the population size is less than 3 (tornumanet size)
        if len(population) < 3:
            break

    
    return best_grid, best_score
