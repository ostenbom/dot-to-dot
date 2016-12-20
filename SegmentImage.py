from PIL import Image

from SegmentBoard import SegmentBoard


class SegmentImage():

    def __init__(self, fileName, similarity):
        self.similarity = similarity

        self.imageData = Image.open(fileName)
        self.width = self.imageData.width
        self.height = self.imageData.height
        self.size = self.width * self.height

        self.image = self.imageData.load()

        self.visitedPixels = SegmentBoard(self.width, self.height)

        self.segments = []
        self.counter = 0

    def getSegments(self):
        if len(self.segments):
            return self.segments
        else:
            self.imageAsSegments()
            return self.segments

    def imageAsSegments(self):
        for i in range(self.width):
            for j in range(self.height):
                if not self.visitedPixels.isTrueAt(i, j):
                    newSegment = self.makeSegmentOfSimilarPixels(i, j)
                    if len(newSegment) > 0:
                        self.segments.append(newSegment)
        self.printDiagnostics()

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
        neighbours = self.visitedPixels.getNeighbours(x, y)
        for neighbour in neighbours:
            x = neighbour[0]
            y = neighbour[1]
            if not self.visitedPixels.isTrueAt(x, y):
                self.visitedPixels.markTrueAt(x, y)
                pixelsToCheck.append((x, y))

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

    def averageList(self, l):
        average = sum(l) / len(l)
        return int(average)
