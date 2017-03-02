

class EdgeMatrix():

    def __init__(self, numberMatrix):
        self.width = len(numberMatrix[0])
        self.height = len(numberMatrix)
        self.matrix = []
        # No guarantees that points reflects the state of the matrix,
        # just a copy of initial matrix representation to avoid 2 passes
        self.points = []
        self.initialiseBoolMatrix(numberMatrix)

    def initialiseBoolMatrix(self, numberMatrix):
        # Want to access the bool matrix as x, y, not y, x
        for i in range(self.width):
            self.matrix.append([False] * self.height)

        y = 0
        for row in numberMatrix:
            x = 0
            for column in row:
                if column != 0:
                    self.matrix[x][y] = True
                    self.points.append((x, y))
                x += 1
            y += 1

    def matrixToPoints(self):
        points = []
        x = 0
        for column in self.matrix:
            y = 0
            for row in column:
                if row:
                    points.append((x, y))
                y += 1
            x += 1

        return points

    def markTruePoints(self, points):
        for point in points:
            x = point[0]
            y = point[1]
            self.markTrueAt(x, y)

    def getXYFromArgs(self, x, y = None):
        if type(x) is not int:
            y = x[1]
            x = x[0]
        return x, y

    def markTrueAt(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        self.matrix[x][y] = True

    def markFalseAt(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        self.matrix[x][y] = False

    def isTrueAt(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        return self.matrix[x][y]

    def getTrueNeighboursCount(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        return self.getTrueNeighboursInRadiusCount(1, x, y)

    def getTrueNeighboursInRadiusCount(self, radius, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        neighbours = self.getNeighboursInRadius(radius, x, y)
        trueNeighbours = 0
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if self.matrix[x][y]:
                trueNeighbours += 1

        return trueNeighbours

    def getNeighbours(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        return self.getNeighboursInRadius(1, x, y)

    def getNeighboursInRadius(self, radius, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        neighbours = []
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if ((not (i == x and j == y))
                        and self.matrixContains(i, j)):
                    neighbours.append((i, j))

        return neighbours

    def getTrueNeighbours(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        neighbours = self.getNeighbours(x, y)
        trueNeighbours = []
        for neighbour in neighbours:
            if self.matrix[neighbour[0]][neighbour[1]]:
                trueNeighbours.append(neighbour)

        return trueNeighbours

    def matrixContains(self, x, y = None):
        x, y = self.getXYFromArgs(x, y)
        inHeight = y >= 0 and y < len(self.matrix[0])
        inWidth  = x >= 0 and x < len(self.matrix)
        return inWidth and inHeight
