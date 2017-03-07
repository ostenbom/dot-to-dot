from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_WIDTH = 5000
BASE_LIMIT = 15000

INITIAL_FONT_SIZE = 12
MIN_FONT_SIZE = 9

NUMBERS_PER_COLOUR = 100
WHITE = (255, 255, 255)
COLOURS = [(0, 0, 200), (50, 50, 50), (200, 0, 200), (200, 0, 0), (200, 100, 0), (200, 200, 0), (0, 200, 0), (0, 200, 200)]
OUTLINE_SPACE = 50

class OutputImage():

    def __init__(self, points, originalWidth, originalHeight, drawLines = False, ensureSpace = True):
        self.points = points[:]
        self.originalWidth = originalWidth
        self.originalHeight = originalHeight

        self.imageRatio = float(self.originalHeight) / float(self.originalWidth)

        self.base = BASE_IMAGE_WIDTH
        self.setInitialValuesFromBase(self.base, INITIAL_FONT_SIZE)

        drawFunc = self.drawLines if drawLines else self.drawPoints

        if ensureSpace:
            while self.base < BASE_LIMIT and not drawFunc(True):
                self.setInitialValuesFromBase(self.base + 500, self.fontSize - 0.5)

        self.setInitialValuesFromBase(self.base, self.fontSize)
        drawFunc(False)

    def setInitialValuesFromBase(self, base, fontSize):
        self.base = base
        self.fontSize = fontSize if fontSize > MIN_FONT_SIZE else MIN_FONT_SIZE
        imageWidth = base
        imageHeight = imageWidth * self.imageRatio

        fullWidth = imageWidth + (OUTLINE_SPACE * 2)
        fullHeight = imageHeight + (OUTLINE_SPACE * 2)

        self.fullWidth = fullWidth
        self.fullHeight = fullHeight

        self.xScaling = float(imageWidth) / float(self.originalWidth)
        self.yScaling = float(imageHeight) / float(self.originalHeight)

        print ("Dimensions: (" + str(imageWidth) + ", " + str(imageHeight) + ")")

        self.image = Image.new("RGB", (fullWidth, int(fullHeight)), color=WHITE)

        self.draw = ImageDraw.Draw(self.image)

        self.font = ImageFont.truetype("open-sans.ttf", int(self.fontSize))

        self.colorIndex = 0

    def getImageObject(self):
        return self.image

    def saveImage(self):
        self.image.save("dots.jpg")

    def showImage(self):
        self.image.show()

    def drawLines(self, ensureSpace):
        if not self.drawPoints(ensureSpace):
            return False

        points = self.points[:]

        i = 1
        color = self.pickNextColor()
        prev = points.pop(0)
        self.drawPointWithNumber(prev, i, color, ensureSpace)
        i += 1

        while len(points):
            current = points.pop(0)
            self.drawLineBetweenPoints(prev, current)
            prev = current
            i += 1

        return True

    def drawLineBetweenPoints(self, p1, p2):
        color = (0, 0, 0)

        x1 = p1[0] * self.xScaling + OUTLINE_SPACE
        x2 = p2[0] * self.xScaling + OUTLINE_SPACE

        y1 = p1[1] * self.yScaling + OUTLINE_SPACE
        y2 = p2[1] * self.yScaling + OUTLINE_SPACE

        self.draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

    def drawPoints(self, ensureSpace):
        i = 1
        color = self.pickNextColor()
        for point in self.points:
            if i % NUMBERS_PER_COLOUR == 0:
                color = self.pickNextColor()
            if not self.drawPointWithNumber(point, i, color, ensureSpace) and ensureSpace:
                return False
            i += 1

        return True

    def drawPointWithNumber(self, point, number, color, ensureSpace):
        if number == 1:
            pointSize = 4
        else:
            pointSize = 2

        ellipseX = point[0] * self.xScaling + OUTLINE_SPACE
        ellipseY = point[1] * self.yScaling + OUTLINE_SPACE
        textX, textY, success = self.chooseTextPoint(ellipseX, ellipseY, number)

        if not success and ensureSpace:
            return False

        self.draw.text((textX, textY), str(number), font=self.font, fill=color)
        self.draw.ellipse([ellipseX - pointSize, ellipseY - pointSize, ellipseX + pointSize, ellipseY + pointSize], fill=color)

        return True

    def chooseTextPoint(self, pointX, pointY, number):
        textWidth, textHeight = self.draw.textsize(str(number), self.font)
        possibleTextPositions = [
            (pointX + 2, pointY + 2),
            (pointX + 2, pointY - 2 - textHeight),
            (pointX - 2 - textWidth, pointY + 2),
            (pointX - 2 - textWidth, pointY - 2 - textHeight)]


        spaceExists = False

        for textPoint in possibleTextPositions:
            textX = textPoint[0]
            textY = textPoint[1]
            if not self.overlaps(textX, textY, textWidth, textHeight):
                spaceExists = True
                break


        if not spaceExists:
            print ('--- Overlap! No Space for Point: (' + str(pointX) + ', ' + str(pointY) + ') ---')
            return [textX, textY, False]

        return [textX, textY, True]

    def overlaps(self, textX, textY, width, height):
        for x in range(int(textX), int(textX + width + 1)):
            for y in range(int(textY), int(textY + height + 1)):
                if self.image.getpixel((x, y)) != WHITE:
                    return True
        return False

    def pickNextColor(self):
        color = COLOURS[self.colorIndex]
        self.colorIndex = (self.colorIndex + 1) % 8
        return color
