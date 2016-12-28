import math
import sys
from operator import itemgetter

from SegmentBoard import SegmentBoard
from DistanceUtils import distanceBetween, angleBetween
from IntermediateImage import IntermediateImage

class TraceFollower():

    def __init__(self, outlines, width, height, minLineLength):
        self.segments = outlines
        self.width = width
        self.height = height
        self.minLineLength = minLineLength

    def getDottedSegments(self):
        return self.findDefiningPoints(self.minLineLength)

    def findDefiningPoints(self, minLineLength):
        newSegments = []
        while len(self.segments):
            segment = self.segments.pop(0)
            trace = self.makeSegmentTrace(segment)
            if len(trace):
                newSegment = self.makePointsFromTrace(trace, minLineLength)
                newSegments.append(newSegment)

        return newSegments

    def findSingleTrace(self, segment):
        trace = []
        segmentBoard = SegmentBoard(self.width, self.height)
        segmentBoard.markTruePoints(segment)

        current = self.findMinimumPoint(segment)
        segment.remove(current)
        trace.append(current)

        nextPoint = self.nextPointInTraceByAdjacent(2, current, segmentBoard, segment, trace)
        if not nextPoint:
            # TODO: Explore the impacts of this edge case
            return []

        segment.remove(nextPoint)
        trace.append(nextPoint)
        current = nextPoint

        lookingForFirstTrace = True
        while True:
            nextPoint = self.nextPointInTraceByAdjacent(1, current, segmentBoard, segment, trace)
            if not nextPoint:
                break
            segment.remove(nextPoint)
            trace.append(nextPoint)
            current = nextPoint

        return trace

    def makeSegmentTrace(self, segment):
        if len(segment) < 4:
            return segment

        firstTrace = self.findSingleTrace(segment)
        if not len(firstTrace):
            return firstTrace
        orderedSegment = self.appendRemainingTraces(firstTrace, segment)

        return orderedSegment

    def appendRemainingTraces(self, baseTrace, remaining):
        baseTraceBoard = SegmentBoard(self.width, self.height)
        baseTraceBoard.markTruePoints(baseTrace)

        addLaterTraces = []

        while len(remaining):
            nextTrace = self.findSingleTrace(remaining)
            if len(nextTrace):
                firstPoint = nextTrace[0]
                minBetween = self.findMinimumDistance(nextTrace, baseTrace)
                minDistance = minBetween[2]
                closest = minBetween[1]
                if minDistance > 50:
                    if len(nextTrace) > 25:
                        addLaterTraces.append(nextTrace)
                else:
                    where = baseTrace.index(closest)

                    while len(nextTrace):
                        point = nextTrace.pop()
                        baseTrace.insert(where, point)

                    baseTraceBoard.markTruePoints(nextTrace)

        while len(addLaterTraces):
            trace = addLaterTraces.pop(0)
            firstPoint = trace[0]
            minBetween = self.findMinimumDistance(trace, baseTrace)
            minDistance = minBetween[2]
            closest = minBetween[1]
            if minDistance > 50:
                addLaterTraces.append(trace)
            else:
                where = baseTrace.index(closest)

                while len(nextTrace):
                    point = trace.pop()
                    baseTrace.insert(where, point)

                baseTraceBoard.markTruePoints(nextTrace)

        return baseTrace

    def findClosestPoint(self, point, board):
        x = point[0]
        y = point[1]

        adjacent = 0
        radius = 0
        while not adjacent:
            if radius > 50:
                return
            radius += 1
            adjacent = board.getTrueNeighboursInRadiusCount(x, y, radius)

        closestNeighbours = board.getTrueNeighboursInRadius(x, y, radius)
        closestNeighbours = sorted(closestNeighbours, key = lambda p: distanceBetween(point, p))

        return closestNeighbours[0]

    def showIntermediateSegments(self, segment, orderedSegment):
        intermediate = IntermediateImage([segment, orderedSegment], self.width, self.height)
        intermediate.colorAllSegments()
        intermediate.showImage()

    def nextPointInTraceByAdjacent(self, directions,
            current, segmentBoard,
            segment, orderedSegment):
        segmentBoard.markFalsePoint(current)
        x = current[0]
        y = current[1]

        adjacentCells = 0
        radius = 0
        while adjacentCells < directions:
            if radius > 20:
                print ("Radius large warning", current)
                return
            radius += 1
            adjacentCells = segmentBoard.getTrueNeighboursInRadiusCount(x, y, radius)

        neighbours = segmentBoard.getTrueNeighboursInRadius(x, y, radius)

        neighboursByAngle = sorted(neighbours, key = lambda p: angleBetween(current, p))

        return neighboursByAngle[0]

    def makePointsFromTrace(self, trace, minLineLength):
        points = []

        if len(trace) >= 2:
            prevPoint = trace.pop(0)
            currentPoint = trace.pop(0)
        else:
            return trace

        while len(trace) > 0:
            while distanceBetween(prevPoint, currentPoint) < minLineLength and len(trace):
                currentPoint = trace.pop(0)

            points.append(prevPoint)
            prevPoint = currentPoint
            if len(trace):
                currentPoint = trace.pop(0)

        return points

    def findMinimumPoint(self, segment):
        sortedY = sorted(segment, key = itemgetter(1))
        minPoint = sortedY[-1]

        minY = minPoint[1]
        amountOfMinimums = 1
        while len(sortedY) >= amountOfMinimums and sortedY[-amountOfMinimums][1] == minY:
            amountOfMinimums += 1

        if amountOfMinimums > 2:
            minimums = sortedY[-amountOfMinimums:]
            sortedX = sorted(minimums)
            minPoint = sortedX[0]

        return minPoint

    def findMinimumDistance(self, first, second):
        minDistance = sys.maxint
        minFrom = None
        minTo = None
        for i in first:
            for j in second:
                distance = distanceBetween(i, j)
                if distance < minDistance:
                    minDistance = distance
                    minFrom = i
                    minTo = j

        return (minFrom, minTo, minDistance)
