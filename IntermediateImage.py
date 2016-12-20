from PIL import Image

NUM_LARGE_SEGMENTS = 300

class IntermediateImage():

    def __init__(self, fileName, similarity, segments):
        self.imageData = Image.open(fileName)
        self.width = self.imageData.width
        self.height = self.imageData.height
        self.size = self.width * self.height

        self.image = self.imageData.load()

        if isinstace(segments, list):
            self.segments = segments
        else:
            self.segments = [segments]

        self.counter = 0

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

    def makeImageBlack(self):
        for i in range(self.width):
            for j in range(self.height):
                self.image[i, j] = (0, 0, 0)

    def averageList(self, l):
        average = sum(l) / len(l)
        return int(average)
