import copy
import math

import EdgeMatrix as EdgeMatrix

LINE_SCORE_RADIUS = 3

class CannyScorer():

    def __init__(self, edgeMatrix, cannyImage, width, height):
        self.edgeMatrix = copy.deepcopy(edgeMatrix)
        self.width = width
        self.height = height
        self.image = cannyImage

    def getCannyImage(self):
        return self.image

    def scoreLine(self, p1, p2):
        x1 = p1[0]
        x2 = p2[0]
        y1 = p1[1]
        y2 = p2[1]
        linePoints = self.getPointsInLine(x1, y1, x2, y2)

        lineScore = 0
        for point in linePoints:
            pointScore = self.edgeMatrix.getTrueNeighboursInRadiusCount(LINE_SCORE_RADIUS, point)
            lineScore += pointScore

        lineScore = float(lineScore) / len(linePoints)

        return lineScore


    def getPointsInLine(self, x1, y1, x2, y2):
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

        return points
