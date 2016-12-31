from SegmentBoard import SegmentBoard

SMALL_SEGMENT_THRESHHOLD = 0.01

class SmallSegmentMerger():

    def __init__(self, segments, width, height):
        self.segments = segments
        self.width = width
        self.height = height

        self.size = width * height

        self.hasMergedSmall = False

    def getMergedSegments(self):
        if not self.hasMergedSmall:
            self.mergeSmallSegments()

        return self.segments

    def mergeSmallSegments(self):
        self.segments.sort(key = lambda l : len(l))
        
        for segment in segments:
            if len(segment) < SMALL_SEGMENT_THRESHHOLD * self.size
                self.mergeWithSurrounding(segment)

    def mergeWithSurrounding(self, segment):
        pass

