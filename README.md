# Genetic Game of Life

A GUI-based implementation of Conway's Game of Life enhanced with genetic algorithms to discover and evolve interesting patterns.

## Overview

This project combines Conway's Game of Life cellular automaton with genetic algorithms to evolve patterns that exhibit interesting behaviors, such as long-lasting growth or complex evolutionary paths. The application provides a visual interface to watch these patterns evolve and interact in real-time.

## Features

- **Interactive Game of Life Simulation**
  - Start, stop, and clear controls
  - Random pattern generation
  - Real-time visualization

- **Genetic Algorithm Optimization**
  - Evolve patterns that maximize longevity and growth
  - Multiple selection strategies (tournament and roulette wheel)
  - Customizable genetic parameters

- **Pattern Management**
  - Save evolved patterns to JSON files
  - Load saved patterns for further experimentation
  - Adjust grid size and simulation settings

- **Fitness Analysis**
  - Plot fitness trends over generations
  - Track best and average fitness metrics
  - Identify generation when peak population occurs

## Implementation Details

### Genetic Algorithm Components

- **Selection Mechanisms**: 
  - Tournament selection picks the best individuals from random subsets
  - Roulette wheel selection weighs individuals by fitness ranking

- **Crossover Operator**:
  - Takes rows from two parent patterns to create offspring
  - Preserves key structures while allowing for variation

- **Mutation Operator**:
  - Randomly flips cell states based on mutation rate
  - Adds diversity to prevent premature convergence

- **Fitness Function**:
  - Evaluates patterns based on:
    - Number of generations before stabilization
    - Maximum difference between initial and peak cell count
    - Time to reach peak population

### Game of Life Simulation

- Standard Conway's Game of Life rules:
  - Live cells with 2-3 neighbors survive
  - Dead cells with exactly 3 neighbors become alive
  - All other cells die or remain dead

## Installation

```bash
# Install required dependencies
pip install PyQt5 matplotlib numpy
```

## Usage

```bash
# Run the application
python GeneticGameOfLife.py
```

### Controls

- **Start/Stop**: Control the Game of Life simulation
- **Clear**: Reset the grid to empty
- **Randomize**: Generate a random initial pattern
- **Evolve Chromosome**: Run the genetic algorithm to find optimal patterns
- **Save/Load Chromosome**: Export or import patterns in JSON format
- **Plot Fitness Graph**: Visualize fitness trends during evolution
- **Settings**: Adjust grid size and other parameters

### Simulation Parameters

- **Population Size**: Number of candidate patterns per generation
- **Max Generations**: Maximum steps to simulate for each pattern
- **Generations Until Stop**: Number of genetic algorithm iterations
- **Mutation Rate**: Probability of mutation during reproduction
- **Grid Size**: Dimensions of the Game of Life grid

## Example Patterns

The repository includes a sample.json file containing a pre-evolved pattern with interesting emergent properties. Load this pattern to observe complex behavior over multiple generations.

## How It Works

1. The genetic algorithm starts with a population of random patterns
2. Each pattern is evaluated by simulating Game of Life rules for multiple generations
3. Patterns with higher fitness (longer survival, more growth) are selected for reproduction
4. Selected patterns undergo crossover and mutation to create new offspring
5. The process repeats for multiple generations, evolving increasingly interesting patterns
6. The best pattern found is displayed in the GUI for visualization

## Technical Architecture

- **GeneticAlgorithm.py**: Core evolutionary algorithm implementation
- **GeneticGameOfLife.py**: PyQt5-based GUI and simulation controller

## Contributing

Feel free to fork this project and submit pull requests with improvements. Some ideas for extensions:

- Add more complex fitness functions
- Implement additional selection methods
- Create a pattern gallery/library
- Add 3D visualization capabilities
