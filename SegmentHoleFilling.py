from operator import itemgetter

from SegmentBoard import SegmentBoard

SMALL_SEGMENT_PERCENT = 0.0003

class SegmentHoleFilling():

    def __init__(self, segments, width, height):
        self.segments = segments
        self.width = width
        self.height = height
        self.size = width * height
        self.hasDoneHoleFilling = False

    def getFilledSegments(self):
        if not self.hasDoneHoleFilling:
            self.holeFillSegments()
        return self.segments

    def holeFillSegments(self):
        self.hasDoneHoleFilling = True
        for segment in self.segments:
            if len(segment) > SMALL_SEGMENT_PERCENT * self.size:
                self.fillSingleSegmentHole(segment)

    def fillSingleSegmentHole(self, segment):
        sortedX = sorted(segment)
        minX = sortedX[0][0]
        maxX = sortedX[-1][0]

        sortedY = sorted(segment, key = itemgetter(1))
        minY = sortedY[0][1]
        maxY = sortedY[-1][1]

        segmentBoard = SegmentBoard(self.width, self.height)
        segmentBoard.markTruePoints(segment)

        for i in range(minX, maxX + 1):
            for j in range(minY, maxY + 1):
                if not segmentBoard.isTrueAt(i, j):
                    numberOfNeighbours = segmentBoard.getTrueNeighboursCount(i, j)
                    if numberOfNeighbours >= 5 or segmentBoard.enclosedByTrue(i, j):
                        segment.append((i, j))
