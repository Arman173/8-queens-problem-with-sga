"""
    By Armando Canul, Diana, Arturo - 03/10/2024

    A example for simple genetic algorithm (SGA) implementation.
    the problem consist in found the correct queens positions where
    any don't threaten.
"""
import random
import pygame
import sys

# GLOBAL VARIABLES (SETTING AND OTHERS)
# PYGAME SETTINGS
N = 8
BOX_WIDTH = 60
GRID_DIMENSION = N
WINDOW_WIDTH = WINDOW_HEIGHT = BOX_WIDTH * GRID_DIMENSION
# colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
QUEEN_COLOR = (255, 0, 0)  # Red for queens

# SGA CONST AND SETTINGS
GENES = [1,2,3,4,5,6,7,8]
POPULATION_SIZE = 50

# CLASSES
class Chromosome:
    def __init__(self) -> None:
        self.length = 8 * 2
        self.fitness = -1
        self.positions = []
        for _ in range(0, self.length):
            self.positions.append(0)
    
    def setData(self, d: list) -> None:
        self.positions = d
    
    def tuples(self):
        tuplesList = []
        for i in range(0, self.length, 2):
            t = (self.positions[i], self.positions[i+1])
            tuplesList.append(t)
        return tuplesList
    
    def randomGenes(self) -> None:
        # generate a random number for chromosome data
        for i in range(0, self.length):
            self.positions[i] = ranGene()
    
    def crossover(self, parent1, parent2) -> bool:
        # crossover function
        ranIndex = int(random.uniform(0.6,1) * self.length) - 1
        child1 = Chromosome()
        child1.setData(parent1.positions[:ranIndex] + parent2.positions[ranIndex:])
        child2 = Chromosome()
        child2.setData(parent2.positions[:ranIndex] + parent1.positions[ranIndex:])

        if child1.Fitness() >= child2.Fitness():
            self.positions = child1.positions
        else:
            self.positions = child2.positions
    
    # calculate fitness from target string
    # fitness function, depends from the what similar is Individual than target
    def Fitness(self):
        self.fitness = 0

        # check raws and columns
        x_pos = set()
        y_pos = set()
        for i in range(0, self.length):
            # par (x)
            if i % 2 == 0:
                if self.positions[i] not in x_pos:
                    x_pos.add(self.positions[i])
                else:
                    self.fitness += 1
            else: # impar (y)
                if self.positions[i] not in y_pos:
                    y_pos.add(self.positions[i])
                else:
                    self.fitness += 1
        
        # check diagonals
        posList = self.tuples()
        # print(self.positions)
        # print(posList)
        for pos in posList:
            # print(pos)
            x, y = pos
            for queen in posList:
                # print("\t",queen)
                # Recorrer diagonal principal (↘ y ↖)
                for i in range(1, N):
                    # ↘ Diagonal hacia abajo-derecha
                    if x + i < N and y + i < N:
                        if (x + i, y + i) == queen:
                                self.fitness += 1
                        # diagonales.append((x + i, y + i))
                    
                    # ↖ Diagonal hacia arriba-izquierda
                    if x - i >= 1 and y - i >= 1:
                        if (x - i, y - i) == queen:
                                self.fitness += 1
                        # diagonales.append((x - i, y - i))

                # Recorrer diagonal secundaria (↙ y ↗)
                for i in range(1, N):
                    # ↙ Diagonal hacia abajo-izquierda
                    if x + i < N and y - i >= 1:
                        if (x + i, y - i) == queen:
                                self.fitness += 1
                        # diagonales.append((x + i, y - i))
                    
                    # ↗ Diagonal hacia arriba-derecha
                    if x - i >= 1 and y + i < N:
                        if (x - i, y + i) == queen:
                                self.fitness += 1
                        # diagonales.append((x - i, y + i))
        
        return self.fitness
    
    def mutation(self) -> None:
        for i in range(0, self.length):
            p_m = random.random()
            if p_m >= 0.1 and p_m <= 0.3:
                self.positions[i] = ranGene()
    
    def getFitness(self) -> int:
        return self.fitness
    
    # def getLength(self) -> int:
    #     return self.length

# FUNCTIONS

# function to draw grid in pygame
def draw_grid(display):
    for r in range(GRID_DIMENSION):
        for c in range(GRID_DIMENSION):
            if (r + c) % 2 == 0:
                color = WHITE_COLOR
            else:
                color = BLACK_COLOR
            pygame.draw.rect(display, color, pygame.Rect(c * BOX_WIDTH, r * BOX_WIDTH, BOX_WIDTH, BOX_WIDTH))

def draw_queens(display, queens: list):
    for queen in queens:
        x, y = queen
        pygame.draw.circle(display, QUEEN_COLOR, ((x-0.5)*BOX_WIDTH,(y-0.5)*BOX_WIDTH), BOX_WIDTH/2)
    # pygame.draw.circle(display, QUEEN_COLOR, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), BOX_WIDTH/2)

# return a random gene from GENES (valid genes list)
def ranGene():
    r = random.randint(0, len(GENES) - 1)
    return GENES[r]

# return a random population with N elements and each element
# has len(T) (target length) length
def generateInitialPopulation(N: int):
    generated = []
    for _ in range(0, N):
        new_chromosome = Chromosome()
        new_chromosome.randomGenes()
        generated.append(new_chromosome)
    return generated

def selection(population):
    # create a list for new population (new generation)
    new_population = []
    # order our population by fitness, lower to greater
    population = sorted(population, key = lambda chromosome:chromosome.Fitness())

    # get the 10% index from population list
    n = int(0.1*POPULATION_SIZE)
    # save the 10% of best childs
    new_population.extend(population[:n])

    if population[0].getFitness() == 0:
        return [population, True]

    # get the 90% index from population list
    n = int(0.9*POPULATION_SIZE)
    # get the 50% index from population list, this is for get the top 50 of fitness
    nf = int(0.5*POPULATION_SIZE)
    for _ in range(0, n):
        parents = random.choices(population[:nf], k=17)
        parents = sorted(parents, key = lambda chromosome:chromosome.getFitness())
        child = Chromosome()
        child.crossover(parents[0], parents[1])
        child.mutation()
        new_population.append(child)
    
    return [new_population, False]

def main():

    # Initialize Pygame
    pygame.init()
    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("8-Queens Problem")

    found = False
    generation = 0
    population = generateInitialPopulation(POPULATION_SIZE)
    while not found:
        generation+=1
        population, found = selection(population)
        print(generation, "generation", "best", population[0].positions, "fitness", population[0].getFitness())
        if found:
            found = True
    
    draw_grid(display)
    draw_queens(display, population[0].tuples())
    pygame.display.flip()

    # wait for close event (click in close button window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# execute main function
if __name__ == "__main__":
    main()