from PIL import Image


class SegmentImage():

    def __init__(self, fileName, similarity):
        self.similarity = similarity

        self.imageData = Image.open(fileName)
        self.width = self.imageData.width
        self.height = self.imageData.height

        self.image = self.imageData.load()

        self.visitedPixels = []
        for i in range(self.width):
            self.visitedPixels.append([False] * self.height)
    
        self.segments = []

    def imageAsSegments(self):
        for i in range(self.width):
            for j in range(self.height):
                if not self.visitedPixels[i][j]:
                    newSegment = self.makeSegmentOfSimilarPixels(i, j)
                    if len(newSegment) > 0:
                        self.segments.append(newSegment)
        print (str(len(self.segments)) + " segments")
    
    
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
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if ((not (i == x and j == y)) 
                        and self.pictureContains(i, j) 
                        and not self.visitedPixels[i][j]):
                    self.visitedPixels[i][j] = True
                    pixelsToCheck.append((i, j))

    def pictureContains(self, x, y):
        inHeight = y >= 0 and y < self.height
        inWidth  = x >= 0 and x < self.width
        return inWidth and inHeight

    def colorAllSegments(self):
        for segment in self.segments:
            self.colorSegment(segment)

    def colorSegment(self, segment):
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
