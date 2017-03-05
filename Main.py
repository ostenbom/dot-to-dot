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

edgeDetector = EdgeDetector(fileName)
edgesNumberMatrix = timeFunction(edgeDetector.getCannyImage)

edgeMatrix = EdgeMatrix(edgesNumberMatrix)

edgeFollower = EdgeFollower(edgeMatrix, width, height)
traces = timeFunction(edgeFollower.getTraces)

traceConverter = TraceConverter(traces)
lines = timeFunction(traceConverter.getLines)

print ('Lines to connect: ' + str(len(lines)))

lineConnecter = LineConnecter(lines)
sortedLines = timeFunction(lineConnecter.getConnectedLines)

pointsInOrder = [point for sublist in sortedLines for point in sublist]
print ('Dots in image: ' + str(len(pointsInOrder)))
out = OutputImage(pointsInOrder, (width, height), True)
out.showImage()
