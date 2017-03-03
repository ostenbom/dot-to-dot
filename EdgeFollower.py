import sys
import math
import numpy as np
import warnings
warnings.simplefilter('ignore', np.RankWarning)

from DistanceUtils import lineAngle
from EdgeMatrix import EdgeMatrix

TRACE_SIZE_THRESHOLD = 4
POINTS_FOR_DIRECTION = 5

class EdgeFollower():

    def __init__(self, edgeMatrix, width, height):
        self.edgeMatrix = edgeMatrix
        self.points = edgeMatrix.points[:]
        self.width = width
        self.height = height
        self.traces = []
        self.hasFoundTraces = False

    def getTraces(self):
        if not self.hasFoundTraces:
            self.traces = self.findTraces()
            self.hasFoundTraces = True
        return self.traces

    def findTraces(self):
        traces = []

        while len(self.points):
            point = self.points.pop(0)
            trace = self.makeTrace(point)
            if len(trace) > TRACE_SIZE_THRESHOLD:
                traces.append(trace)

        return traces

    def makeTrace(self, startingPoint, limit = sys.maxint, persistent = True):
        self.edgeMatrix.markFalseAt(startingPoint)
        trace = [startingPoint]
        nextNeighbours = self.edgeMatrix.getTrueNeighbours(startingPoint)
        originalNeighbours = nextNeighbours[:]
        if not len(nextNeighbours):
            return trace

        removed = []


        nextPoint = nextNeighbours[0]
        self.removeFromMatrix(nextPoint)
        removed.append(nextPoint)
        trace.append(nextPoint)
        nextNeighbours = self.edgeMatrix.getTrueNeighbours(nextPoint)

        while len(nextNeighbours) and len(trace) < limit:
            if len(nextNeighbours) == 1:
                nextPoint = nextNeighbours[0]
            elif len(nextNeighbours) == 2 and self.twoNeighboursAdjacent(nextNeighbours):
                nextPoint = self.adjacentNeighbour(nextPoint, nextNeighbours)
            elif len(trace) < POINTS_FOR_DIRECTION: # Trace not long enough for crossroad analysis
                nextPoint = nextNeighbours[0]
            else:
                nextPoint = self.chooseCrossroadsNeighbour(nextPoint, nextNeighbours, trace)

            self.removeFromMatrix(nextPoint)
            removed.append(nextPoint)
            trace.append(nextPoint)
            nextNeighbours = self.edgeMatrix.getTrueNeighbours(nextPoint)

        if persistent:
            if len(originalNeighbours) == 2 and not self.twoNeighboursAdjacent(originalNeighbours):
                otherDirectionTrace = self.makeTrace(originalNeighbours[1])
                otherDirectionTrace.reverse()
                trace = trace + otherDirectionTrace
        else:
            self.edgeMatrix.markTrueAt(startingPoint)
            for point in removed:
                self.addToMatrix(point)

        return trace

    def twoNeighboursAdjacent(self, neighbours):
        x = neighbours[0][0]
        y = neighbours[0][1]
        adjacents = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for adjacent in adjacents:
            if adjacent == neighbours[1]:
                return True

        return False

    def adjacentNeighbour(self, point, neighbours):
        x = point[0]
        y = point[1]
        adjacents = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for neighbour in neighbours:
            for adjacent in adjacents:
                if neighbour == adjacent:
                    return neighbour

    def chooseCrossroadsNeighbour(self, point, neighbours, trace):
        aheadTraces = []
        aheadDirections = []

        # Make ahead traces for each of the crossroad directions
        for point in neighbours:
            for otherPoint in neighbours:
                if otherPoint is not point:
                    self.removeFromMatrix(otherPoint)

            aheadTraces.append(self.getAheadDirection(point))

            for otherPoint in neighbours:
                if otherPoint is not point:
                    self.addToMatrix(otherPoint)

        # Get the linear coefficients for the ahead and behind directions
        behindDirection = self.getBehindDirection(point, trace)
        for ahead in aheadTraces:
            aheadDirections.append(self.aheadDirectionAngle(ahead))

        currentBest = 360
        bestIndex = -1
        for i, ahead in enumerate(aheadTraces):
            straightPoint = (point[0] + 1, point[1] + behindDirection)

            averageAheadAngle = 0
            for aheadPoint in ahead:
                averageAheadAngle += lineAngle(straightPoint, point, aheadPoint)
            averageAheadAngle = float(averageAheadAngle) / len(ahead)
            # print ('aheadAngle: ' + str(averageAheadAngle))

            thisAccute = math.degrees(abs(math.atan(float(behindDirection)) - math.atan(float(aheadDirections[i]))))
            thisObtuse = 180 - thisAccute
            # print ('acute: ', str(thisAccute))
            # print ('obtuse: ', str(thisObtuse))


            thisAngle = thisAccute if abs(averageAheadAngle - thisAccute) < abs(averageAheadAngle - thisObtuse) else thisObtuse
            # print ('thisAngle: ' + str(thisAngle))

            if thisAngle < currentBest:
                currentBest = thisAngle
                bestIndex = i

        for i, neighbour in enumerate(neighbours):
            if i != bestIndex:
                self.points.remove(neighbour)
                self.points.insert(0, neighbour)

        return neighbours[bestIndex]

    def getAheadDirection(self, point):
        return self.makeTrace(point, POINTS_FOR_DIRECTION, False)

    def aheadDirectionAngle(self, ahead):
        xs = [p[0] for p in ahead]
        ys = [p[1] for p in ahead]
        m, c = np.polyfit(xs, ys, 1)

        # print('ahead from: ' + str(ahead[0]) + ' coeff: ' + str(m))
        return m

    def getBehindDirection(self, point, trace):
        fullRecent = trace[:]
        fullRecent.append(point)
        limit = POINTS_FOR_DIRECTION
        mostRecent = []

        while len(fullRecent) and limit > 0:
            mostRecent.append(fullRecent.pop())
            limit -=1

        xs = [p[0] for p in mostRecent]
        ys = [p[1] for p in mostRecent]
        m, c = np.polyfit(xs, ys, 1)

        return m

    def removeFromMatrix(self, point):
        self.edgeMatrix.markFalseAt(point)
        self.points.remove(point)

    def addToMatrix(self, point):
        self.edgeMatrix.markTrueAt(point)
        self.points.append(point)
