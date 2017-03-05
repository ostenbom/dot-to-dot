import sys
import time
import copy
import itertools
from PIL import Image
import numpy as np

import cv2

# from SegmentImage import SegmentImage
# from SegmentHoleFilling import SegmentHoleFilling
# from SegmentCenterRemoval import SegmentCenterRemoval
# from TraceFollower import TraceFollower
# from TraceConnecter import TraceConnecter
# from IntermediateImage import IntermediateImage

from EdgeDetector import EdgeDetector
from EdgeMatrix import EdgeMatrix
from EdgeFollower import EdgeFollower
from TraceConverter import TraceConverter
from LineConnecter import LineConnecter

from OutputImage import OutputImage
from OutputNonConnectedLines import OutputNonConnectedLines
from IntermediateImage import IntermediateImage

arguments = len(sys.argv)

if arguments > 1:
    fileName = sys.argv[1]
else:
    fileName = "testimages/simple.jpg"


def timeFunction(function, *args):
    start = time.clock()
    returnValue = function(*args)
    end = time.clock()
    print ('--- ' + str(function.__name__) + ' --- Time: ' + str(end - start) + ' ---')
    return returnValue

imageData = Image.open(fileName)
width = imageData.width
height = imageData.height

# Canny Method:
edgeDetector = EdgeDetector(fileName)
edgesNumberMatrix = timeFunction(edgeDetector.getCannyImage)

edgeMatrix = EdgeMatrix(edgesNumberMatrix)

edgeFollower = EdgeFollower(edgeMatrix, width, height)
traces = timeFunction(edgeFollower.getTraces)

intermediate = IntermediateImage(traces, width, height)
intermediate.colorAllSegments()
intermediate.showImage()

traceConverter = TraceConverter(traces)
lines = timeFunction(traceConverter.getLines)

intermediate = IntermediateImage(lines, width, height)
intermediate.colorAllSegments()
intermediate.showImage()

print ('Lines to connect', len(lines))

lineConnecter = LineConnecter(lines)
sortedLines = timeFunction(lineConnecter.getConnectedLines)

out = OutputNonConnectedLines(lines, (width, height))
out.showImage()
out.saveImage()

pointsInOrder = [point for sublist in sortedLines for point in sublist]
out = OutputImage(pointsInOrder, (width, height), True)
out.showImage()

# Segment Method:
'''
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

intermediate = IntermediateImage(filledSegments, width, height)
intermediate.colorLargestSegments()
intermediate.showImage()
intermediate.saveImage("segments.jpg")

centerRemover = SegmentCenterRemoval(filledSegments, width, height)

start = time.clock()
outlines = centerRemover.getSegmentOutlines()
end = time.clock()
print ("---- Center removal time : " + str(end - start) + " ----")

intermediate = IntermediateImage(outlines, width, height)
intermediate.colorLargestSegments()
intermediate.showImage()

traceFollower = TraceFollower(outlines, width, height)

start = time.clock()
dottedSegments = traceFollower.getDottedSegments()
end = time.clock()
print ("---- Defining points time : " + str(end - start) + " ----")

connecter = TraceConnecter(dottedSegments, width, height)
points = connecter.getConnectedTraces()

print ("---- Points in image: " + str(len(points)) + " ----")
out = OutputImage(points, (width, height), True)
out.showImage()
out.saveImage()


#cornerImage = copy.copy(image)
#cornerImage.plotAllSegmentCorners(segmentCorners)
#cornerImage.imageData.save("out_corners.jpg")
'''
