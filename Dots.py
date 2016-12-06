from PIL import Image
from operator import itemgetter

SMALL_SEGMENT_PERCENT = 0.0003


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
        #sortedX = sorted(segment)
        #minX = sortedX[0][0]
        #maxX = sortedX[-1][0]

        #sortedY = sorted(segment, key = itemgetter(1))
        #minY = sortedY[0][1]
        #maxY = sortedY[-1][1]

        segmentBoard = []
        for i in range(self.width):
            segmentBoard.append([False] * self.height)

        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            segmentBoard[x][y] = True

        for i in range(self.width):
            for j in range(self.height):
                if not segmentBoard[i][j]:
                    numberOfNeighbours = self.getTrueNeighboursCount(i, j, segmentBoard)
                    if numberOfNeighbours >= 5 or self.enclosedByTrue(i, j, segmentBoard):
                        print("filling (" + str(i) + ", " + str(j) + ")")
                        segment.append((i, j))


    def getTrueNeighboursCount(self, x, y, board):
        neighbours = self.getNeighbours(x, y, board)
        trueNeighbours = 0
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if board[x][y]:
                trueNeighbours += 1

        return trueNeighbours

    def getNeighbours(self, x, y, board):
        neighbours = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
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
            

    def boardContains(self, x, y, board):
        inHeight = y >= 0 and y < len(board[0])
        inWidth  = x >= 0 and x < len(board)
        return inWidth and inHeight


    def pictureContains(self, x, y):
        return self.boardContains(x, y, self.visitedPixels)

    def colorAllSegments(self):
        for segment in self.segments:
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

    def averageList(self, l):
        average = sum(l) / len(l)
        return int(average)
