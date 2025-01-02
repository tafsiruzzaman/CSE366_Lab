import pygame
from agent import Agent
from environment import Environment
import numpy as np
import random

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800  # Increased height to accommodate updates below the grid
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class Scheduling Visualization")
font = pygame.font.Font(None, 24)

# Environment setup
num_classes = 8
num_students = 5
environment = Environment(num_classes, num_students)
class_assignments = environment.generate_assignments()

# Initialize agents (students)
agents = [Agent(id=i, availability=environment.student_availabilities[i], preferences=environment.student_preferences[i]) for i in range(num_students)]

# Genetic Algorithm parameters
population_size = 50
mutation_rate = 0.1
n_generations = 100
generation_delay = 1000  # Delay (milliseconds) between each generation for visualization

# Updates list to display below the grid
updates = []
max_updates = 5  # Max number of updates to display at once

# Fitness Function (Conflict Minimization and Preference Alignment)
def fitness(individual):
    """Calculate fitness of the schedule by minimizing conflict and preference penalties."""
    conflict_penalty = 0
    preference_penalty = 0

    # Check each class assigned in the individual's schedule
    for class_id, student in enumerate(individual):
        slot = class_id % 24  # Assume class_id mod 24 is the slot (simplification)

        # Conflict penalty: penalize if student is unavailable at the assigned time
        if environment.student_availabilities[student, slot] == 0:
            conflict_penalty += 1

        # Preference penalty: penalize if the time slot is not preferred
        preference_penalty += 1 / max(1, environment.student_preferences[student, slot])

    # Total fitness is the sum of conflict penalty and preference penalty
    return conflict_penalty + preference_penalty

# Selection Function (Selecting the top half of the population based on fitness)
def selection(population):
    """Selects the top half of the population based on fitness."""
    return sorted(population, key=fitness)[:population_size // 2]

# Crossover Function (Single-Point Crossover)
def crossover(parent1, parent2):
    """Performs single-point crossover to combine two parent schedules."""
    point = random.randint(1, num_classes - 1)
    child = np.concatenate([parent1[:point], parent2[point:]])
    return child

# Mutation Function (Random Assignment Mutation)
def mutate(individual):
    """Randomly mutates the class assignments."""
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, num_students - 1)  # Reassign class to a random student
    return individual

# Initialize population
population = environment.generate_assignments()

# Main loop for genetic algorithm and visualization
running = True
best_solution = None
best_fitness = float('inf')
generation_count = 0
max_fitness_achieved = float('inf')  # Variable to track the max fitness achieved

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm Step-by-Step per Generation
    # Select parents based on fitness
    selected = selection(population)

    # Crossover and mutation to create next generation
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))

    # Update population with the next generation
    population = next_generation

    # Find the best solution in the current generation
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    # Track max fitness achieved
    if current_fitness < max_fitness_achieved:
        max_fitness_achieved = current_fitness

    # Draw current generation's best solution on the grid
    environment.draw_grid(screen, font, current_best)

    # Display generation and fitness info on the right panel
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness (Current): {best_fitness:.2f}", True, (0, 0, 0))
    max_fitness_text = font.render(f"Max Fitness Achieved: {max_fitness_achieved:.2f}", True, (0, 0, 0))

    screen.blit(generation_text, (SCREEN_WIDTH - 300, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 300, 80))
    screen.blit(max_fitness_text, (SCREEN_WIDTH - 300, 110))

    # Add update for the current generation to the updates list
    update_text = f"Generation {generation_count + 1}: Best Fitness = {best_fitness:.2f}"
    updates.append(update_text)
    if len(updates) > max_updates:
        updates.pop(0)

    # Display the list of updates below the grid
    update_start_y = 500
    for i, update in enumerate(updates):
        update_surface = font.render(update, True, (0, 0, 0))
        screen.blit(update_surface, (50, update_start_y + i * 25))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1
    if generation_count >= n_generations:
        break

# Keep window open after completion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
