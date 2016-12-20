from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_WIDTH = 5000

class OutputImage():

    def __init__(self, points, originalDimensions, drawLines = False):
        self.points = points
        originalWidth = originalDimensions[0]
        originalHeight = originalDimensions[1]

        imageRatio = float(originalHeight) / float(originalWidth)

        imageHeight = BASE_IMAGE_WIDTH * imageRatio

        self.xScaling = float(BASE_IMAGE_WIDTH) / float(originalWidth)
        self.yScaling = float(imageHeight) / float(originalHeight)

        print ("Dimensions: (" + str(BASE_IMAGE_WIDTH) + ", " + str(imageHeight) + ")")

        self.image = Image.new("RGB", (BASE_IMAGE_WIDTH, int(imageHeight)), color=(255, 255, 255))

        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype("open-sans.ttf", 12)

        if drawLines:
            self.drawLines()
        else:
            self.drawPoints()


    def drawLines(self):
        i = 1
        prev = self.points.pop(0)
        self.drawPointWithNumber(prev, i)

        color = (0, 0, 0)

        while len(self.points):
            current = self.points.pop(0)
            self.drawLineBetweenPoints(prev, current)
            self.drawPointWithNumber(current, i)
            prev = current
            i += 1

    def drawLineBetweenPoints(self, p1, p2):
        color = (0, 0, 0)

        x1 = p1[0] * self.xScaling
        x2 = p2[0] * self.xScaling

        y1 = p1[1] * self.yScaling
        y2 = p2[1] * self.yScaling

        self.draw.line([(x1, y1), (x2, y2)], fill=color, width=1)

    def drawPoints(self):
        i = 1
        for point in self.points:
            self.drawPointWithNumber(point, i)
            i += 1

    def drawPointWithNumber(self, point, number):
        x = point[0] * self.xScaling
        y = point[1] * self.yScaling
        self.draw.point((x, y), fill=(0, 0, 0))
        x += 2
        y += 2
        self.draw.text((x, y), str(number), fill=(0, 0, 0), font=self.font)

    def saveImage(self):
        self.image.save("out.jpg")
