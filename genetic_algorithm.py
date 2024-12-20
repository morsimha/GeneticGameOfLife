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
# and also maximize the number of live cells at the end minus at the beginning
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
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%max_diff, gen: ",max_diff, max_diff_gen)
            max_diff_gen = generations

    # Count the number of live cells at the end
    final_alive_cells = sum(sum(row) for row in grid)
    
    # The fitness is the difference between the final and initial live cells, along with generations

    #(initial_alive_cells, final_alive_cells) is a tuple of the number of live cells at the start and end

    return generations, max_diff, (initial_alive_cells, final_alive_cells, max_diff_gen)

# Function to create an initial population of grids
def create_initial_population(population_size, grid_size):
    # Generates initial population of chromosomes (grids) with 90% chance of 0 and 10% chance of 1
    return [
        [[1 if random.random() < 0.01 else 0 for _ in range(grid_size)] for _ in range(grid_size)]
        for _ in range(population_size)
    ]

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
def genetic_algorithm(population_size, grid_size, max_generations, stabilization_generations):
    # Generate initial random population, each grid is a 2D array of 0s and 1s
    population = create_initial_population(population_size, grid_size)

    # Print population to check
    print(f"Initial Population: {len(population)} grids")

    # Calculate fitness scores for each grid, using game of life simulation for each grid
    #returns a tuple of (generations, alive_cells), for each grid
    fitness_scores = []
    for chromosome in population:

        fitness_scores.append(fitness(chromosome, max_generations))

    
    # Print fitness scores for debugging
    print(f"Fitness Scores (generations, cell_diff, initial_alive_cells, final_alive_cells)): {fitness_scores}")

    # # Check if the fitness_scores is not empty
    # if not fitness_scores:
    #     raise ValueError("Fitness scores are empty. Ensure the population is correctly initialized and the fitness function is returning valid scores.")

    # Find the best solution (the chromosome with the highest fitness score, based on cell difference between start and end)
    best_solution = max(zip(population, fitness_scores), key=lambda x: x[1][0])
    best_chromosome = best_solution[0]
    best_fitness = best_solution[1]
    # print(best_chromosome)
    print("best_fitness ",best_fitness)
    # return best_grid, best_score

    # עד פה חקרנו 10 גרידים, כל אחד מהם עשה סימולציה של משחק החיים וקיבל ציון של כמה דורות שרד וכמה תאים חיים       
    
    # Iterate through generations
    for generation in range(stabilization_generations):
        selected = tournament_selection(population, fitness_scores)
        offspring_population = []

        # Ensure selected has an even number of individuals
        if len(selected) % 2 != 0:
            selected.append(random.choice(population))  # Adding a random individual to make it even
        
        # Crossover and mutation
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            offspring = crossover(parent1, parent2)
            offspring = mutate(offspring)
            offspring_population.append(offspring)
        population = offspring_population
        fitness_scores = [fitness(chromosome, max_generations) for chromosome in population]
        
        # Print the new fitness scores for debugging
        print(f"Generation {generation} Fitness Scores: {fitness_scores}")

        # Track the best solution
        current_best_solution = max(zip(population, fitness_scores), key=lambda x: x[1][0])
        if current_best_solution[1][0] > best_fitness[0]:
            best_chromosome = current_best_solution[0]
            best_fitness = current_best_solution[1]

        print("#########best_fitness (generations, cell_diff, initial_alive_cells, final_alive_cells, max_diff_gen))",best_fitness)

        # Return the best grid and its fitness score if the population size is less than 3 (tornumanet size)
        if len(population) < 3:
            break

    
    return best_chromosome, best_fitness
