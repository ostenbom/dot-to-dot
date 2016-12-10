import math

from PIL import Image
from operator import itemgetter

SMALL_SEGMENT_PERCENT = 0.0003
CONTIGUOUS_FACTOR = 12
NUM_LARGE_SEGMENTS = 300

class SegmentImage():

    def __init__(self, fileName, similarity):
        self.similarity = similarity

        self.imageData = Image.open(fileName)
        self.width = self.imageData.width
        self.height = self.imageData.height
        self.size = self.width * self.height

        self.image = self.imageData.load()

        self.visitedPixels = []
        for i in range(self.width):
            self.visitedPixels.append([False] * self.height)
    
        self.segments = []
        self.counter = 0

    def imageAsSegments(self):
        for i in range(self.width):
            for j in range(self.height):
                if not self.visitedPixels[i][j]:
                    newSegment = self.makeSegmentOfSimilarPixels(i, j)
                    if len(newSegment) > 0:
                        self.segments.append(newSegment)
        self.printDiagnostics()
    
    def printDiagnostics(self):
        print ("Image width: " + str(self.width))
        print ("Image height: " + str(self.height))
        print ("Number of pixels: " + str(self.width * self.height))
        print (str(len(self.segments)) + " segments")

        segmentLengths = []
        for segment in self.segments:
            segmentLengths.append(len(segment))

        averageSegmentSize = self.averageList(segmentLengths)

        print ("Average segment size " + str(averageSegmentSize))
    
    def makeSegmentOfSimilarPixels(self, x, y):
        segment = []
        pixelsToCheck = []
        pixel = self.image[x, y]
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        self.addPixelsAroundToQueue(x, y, pixelsToCheck)
    
        while len(pixelsToCheck):
            otherPixelCoordinates = pixelsToCheck.pop()
            otherX = otherPixelCoordinates[0]
            otherY = otherPixelCoordinates[1]
            otherPixel = self.image[otherX, otherY]
            
            otherR = otherPixel[0]
            otherG = otherPixel[1]
            otherB = otherPixel[2]

            if (abs(r - otherR) < self.similarity
                    and abs(g - otherG) < self.similarity
                    and abs(b - otherB) < self.similarity):
                self.addPixelsAroundToQueue(otherX, otherY, pixelsToCheck)
                segment.append((otherX, otherY))

        return segment
    
    def addPixelsAroundToQueue(self, x, y, pixelsToCheck):
        neighbours = self.getNeighbours(x, y, self.visitedPixels)
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if not self.visitedPixels[x][y]:
                self.visitedPixels[x][y] = True
                pixelsToCheck.append((x, y))

    def holeFillSegments(self):
        for segment in self.segments:
            if len(segment) > SMALL_SEGMENT_PERCENT * self.size:
                self.fillInSegmentHole(segment)

    def fillInSegmentHole(self, segment):
        sortedX = sorted(segment)
        minX = sortedX[0][0]
        maxX = sortedX[-1][0]

        sortedY = sorted(segment, key = itemgetter(1))
        minY = sortedY[0][1]
        maxY = sortedY[-1][1]

        segmentBoard = []
        for i in range(self.width):
            segmentBoard.append([False] * self.height)

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            segmentBoard[x][y] = True

        for i in range(minX, maxX + 1):
            for j in range(minY, maxY + 1):
                if not segmentBoard[i][j]:
                    numberOfNeighbours = self.getTrueNeighboursCount(i, j, segmentBoard)
                    if numberOfNeighbours >= 5 or self.enclosedByTrue(i, j, segmentBoard):
                        segment.append((i, j))


    def removeSegmentCenters(self):
        for segment in self.segments:
            segmentLength = len(segment)
            self.removeCenter(segment)
            lengthAfterRemove = len(segment)

    def removeCenter(self, segment):
        segmentBoard = []
        for i in range(self.width):
            segmentBoard.append([False] * self.height)

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            segmentBoard[x][y] = True
        
        pixelsToRemove = []
        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            numberOfNeighbours = self.getTrueNeighboursCount(x, y, segmentBoard)
            if numberOfNeighbours > 5:
                pixelsToRemove.append(pixel)

        for pixel in pixelsToRemove:
            segment.remove(pixel)

        return segment
        
    def getTrueNeighboursCount(self, x, y, board):
        return self.getTrueNeighboursInRadiusCount(x, y, 1, board)

    def getTrueNeighboursInRadiusCount(self, x, y, radius, board):
        neighbours = self.getNeighboursInRadius(x, y, radius, board)
        trueNeighbours = 0
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if board[x][y]:
                trueNeighbours += 1

        return trueNeighbours

    def getTrueNeighboursInRadius(self, x, y, radius, board):
        neighbours = self.getNeighboursInRadius(x, y, radius, board)
        trueNeighbours = []
        for neighbour in neighbours:
             x = neighbour[0]
             y = neighbour[1]
             if board[x][y]:
                 trueNeighbours.append(neighbour)

        return trueNeighbours

    def getNeighbours(self, x, y, board):
        return self.getNeighboursInRadius(x, y, 1, board)

    def getNeighboursInRadius(self, x, y, radius, board):
        neighbours = []
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if ((not (i == x and j == y))
                        and self.boardContains(i, j, board)):
                    neighbours.append((i, j))

        return neighbours

    def enclosedByTrue(self, x, y, board):
        enclosers = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        containsAll = True
        for pixel in enclosers:
            if not self.boardContains(pixel[0], pixel[1], board):
                containsAll = False

        if not containsAll:
            return False

        allTrue = True 
        for pixel in enclosers:
            if not board[pixel[0]][pixel[1]]:
                allTrue = False

        return allTrue

    def findDefiningPoints(self):
        for segment in self.segments:
            self.removePointsAtSimilarAngle(segment)

    def removePointsAtSimilarAngle(self, segment):
        orderedSegment = []
        current = self.findMinimumPoint(segment)
        segment.remove(current)
        orderedSegment.append(current)

        segmentBoard = []
        for i in range(self.width):
            segmentBoard.append([False] * self.height)

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            segmentBoard[x][y] = True

        while len(segment) > 2:
            x = current[0]
            y = current[1]
            segmentBoard[x][y] = False

            adjacentCells = 0
            radius = 1
            while adjacentCells < 2:
                adjacentCells = self.getTrueNeighboursInRadiusCount(x, y, radius, segmentBoard)
                radius += 1

            neighbours = self.getTrueNeighboursInRadius(x, y, radius, segmentBoard)

            neighboursByAngle = sorted(neighbours, key = lambda p: self.angleBetween(current, p))
            nextPoint = neighboursByAngle[0]
            segment.remove(nextPoint)
            orderedSegment.append(nextPoint)
            current = nextPoint

        import pdb; pdb.set_trace()

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
            angle = 360 - 90 - 180 - angle
        elif x1 > x2 and y1 < y2:
            angle = 180 - angle

        return angle
    
    def findMinimumPoint(self, segment):
        sortedY = sorted(segment, key = itemgetter(1))
        minPoint = sortedY[-1]

        minY = minPoint[1]
        amountOfMinimums = 1
        while(sortedY[-amountOfMinimums][1] == minY):
            amountOfMinimums += 1

        if amountOfMinimums > 2:
            minimums = sortedY[-amountOfMinimums:]
            sortedX = sorted(minimums)
            minPoint = sortedX[0]

        return minPoint

            
    def findAllSegmentCorners(self):
        allSegmentCorners = []
        for segment in self.segments:
           segmentCorners = self.findSegmentCorners(segment)
           allSegmentCorners.append(segmentCorners)

        total = 0
        for segment in allSegmentCorners:
            total += len(segment)

        print ( "Number of corners: " + str(total))

        return allSegmentCorners

    def findSegmentCorners(self, segment):
        corners = []

        segmentBoard = []
        for i in range(self.width):
            segmentBoard.append([False] * self.height)

        for pixel in segment:
            segmentBoard[pixel[0]][pixel[1]] = True

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            contiguousPixels = self.getNumberOfContiguousPixles(x, y, segmentBoard)
            if contiguousPixels < 16 - CONTIGUOUS_FACTOR: 
                corners.append((x, y))

        return corners

    def getNumberOfContiguousPixles(self, x, y, board):
        circle = [
            (x + 4, y - 1),
            (x + 4, y),
            (x + 4, y + 1),
            (x - 4, y - 1),
            (x - 4, y),
            (x - 4, y + 1),
            (x - 1, y + 4),
            (x,     y + 4),
            (x + 1, y + 4),
            (x - 1, y - 4),
            (x,     y - 4),
            (x + 1, y - 4),
            (x + 3, y + 3),
            (x + 3, y - 3),
            (x - 3, y + 3),
            (x - 3, y - 3)
        ]

        containsAll = True
        for pixel in circle:
            if not self.boardContains(pixel[0], pixel[1], board):
                containsAll = False

        if not containsAll:
            # Eight for straight
            return 8

        numberContiguous = 0
        for pixel in circle:
            x = pixel[0]
            y = pixel[1]
            
            if board[x][y]:
                numberContiguous += 1
        
        return numberContiguous

    def boardContains(self, x, y, board):
        inHeight = y >= 0 and y < len(board[0])
        inWidth  = x >= 0 and x < len(board)
        return inWidth and inHeight


    def pictureContains(self, x, y):
        return self.boardContains(x, y, self.visitedPixels)

    def colorAllSegments(self):
        self.makeImageBlack()
        for segment in self.segments:
            color = self.pickDifferentColor()
            self.colorSegment(segment, color)

    def colorLargestSegments(self):
        self.makeImageBlack()
        self.segments.sort(key = lambda l : len(l))
        for segment in self.segments[-NUM_LARGE_SEGMENTS:]:
            color = self.pickDifferentColor()
            self.colorSegment(segment, color)

    def pickDifferentColor(self):
        self.counter = (self.counter + 1) % 7
        return {
            0: (255, 0, 0),
            1: (255, 255, 0),
            2: (0, 255, 0),
            3: (0, 255, 255),
            4: (0, 0, 255),
            5: (255, 0, 255),
            6: (255, 255, 255)
        }[self.counter]

    def colorSegment(self, segment, color = None):
        if color:
            pass
        elif len(segment) < SMALL_SEGMENT_PERCENT * self.size:
            color = (0, 0, 0)
        else: 
            color = self.segmentAverageColor(segment)

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]

            self.image[x, y] = color

    def segmentAverageColor(self, segment):
        rs = []
        gs = []
        bs = []
        for pixel in segment:
            x = pixel[0]
            y = pixel[1]

            color = self.image[x, y]
            
            rs.append(color[0])
            gs.append(color[1])
            bs.append(color[2])

        r = self.averageList(rs)
        g = self.averageList(gs)
        b = self.averageList(bs)

        return (r, g, b)

    def plotAllSegmentCorners(self, segmentCorners):
        self.makeImageBlack()
        for segment in segmentCorners:
            for point in segment:
                self.image[point[0], point[1]] = (255, 255, 255)

    def makeImageBlack(self):
        for i in range(self.width):
            for j in range(self.height):
                self.image[i, j] = (0, 0, 0)

    def averageList(self, l):
        average = sum(l) / len(l)
        return int(average)
