import os
import sys
import time
from PIL import Image

from EdgeDetector import EdgeDetector
from EdgeMatrix import EdgeMatrix
from EdgeFollower import EdgeFollower
from TraceConverter import TraceConverter
from LineConnector import LineConnector
from DotCleanup import DotCleanup

from OutputImage import OutputImage
from OutputNonConnectedLines import OutputNonConnectedLines
from IntermediateImage import IntermediateImage

TEMP_IMG_NAME = "temp_img.jpg"
GREEDY_SOLUTIONS_TO_TRY = 50

def timeFunction(function, *args):
    start = time.clock()
    returnValue = function(*args)
    end = time.clock()
    print ('--- ' + str(function.__name__) + ' --- Time: ' + str(end - start) + ' ---')
    return returnValue

def makeDotToDot(fullFilePath, intermediateSteps = False):
    # Getting proper in/out names and image dimensions.
    fileName = os.path.split(fullFilePath)[-1]
    outPathJpg = 'out/jpg/' + fileName
    outPathPdf = 'out/pdf/' + os.path.splitext(fileName)[0] + '.pdf'

    imageData = Image.open(fullFilePath)
    width = imageData.width
    height = imageData.height

    # Canny edge detection step
    edgeDetector = EdgeDetector(fullFilePath)
    edgesNumberMatrix = timeFunction(edgeDetector.getCannyEdges)

    edgeMatrix = EdgeMatrix(edgesNumberMatrix)

    if intermediateSteps:
        outCanny = IntermediateImage([edgeMatrix.points], width, height)
        outCanny.colorWhiteSegments()
        outCanny.saveImage("intermediate/canny.jpg")

    # Trace following step
    edgeFollower = EdgeFollower(edgeMatrix, width, height)
    traces = timeFunction(edgeFollower.getTraces)

    if intermediateSteps:
        outEdges = IntermediateImage(traces, width, height)
        outEdges.colorAllSegments()
        outEdges.saveImage("intermediate/edges.jpg")

    # Trace to line conversion
    traceConverter = TraceConverter(traces)
    lines = timeFunction(traceConverter.getLines)

    if intermediateSteps:
        nonConnectedLinesOut = OutputNonConnectedLines(lines, width, height)
        nonConnectedLinesOut.saveImage("intermediate/lines.jpg")

    print ('Lines to connect: ' + str(len(lines)))

    # Finding the best greedy solution
    lineConnector = LineConnector(lines)
    greedyLines = timeFunction(lineConnector.bestOfManyGreedys, GREEDY_SOLUTIONS_TO_TRY)
    greedyPoints = [point for sublist in greedyLines for point in sublist]

    if intermediateSteps:
            outGreedy = OutputImage(greedyPoints, width, height, True, False, "intermediate/notClean.pdf", "intermediate/notClean.jpg")

    # Cleaning up too close/far away dots
    print ('Dots before clean: ' + str(len(greedyPoints)))
    dotCleaner = DotCleanup(greedyPoints, width, height)
    cleanPoints = timeFunction(dotCleaner.getCleanedDots)
    dotsInImage = len(cleanPoints)

    # Output image
    print ('Dots in image: ' + str(dotsInImage))
    out = OutputImage(cleanPoints, width, height, True, False, outPathPdf)
    out.saveImage(outPathJpg)

    return cleanPoints

def makeMaxSizeDot(fullFilePath, maxDots):
    inputImageDimension = 1200
    dotsInImage = maxDots + 1

    fileName = os.path.split(fullFilePath)[-1]
    outPathJpg = 'out/jpg/' + fileName
    outPathPdf = 'out/pdf/' + os.path.splitext(fileName)[0] + '.pdf'

    # Repeat complete makeDotToDot process, decreasing image resolution, until
    # few enough dots
    while(dotsInImage > maxDots and inputImageDimension > 300):
        inputImageDimension -= 200
        print('Image Dimensions now at: ' + str(inputImageDimension))
        imageData = Image.open(fullFilePath)
        width = imageData.width
        height = imageData.height
        maxDimension = width if width > height else height
        if (maxDimension > inputImageDimension):
            scaling = float(inputImageDimension) / maxDimension
            width = int(width * scaling)
            height = int(height * scaling)
            imageData = imageData.resize((width, height), Image.BICUBIC)

        imageData.save(TEMP_IMG_NAME)

        dotPoints = makeDotToDot(TEMP_IMG_NAME)
        dotsInImage = len(dotPoints)

    out = OutputImage(dotPoints, width, height, True, False, outPathPdf, outPathJpg)
