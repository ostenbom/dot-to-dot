import sys
import time

from Dots import SegmentImage

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
    


image = SegmentImage(fileName, similarity)

start = time.clock()
image.imageAsSegments()
end = time.clock()
print ("---- Segmentation time : " + str(end - start) + " ----")

start = time.clock()
image.holeFillSegments()
end = time.clock()
print ("---- Hole fill time : " + str(end - start) + " ----")

start = time.clock()
#segmentCorners = image.findAllSegmentCorners()
end = time.clock()
print ("---- Corner find time : " + str(end - start) + " ----")

#image.colorAllSegments()
image.colorLargestSegments()
#image.plotAllSegmentCorners(segmentCorners)
image.imageData.save("out.jpg")
