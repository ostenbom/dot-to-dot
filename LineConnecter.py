import math
import sys
import numpy as np
import scipy
from scipy import optimize

from DistanceUtils import distanceBetween

class LineConnecter():

    def __init__(self, lines):
        self.lines = lines
        self.indexes = range(len(lines) * 2)
        self.coords = []
        for line in lines:
            start = line[0]
            end = line[-1]
            self.coords.append(start)
            self.coords.append(end)

        self.distanceMatrix = self.generateDistanceMatrix()

        self.solution = []

    def generateDistanceMatrix(self):
        n = len(self.coords)
        distanceMatrix = [[distanceBetween(self.coords[i], self.coords[j]) for i in range(n)] for j in range(n)]
        return distanceMatrix

    def getConnectedLines(self, tries):
        initialSolutions = [self.greedySolution() for i in range(tries)]
        optimizedSolutions = []
        for sol in initialSolutions:
            potentialSolution, potentialFitness = self.anneal(sol)
            optimizedSolutions.append((potentialSolution, potentialFitness))
        bestSolution = min(optimizedSolutions, key=lambda x: x[1])
        print ('--- --- Best Solution: ' + str(bestSolution[1]) + ' --- ---')
        solution = self.solutionIndexesToLines(bestSolution[0])
        self.solution = solution
        return solution

    def greedySolution(self):
        current = np.random.randint(0, len(self.lines))
        currentEnd = self.otherEndIndex(current)
        greedySol = [current]

        freeList = self.indexes[:]
        freeList.remove(current)
        freeList.remove(currentEnd)

        while len(freeList):
            closestDistance = min([(self.distanceMatrix[currentEnd][i], i) for i in freeList], key=lambda x: x[0])
            current = closestDistance[1]
            currentEnd = self.otherEndIndex(current)
            freeList.remove(current)
            freeList.remove(currentEnd)
            greedySol.append(current)

        return greedySol

    def anneal(self, initial, iterations = 10000):
        T = math.sqrt(len(self.coords))
        print ('--- Annealing ' + str(iterations) + ' Initial Temp: ' + str(T) + ' ---')
        alpha = 0.995
        stoppingTemp = 0.000001

        initialFitness = self.indexDistance(initial)

        self.currentSol = initial[:]
        self.currentSolFitness = self.indexDistance(self.currentSol)
        self.bestSol = self.currentSol[:]
        self.bestSolFitness = self.currentSolFitness

        iteration = 1
        while T > stoppingTemp and iteration < iterations:
            candidate = self.currentSol[:]
            upper = np.random.randint(1, len(self.coords))
            lower = np.random.randint(0, len(self.coords) - upper)
            candidate[lower:(lower+upper)] = reversed(candidate[lower:(lower+upper)])
            self.accept(candidate, T)
            T *= alpha
            iteration += 1

        if T > stoppingTemp:
            print ('Ended for Temperature, Iterations: ' + str(iteration))
        else:
            print ('Ended for Iterations, Temperature: ' + str(T))

        print ('Best fitness: ' + str(self.bestSolFitness))
        print ('Improvement: ' + str(initialFitness - self.bestSolFitness))
        return (self.bestSol, self.bestSolFitness)

    def accept(self, candidate, T):
        candidateFitness = self.indexDistance(candidate)
        if candidateFitness < self.currentSolFitness:
            self.currentSol = candidate
            self.currentSolFitness = candidateFitness
            if candidateFitness < self.bestSolFitness:
                self.bestSol = candidate
                self.bestSolFitness = candidateFitness
        else:
            if np.random.random_sample() < self.pAccept(candidateFitness, self.currentSolFitness, T):
                self.currentSol = candidate
                self.currentSolFitness = candidateFitness

    def pAccept(self, candidateFitness, currentFitness, T):
        return math.exp(-abs(candidateFitness - currentFitness) / T)

    def indexDistance(self, sol):
        total = np.sum([self.distanceMatrix[int(sol[self.otherEndIndex(i - 1)])][int(sol[i])] for i in range(1, len(sol))])
        return total

    def otherEndIndex(self, index):
        if index % 2 == 0:
            return index + 1
        else:
            return index - 1

    def solutionIndexesToLines(self, indexes):
        lines = []
        for i in indexes:
            line = self.lines[i / 2]
            if i % 2 == 1:
                # Will this reverse the original line?
                line.reverse()
            lines.append(line)
        return lines

    def calculateSolutionDistance(self, sol):
        solution = sol[:]
        totalDistance = 0
        currLine = solution.pop(0)
        nextLine = solution.pop(0)

        while len(solution):
            curEnd = currLine[-1]
            nextStart = nextLine[0]
            totalDistance += distanceBetween(curEnd, nextStart)
            currLine = nextLine
            nextLine = solution.pop(0)

        return totalDistance
