from DistanceUtils import distanceBetween, angleBetween

MAX_SEGMENTS = 50

class TraceConnecter():

    def __init__(self, segments, width, height):
        self.segments = segments
        self.width = width
        self.height = height

        self.points = []
        self.hasConnectedPoints = False

    def getConnectedTraces(self):
        if not self.hasConnectedPoints:
            self.connectTraces()
        return self.points

    def connectTraces(self):
        distanceBetweenSegments = []
        lastPointPositions = []
        self.segments.sort(key = lambda l : len(l))
        largestSegments = self.segments[-MAX_SEGMENTS:]
        for segment in largestSegments:
            if len(lastPointPositions):
                lastPoint = lastPointPositions[-1]
                firstPoint = segment[0]
                distance = distanceBetween(lastPoint, firstPoint)
                distanceBetweenSegments.append(distance)

            if len(segment):
                endPoint = segment[-1]
                lastPointPositions.append(endPoint)

            for point in segment:
                self.points.append(point)

        distanceBetweenSegments.sort()
        print ('Longest distances between segments: ', distanceBetweenSegments[-5:])
