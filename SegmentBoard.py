

class SegmentBoard():

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = []
        for i in range(self.width):
            self.board.append([False] * self.height)

    def markTruePoints(self, points):
        for point in points:
            x = point[0]
            y = point[1]
            self.markTrueAt(x, y)

    def markTrueAt(self, x, y):
        self.board[x][y] = True

    def markFalsePoint(self, point):
        x = point[0]
        y = point[1]
        self.board[x][y] = False

    def isTrueAt(self, x, y):
        return self.board[x][y]

    def enclosedByTrue(self, x, y):
        enclosers = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        containsAll = True
        for pixel in enclosers:
            if not self.boardContains(pixel[0], pixel[1]):
                containsAll = False

        if not containsAll:
            return False

        allTrue = True
        for pixel in enclosers:
            if not self.board[pixel[0]][pixel[1]]:
                allTrue = False

        return allTrue

    def getTrueNeighboursCount(self, x, y):
        return self.getTrueNeighboursInRadiusCount(x, y, 1)

    def getTrueNeighboursInRadiusCount(self, x, y, radius):
        neighbours = self.getNeighboursInRadius(x, y, radius)
        trueNeighbours = 0
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if self.board[x][y]:
                trueNeighbours += 1

        return trueNeighbours

    def getTrueNeighboursInRadius(self, x, y, radius):
        neighbours = self.getNeighboursInRadius(x, y, radius)
        trueNeighbours = []
        for neighbour in neighbours:
             x = neighbour[0]
             y = neighbour[1]
             if self.board[x][y]:
                 trueNeighbours.append(neighbour)

        return trueNeighbours

    def getNeighbours(self, x, y):
        return self.getNeighboursInRadius(x, y, 1)

    def getNeighboursInRadius(self, x, y, radius):
        neighbours = []
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if ((not (i == x and j == y))
                        and self.boardContains(i, j)):
                    neighbours.append((i, j))

        return neighbours

    def boardContains(self, x, y):
        inHeight = y >= 0 and y < len(self.board[0])
        inWidth  = x >= 0 and x < len(self.board)
        return inWidth and inHeight
