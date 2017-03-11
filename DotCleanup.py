import math

from DistanceUtils import distanceBetween

LONGEST_LINE_DIVISION = 5
SMALLEST_LINE_DIVISION = 100

class DotCleanup():
    def __init__(self, dots, width, height):
        self.dots = dots

        maxDimension = width if width > height else height
        self.maxLineLength = int(float(maxDimension) / LONGEST_LINE_DIVISION)
        self.minLineLength = int(float(maxDimension) / SMALLEST_LINE_DIVISION)

    def getCleanedDots(self):
        dots = self.dots[:]
        prev = dots.pop(0)
        cleanedDots = []

        while len(dots):
            curr = dots.pop(0)
            distance = distanceBetween(prev, curr)
            if distance > self.maxLineLength:
                line = self.divideLine(prev, curr)
                cleanedDots = cleanedDots + line
            elif distance < self.minLineLength:
                pass
            else:
                cleanedDots.append(prev)
            prev = curr

        cleanedDots.append(curr)

        return cleanedDots

    def divideLine(self, start, end):
        line = [start]
        length = distanceBetween(start, end)
        divisions = 1
        while length / divisions > self.maxLineLength:
            divisions += 1

        pointsToIntroduce = divisions - 1
        pointsOnLine = self.getPointsInLine(start, end)
        pointOnLineStep = len(pointsOnLine) / divisions
        for i in range(1, pointsToIntroduce + 1):
            line.append(pointsOnLine[pointOnLineStep * i])

        return line

    def getPointsInLine(self, start, end):
        x1, y1, x2, y2 = start[0], start[1], end[0], end[1]
        deltaX = abs(x1 - x2)
        deltaY = abs(y1 - y2)

        if deltaX == 0:
            yFrom = y1 if y1 < y2 else y2
            yTo = y1 if yFrom == y2 else y2
            return [(x1, y) for y in range(yFrom, yTo + 1)]

        xFrom = x1 if x1 < x2 else x2
        yFrom = y1 if xFrom == x1 else y2
        otherY = y1 if yFrom == y2 else y2
        yMultiple = 1 if otherY > yFrom else -1

        theta = math.atan(float(deltaY) / float(deltaX))

        points = []
        for i in range(deltaX + 1):
            x = xFrom + i
            yHeight = math.tan(theta) * i
            y = yFrom + (yMultiple * yHeight)
            points.append((x, int(round(y))))

        if points[0] != start:
            points.reverse()
        return points
