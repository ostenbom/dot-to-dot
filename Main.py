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
from IntermediateImage import IntermediateImage
from OutputNonConnectedLines import OutputNonConnectedLines

MAX_DOTS_IN_IMAGE = 800

def makeDotToDot(fullFilePath):
    fileName = os.path.split(fullFilePath)[-1]
    outPathJpg = 'out/jpg/' + fileName
    outPathPdf = 'out/pdf/' + os.path.splitext(fileName)[0] + '.pdf'

    def timeFunction(function, *args):
        start = time.clock()
        returnValue = function(*args)
        end = time.clock()
        print ('--- ' + str(function.__name__) + ' --- Time: ' + str(end - start) + ' ---')
        return returnValue


    TEMP_IMG_NAME = "temp_in.jpg"

    inputImageDimension = 1200
    dotsInImage = 1000
    while(dotsInImage > MAX_DOTS_IN_IMAGE and inputImageDimension > 300):
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

        edgeDetector = EdgeDetector(TEMP_IMG_NAME)
        edgesNumberMatrix = timeFunction(edgeDetector.getCannyEdges)

        edgeMatrix = EdgeMatrix(edgesNumberMatrix)

        outEdges = IntermediateImage([edgeMatrix.points], width, height)
        outEdges.colorWhiteSegments()
        outEdges.saveImage("canny.jpg")

        edgeFollower = EdgeFollower(edgeMatrix, width, height)
        traces = timeFunction(edgeFollower.getTraces)

        outEdges = IntermediateImage(traces, width, height)
        outEdges.colorAllSegments()
        outEdges.saveImage("edges.jpg")

        traceConverter = TraceConverter(traces)
        lines = timeFunction(traceConverter.getLines)

        nonConnectedLinesOut = OutputNonConnectedLines(lines, width, height)
        nonConnectedLinesOut.saveImage()

        print ('Lines to connect: ' + str(len(lines)))

        lineConnector = LineConnector(lines)
        greedyLines = timeFunction(lineConnector.bestOfManyGreedys, 50)
        greedyPoints = [point for sublist in greedyLines for point in sublist]

        outGreedy = OutputImage(greedyPoints, width, height, True, False, "nonClean.pdf", "nonClean.jpg")
        
        print ('Dots before clean: ' + str(len(greedyPoints)))
        dotCleaner = DotCleanup(greedyPoints, width, height)
        cleanPoints = dotCleaner.getCleanedDots()
        dotsInImage = len(cleanPoints)
        print('Dots at the moment: ' + str(dotsInImage))


    print ('Dots in image: ' + str(len(cleanPoints)))
    out = OutputImage(cleanPoints, width, height, True, False, outPathPdf, outPathJpg)


arguments = len(sys.argv)

if arguments > 1:
    fullFilePath = sys.argv[1]
    makeDotToDot(fullFilePath)
