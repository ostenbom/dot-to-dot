import sys
import math
import numpy as np

from EdgeMatrix import EdgeMatrix

TRACE_SIZE_THRESHOLD = 4
POINTS_FOR_DIRECTION = 5

class EdgeFollower(self):

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
            self.edgeMatrix.markFalseAt(point)
            trace = self.makeTrace(point)
            if len(trace) > TRACE_SIZE_THRESHOLD:
                traces.append(trace)

        return traces

    def makeTrace(self, startingPoint, limit = sys.maxint, persistent = True):
        trace = [startingPoint]
        nextNeighbours = self.edgeMatrix.getNeighbours(startingPoint)
        if not len(neighbours):
            return trace

        removed = []

        nextPoint = nextNeighbours[0]
        self.removeFromMatrix(nextPoint)
        self.removed.append(nextPoint)
        trace.append(nextPoint)
        nextNeighbours = self.edgeMatrix.getNeighbours(nextPoint)

        while len(nextNeighbours) and len(trace) < limit:
            if len(nextNeighbours) = 1:
                nextPoint = nextNeighbours[0]
            else:
                nextPoint = bestNextNeighbour(nextPoint, nextNeighbours, trace)

            self.removeFromMatrix(nextPoint)
            self.removed.append(nextPoint)
            trace.append(nextPoint)
            nextNeighbours = self.edgeMatrix.getNeighbours(nextPoint)

        if not persistent:
            for point in removed:
                addToMatrix(point)

        return trace

    def bestNextNeighbour(self, point, neighbours, trace):
        aheadDirections = []
        for point in neighbours:
            for otherPoint in neighbours:
                if otherPoint is not point:
                    self.removeFromMatrix(otherPoint)

            aheadDirections.append(self.getAheadDirection(point))

            if otherPoint in neighbours:
                if otherPoint is not point:
                    self.addToMatrix(otherPoint)

        behindDirection = self.getBehindDirection(point, trace)



        return neighbours[0]

    def getAheadDirection(self, point):
        ahead = makeTrace(point, POINTS_FOR_DIRECTION, False)
        xs = [p[0] for p in ahead]
        ys = [p[1] for p in ahead]
        m, c = np.polyfit(xs, ys, 1)

        return math.arctan(m)

    def getBehindDirection(self, point, trace):
        fullRecent = trace[:].append(point)
        limit = POINTS_FOR_DIRECTION
        mostRecent = []

        while len(fullRecent) and limit > 0:
            mostRecent.append(fullRecent.pop())
            limit -=1

        xs = [p[0] for p in mostRecent]
        ys = [p[1] for p in mostRecent]
        m, c = np.polyfit(xs, ys, 1)

        return math.arctan(m)

    def removeFromMatrix(self, point):
        self.edgeMatrix.markFalseAt(point)
        self.points.remove(point)

    def addToMatrix(self, point):
        self.edgeMatrix.markTrueAt(point)
        self.points.append(point)
