import random

# define the problem and its parameters
def fitness_function(solution):
    return sum(solution)  # maximize the sum of the solution

solution_length = 10
population_size = 20
opposition_probability = 0.5

# initialize the population
population = []
for i in range(population_size):
    solution = [random.randint(0, 1) for j in range(solution_length)]
    population.append(solution)

# divide each solution into two parts
solution_half_length = int(solution_length / 2)

# create half solutions using opposition-based method
for i in range(population_size):
    solution = population[i]
    solution_left = solution[:solution_half_length]
    solution_right = solution[solution_half_length:]
    
    # randomly select another solution to compare with
    j = random.randint(0, population_size - 1)
    solution2 = population[j]
    solution2_left = solution2[:solution_half_length]
    solution2_right = solution2[solution_half_length:]
    
    # use the best parts of the two solutions as the new half solution
    new_solution_left = []
    for k in range(solution_half_length):
        if random.random() < opposition_probability:
            new_solution_left.append(solution_left[k])
        else:
            new_solution_left.append(solution2_left[k])
    
    # combine the new half solution with the original right half to create the new solution
    new_solution = new_solution_left + solution_right
    
    # evaluate the fitness of the new solution and replace the old solution if it is better
    if fitness_function(new_solution) > fitness_function(solution):
        population[i] = new_solution

for invidual in population:
    print(invidual)
