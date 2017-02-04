from EdgeMatrix import EdgeMatrix

class PathCreator():

    def __init__(self, numberMatrix):
        self.matrix = EdgeMatrix(numberMatrix)
        self.points = self.matrix.matrixToPoints()
        self.paths = []
        self.hasMadePaths = False

    def getPaths(self):
        if not self.hasMadePaths:
            self.paths = makePaths()
            self.hasMadePaths = True
        return self.paths

    def makePaths(self):
        while len(self.points):
            path = []
            point = self.points.pop()
            path.append(point)
            nextPoint = self.getInitialNextPoint(point)
            while nextPoint != point:
                path.append(nextPoint)
                self.matrix.markFalseAt(point)
                self.points.remove(nextPoint)
                point = nextPoint
                nextPoint = self.getNextPoint(point, path)

    def getInitialNextPoint(self, point):
        numNeighbours = self.matrix.getTrueNeighboursCount(point)
        if numNeighbours == 0:
            # Stray pixel.
            return point
        else:
            return self.matrix.getNeighbours(point)[0]

    def getNextPoint(self, point, path):
        numNeighbours = self.matrix.getTrueNeighboursCount(point)
        if numNeighbours == 0:
            # Reached end of line
            return point
        elif numNeighbours == 1:
            # Only one direction to go in
            return self.matrix.getNeighbours(point)[0]
        else:
            # Crossroad case
            behindDirection = self.getBehindDirection(point, path)
            bestAngle = 180
            nextPoint = None
            for potentialNext in self.matrix.getNeighbours(point):
                aheadDirection self.getAheadDirection(potentialNext)
                if self.angleBetween(aheadDirection, behindDirection) < bestAngle:
                    nextPoint = potentialNext
            return nextPoint
