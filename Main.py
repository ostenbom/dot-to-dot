import sys
import time
from PIL import Image

from EdgeDetector import EdgeDetector
from EdgeMatrix import EdgeMatrix
from EdgeFollower import EdgeFollower
from TraceConverter import TraceConverter
from LineConnecter import LineConnecter
from CannyScorer import CannyScorer

from OutputImage import OutputImage
from OutputNonConnectedLines import OutputNonConnectedLines
from IntermediateImage import IntermediateImage
from SolutionSelectionImage import SolutionSelectionImage
from LineDetailViewing import LineDetailViewing
from ConnectionImage import ConnectionImage

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
edgesNumberMatrix = timeFunction(edgeDetector.getCannyEdges)

edgeMatrix = EdgeMatrix(edgesNumberMatrix)

lineScoring = CannyScorer(edgeMatrix, edgeDetector.getCannyImage(), width, height)

edgeFollower = EdgeFollower(edgeMatrix, width, height)
traces = timeFunction(edgeFollower.getTraces)

outEdges = IntermediateImage(traces, width, height)
outEdges.colorAllSegments()
outEdges.saveImage("edges.jpg")
outEdges.showImage()

traceConverter = TraceConverter(traces)
lines = timeFunction(traceConverter.getLines)

# outLines = OutputNonConnectedLines(lines, width, height)
# outLines.saveImage()
# outLines.showImage()

print ('Lines to connect: ' + str(len(lines)))

lineConnecter = LineConnecter(lines)
# sortedLines = timeFunction(lineConnecter.getConnectedLines, 5)
# potentialSolutions = timeFunction(lineConnecter.tryConnecting, 6)

oneSolution = timeFunction(lineConnecter.getConnectedLines, 1)

connectionImage = ConnectionImage(oneSolution, lineScoring, width, height)
connectionImage.drawInbetweenLines()
connectionImage.showImage()

# solutonSelection = SolutionSelectionImage(potentialSolutions, width, height)
# timeFunction(solutonSelection.createSolutionSelectionImage)
# solutonSelection.showImage()
# solutonSelection.saveImage()
#
# print ("Pick and image between 1 - 6")
# imagePick = int(input("Image Number: ")) - 1
# sortedLines = potentialSolutions[imagePick]
#
# pointsInOrder = [point for sublist in sortedLines for point in sublist]
# print ('Dots in image: ' + str(len(pointsInOrder)))
# out = OutputImage(pointsInOrder, width, height, True, True)
# out.saveImage()
