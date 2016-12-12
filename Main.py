import sys
import time
import copy
import itertools

from Dots import SegmentImage
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
    


image = SegmentImage(fileName, similarity)

start = time.clock()
image.imageAsSegments()
end = time.clock()
print ("---- Segmentation time : " + str(end - start) + " ----")

start = time.clock()
image.holeFillSegments()
end = time.clock()
print ("---- Hole fill time : " + str(end - start) + " ----")

colorImage = copy.copy(image)
colorImage.colorLargestSegments()
colorImage.imageData.save("out_color_segments.jpg")

start = time.clock()
image.removeSegmentCenters()
end = time.clock()
print ("---- Center removal time : " + str(end - start) + " ----")

start = time.clock()
image.findDefiningPoints(60)
end = time.clock()
print ("---- Defining points time : " + str(end - start) + " ----")

start = time.clock()
#segmentCorners = image.findAllSegmentCorners()
end = time.clock()
print ("---- Corner find time : " + str(end - start) + " ----")

points = []

image.segments.sort(key = lambda l : len(l))
for segment in image.segments[-50:]:
    for point in segment:
        points.append(point)

print ("---- Points in image: " + str(len(points)) + " ----")
out = OutputImage(points, (image.width, image.height), True)
out.saveImage()


#cornerImage = copy.copy(image)
#cornerImage.plotAllSegmentCorners(segmentCorners)
#cornerImage.imageData.save("out_corners.jpg")
