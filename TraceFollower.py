import math
from operator import itemgetter

from SegmentBoard import SegmentBoard

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

    def makeSegmentTrace(self, segment):
        if len(segment) < 4:
            return segment

        orderedSegment = []
        segmentBoard = SegmentBoard(self.width, self.height)

        current = self.findMinimumPoint(segment)
        segment.remove(current)
        orderedSegment.append(current)

        nextPointsByAngle = self.nextPointInTraceByAdjacent(2, current, segmentBoard, segment, orderedSegment)
        if not nextPointsByAngle:
            return []

        nextPoint = nextPointsByAngle[0]
        segment.remove(nextPoint)
        orderedSegment.append(nextPoint)
        current = nextPoint

        radiusTooLarge = False
        while len(segment) > 2:
            nextPointsByAngle = self.nextPointInTraceByAdjacent(1, current, segmentBoard, segment, orderedSegment)
            if not nextPointsByAngle:
                radiusTooLarge = True
                break
            nextPoint = nextPointsByAngle[0]
            segment.remove(nextPoint)
            orderedSegment.append(nextPoint)
            current = nextPoint

        if radiusTooLarge:
            self.segments.append(segment)

        return orderedSegment

    def nextPointInTraceByAdjacent(self, directions,
            current, segmentBoard,
            segment = None, orderedSegment = None):
        segmentBoard.markFalsePoint(current)
        x = current[0]
        y = current[1]

        adjacentCells = 0
        radius = 0
        while adjacentCells < directions:
            if radius > 50:
                return
            radius += 1
            adjacentCells = segmentBoard.getTrueNeighboursInRadiusCount(x, y, radius)

        neighbours = segmentBoard.getTrueNeighboursInRadius(x, y, radius)

        neighboursByAngle = sorted(neighbours, key = lambda p: self.angleBetween(current, p))

        return neighboursByAngle

    def makePointsFromTrace(self, trace, minLineLength):
        points = []

        if len(trace) >= 2:
            prevPoint = trace.pop(0)
            currentPoint = trace.pop(0)
        else:
            return trace

        while len(trace) > 0:
            while self.distanceBetween(prevPoint, currentPoint) < minLineLength and len(trace):
                currentPoint = trace.pop(0)

            points.append(prevPoint)
            prevPoint = currentPoint
            if len(trace):
                currentPoint = trace.pop(0)

        return points

    def distanceBetween(self, first, second):
        x1 = first[0]
        x2 = second[0]

        y1 = first[1]
        y2 = second[1]

        deltaX = abs(x1 - x2)
        deltaY = abs(y1 - y2)

        distance = math.sqrt(float(deltaX * deltaX) + float(deltaY * deltaY))

        return distance

    def lineAngle(self, p1, p2, p3):
        a = self.distanceBetween(p1, p2)
        b = self.distanceBetween(p2, p3)
        c = self.distanceBetween(p1, p3)
        if a == 0 or b == 0:
            return 90
        angle = math.degrees(math.acos(float(c * c - a * a - b * b) / float(-2 * a * b)))
        return angle

    def angleBetween(self, p1, p2):
        x1 = p1[0]
        x2 = p2[0]

        y1 = p1[1]
        y2 = p2[1]

        deltaX = abs(x1 - x2)
        deltaY = abs(y1 - y2)

        if deltaX == 0:
            return 90

        angle = math.degrees(math.atan(float(deltaY) / float(deltaX)))
        if x1 < x2 and y1 > y2:
            pass
        elif x1 > x2 and y1 > y2:
            angle = 180 - angle
        elif x1 < x2 and y1 < y2:
            angle = 360 - angle
        elif x1 > x2 and y1 < y2:
            angle = 180 + angle

        return angle

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
