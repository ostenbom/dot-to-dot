from SegmentBoard import SegmentBoard

EDGE_SURROUNDING_LIMIT = 5

class SegmentCenterRemoval():

    def __init__(self, segments, width, height):
        self.segments = segments
        self.width = width
        self.height = height
        self.hasRemovedCenters = False

    def getSegmentOutlines(self):
        if not self.hasRemovedCenters:
            self.removeSegmentCenters()
        return self.segments

    def removeSegmentCenters(self):
        self.hasRemovedCenters = True
        for segment in self.segments:
            self.removeCenter(segment)

    def removeCenter(self, segment):
        segmentBoard = SegmentBoard(self.width, self.height)
        segmentBoard.markTruePoints(segment)

        pixelsToRemove = []
        for pixel in segment:
            x = pixel[0]
            y = pixel[1]
            numberOfNeighbours = segmentBoard.getTrueNeighboursCount(x, y)
            if numberOfNeighbours > EDGE_SURROUNDING_LIMIT:
                pixelsToRemove.append(pixel)

        for pixel in pixelsToRemove:
            segment.remove(pixel)

        return segment
