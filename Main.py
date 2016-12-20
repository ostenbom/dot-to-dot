import sys
import time
import copy
import itertools
from PIL import Image

from SegmentImage import SegmentImage
from SegmentHoleFilling import SegmentHoleFilling
from SegmentCenterRemoval import SegmentCenterRemoval
from TraceFollower import TraceFollower
from OutputImage import OutputImage

arguments = len(sys.argv)

if arguments > 1:
    if arguments == 2:
        fileName = "simple.jpg"
    else:
        fileName = sys.argv[2]

    similarity = int(sys.argv[1])
else:
    fileName = "simple.jpg"
    similarity = 40

imageData = Image.open(fileName)
width = imageData.width
height = imageData.height

segmentImage = SegmentImage(fileName, similarity)

start = time.clock()
segments = segmentImage.getSegments()
end = time.clock()
print ("---- Segmentation time : " + str(end - start) + " ----")

holeFilling = SegmentHoleFilling(segments, width, height)
start = time.clock()
filledSegments = holeFilling.getFilledSegments()
end = time.clock()
print ("---- Hole fill time : " + str(end - start) + " ----")

centerRemover = SegmentCenterRemoval(filledSegments, width, height)

start = time.clock()
outlines = centerRemover.getSegmentOutlines()
end = time.clock()
print ("---- Center removal time : " + str(end - start) + " ----")

minLineLength = 10
traceFollower = TraceFollower(outlines, width, height, minLineLength)

start = time.clock()
dottedSegments = traceFollower.getDottedSegments()
end = time.clock()
print ("---- Defining points time : " + str(end - start) + " ----")

points = []

dottedSegments.sort(key = lambda l : len(l))
for segment in dottedSegments[-50:]:
    for point in segment:
        points.append(point)

print ("---- Points in image: " + str(len(points)) + " ----")
out = OutputImage(points, (width, height), True)
out.saveImage()


#cornerImage = copy.copy(image)
#cornerImage.plotAllSegmentCorners(segmentCorners)
#cornerImage.imageData.save("out_corners.jpg")
