import math
import sys
import numpy as np
import scipy
from scipy import optimize

from DistanceUtils import distanceBetween

class LineConnector():

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

    def getGreedySolution(self):
        greedySol = self.greedySolution()
        return [self.solutionIndexesToLines(greedySol), self.indexDistance(greedySol), self.longestLines(greedySol, 5)]

    def bestOfManyGreedys(self, amount):
        greedySolutions = []
        for i in range(amount):
            solution = self.greedySolution()
            greedySolutions.append((solution, self.indexDistance(solution)))

        bestGreedy = min(greedySolutions, key=lambda x: x[1])
        return self.solutionIndexesToLines(bestGreedy[0])

    def greedySolution(self):
        current = np.random.randint(0, len(self.indexes))
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

    def indexDistance(self, sol):
        total = np.sum([self.distanceMatrix[int(self.otherEndIndex(sol[i - 1]))][int(sol[i])] for i in range(1, len(sol))])
        return total

    def longestLines(self, sol, amount):
        allLines = [self.distanceMatrix[int(self.otherEndIndex(sol[i-1]))][int(sol[i])] for i in range(1, len(sol))]
        sortedLines = sorted(allLines)
        return sortedLines[amount:]

    def otherEndIndex(self, index):
        if index % 2 == 0:
            return index + 1
        else:
            return index - 1

    def pointToLineIndex(self, point):
        for i in range(len(self.indexes)):
            if point in self.lines[i / 2]:
                return i

    def solutionIndexesToLines(self, indexes):
        lines = []
        for i in indexes:
            line = self.lines[i / 2]
            line = line[:]
            if i % 2 == 1:
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
