import copy

class Segment():

    def __init__(self, points):
        self.points = points
        self.hasCalculatedCenter = False
        self.visitedPoints = copy.copy(self.points)

    def isEmpty(self):
        return len(self.points) == 0

    def getAtIndex(self, index):
        return self.points[index]

    def visitPoints(self, points):
        for point in points:
            self.visitPoint(point)

    def visitPoint(self, point):
        self.visitPoints.remove(point)

    def getLength(self):
        return len(self.points)

    def getCenter(self):
        if not self.hasCalculatedCenter:
            self.center = self.calculateCenter()
        return self.center

    def calculateCenter(self):
        xs = []
        ys = []
        for point in self.points:
            x = point[0]
            y = point[1]

            xs.append(x)
            ys.append(y)

        xAverage = sum(xs) / len(xs)
        yAverage = sum(ys) / len(ys)

        return (xAverage, yAverage)
