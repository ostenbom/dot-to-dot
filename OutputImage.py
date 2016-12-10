from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter

BASE_IMAGE_WIDTH = 5000

class OutputImage():

    def __init__(self, points, originalDimensions):
        self.points = points
        originalWidth = originalDimensions[0]
        originalHeight = originalDimensions[1]

        imageRatio = float(originalHeight) / float(originalWidth)

        imageHeight = BASE_IMAGE_WIDTH * imageRatio

        xScaling = float(BASE_IMAGE_WIDTH) / float(originalWidth)
        yScaling = float(imageHeight) / float(originalHeight)
        
        print ("Dimensions: (" + str(BASE_IMAGE_WIDTH) + ", " + str(imageHeight) + ")") 

        self.image = Image.new("RGB", (BASE_IMAGE_WIDTH, int(imageHeight)), color=(255, 255, 255))

        draw = ImageDraw.Draw(self.image)

        font = ImageFont.truetype("open-sans.ttf", 12)

        i = 1
        for point in points:
            x = point[0] * xScaling
            y = point[1] * yScaling
            draw.point((x, y), fill=(0, 0, 0))
            x += 2
            y += 2
            draw.text((x, y), str(i), fill=(0, 0, 0), font=font)
            i += 1

    def saveImage(self):
        self.image.save("out.jpg")

