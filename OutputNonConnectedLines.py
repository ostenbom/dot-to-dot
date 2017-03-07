from PIL import Image, ImageDraw, ImageFont
import copy

BASE_IMAGE_WIDTH = 5000
NUMBERS_PER_COLOUR = 100
COLOURS = [(0, 0, 200), (50, 50, 50), (200, 0, 200), (200, 0, 0), (200, 100, 0), (200, 200, 0), (0, 200, 0), (0, 200, 200)]

class OutputNonConnectedLines():

    def __init__(self, lines, originalWidth, originalHeight):
        self.lines = copy.deepcopy(lines)
        self.originalWidth = originalWidth
        self.originalHeight = originalHeight

        imageRatio = float(originalHeight) / float(originalWidth)

        imageHeight = BASE_IMAGE_WIDTH * imageRatio

        self.xScaling = float(BASE_IMAGE_WIDTH) / float(originalWidth)
        self.yScaling = float(imageHeight) / float(originalHeight)

        print ("Dimensions: (" + str(BASE_IMAGE_WIDTH) + ", " + str(imageHeight) + ")")

        self.image = Image.new("RGB", (BASE_IMAGE_WIDTH, int(imageHeight)), color=(255, 255, 255))

        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype("open-sans.ttf", 12)

        self.colorIndex = 0

        self.drawLines()

    def saveImage(self):
        self.image.save("lines.jpg")

    def showImage(self):
        self.image.show()

    def drawLines(self):
        i = 1
        for line in self.lines:
            color = self.pickNextColor()
            prev = line.pop(0)
            self.drawPoint(prev, color)
            i += 1

            while len(line):
                if i % NUMBERS_PER_COLOUR == 0:
                    color = self.pickNextColor()
                current = line.pop(0)
                self.drawLineBetweenPoints(prev, current)
                self.drawPoint(current, color)
                prev = current
                i += 1

    def drawLineBetweenPoints(self, p1, p2):
        color = (0, 0, 0)

        x1 = p1[0] * self.xScaling
        x2 = p2[0] * self.xScaling

        y1 = p1[1] * self.yScaling
        y2 = p2[1] * self.yScaling

        self.draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

    def drawPoint(self, point, color):
        pointSize = 2

        x = point[0] * self.xScaling
        y = point[1] * self.yScaling
        self.draw.ellipse([x - pointSize, y - pointSize, x + pointSize, y + pointSize], fill=color)
        x += 2
        y += 2

    def pickNextColor(self):
        color = COLOURS[self.colorIndex]
        self.colorIndex = (self.colorIndex + 1) % 8
        return color
