import math
import cairocffi as cairo
from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_WIDTH = 5000
BASE_LIMIT = 7000

A3_WIDTH = 842
A3_HEIGHT = 1191

INITIAL_FONT_SIZE = 6
MIN_FONT_SIZE = 6

NUMBERS_PER_COLOUR = 100
WHITE = (255, 255, 255)
COLOURS = [(0, 0, 200), (50, 50, 50), (200, 0, 200), (200, 0, 0), (200, 100, 0), (0, 0, 0), (0, 200, 0), (0, 200, 200)]
OUTLINE_SPACE = 50

class OutputImage():

    def __init__(self, points, originalWidth, originalHeight, drawLines = False, ensureSpace = True, pdfOutput = None):
        self.points = points[:]
        self.originalWidth = originalWidth
        self.originalHeight = originalHeight

        self.imageRatio = float(self.originalHeight) / float(self.originalWidth)

        self.base = A3_WIDTH if originalHeight > originalWidth else A3_HEIGHT
        self.setInitialValuesFromBase(self.base, INITIAL_FONT_SIZE)

        drawFunc = self.drawLines if drawLines else self.drawPoints

        self.pointPositions = []

        if ensureSpace:
            while self.base < BASE_LIMIT and not drawFunc(True, False):
                self.setInitialValuesFromBase(self.base + 500, self.fontSize - 0.5)

        self.setInitialValuesFromBase(self.base, self.fontSize)
        drawFunc(False, True)
        self.drawAsPdf(False, pdfOutput)

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

    def saveImage(self, path = None):
        if not path:
            path = 'dots.jpg'

        self.image.save(path)

    def showImage(self):
        self.image.show()


    def drawAsPdf(self, drawLines, path = None):
        if not path:
            path = "dots.pdf"
        ps = cairo.PDFSurface(path, self.fullWidth, self.fullHeight)
        cr = cairo.Context(ps)

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(2)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(int(self.fontSize))

        self.drawPDFPoints(cr)
        if drawLines:
            self.drawPDFLines(cr)


    def drawPDFLines(self, cr):
        cr.set_source_rgb(0, 0, 0)
        points = self.points[:]

        i = 1
        prev = points.pop(0)

        while len(points):
            curr = points.pop(0)
            self.drawPDFLine(cr, prev, curr)
            prev = curr

    def drawPDFLine(self, cr, p1, p2):
        x1 = p1[0] * self.xScaling + OUTLINE_SPACE
        x2 = p2[0] * self.xScaling + OUTLINE_SPACE

        y1 = p1[1] * self.yScaling + OUTLINE_SPACE
        y2 = p2[1] * self.yScaling + OUTLINE_SPACE
        cr.move_to(x1, y1)
        cr.line_to(x2, y2)
        cr.stroke()

    def drawLines(self, ensureSpace, savePointPositions):
        if not self.drawPoints(ensureSpace, savePointPositions):
            return False

        points = self.points[:]

        color = self.pickNextColor()
        prev = points.pop(0)

        while len(points):
            current = points.pop(0)
            self.drawLineBetweenPoints(prev, current)
            prev = current

        return True

    def drawLineBetweenPoints(self, p1, p2):
        color = (0, 0, 0)

        x1 = p1[0] * self.xScaling + OUTLINE_SPACE
        x2 = p2[0] * self.xScaling + OUTLINE_SPACE

        y1 = p1[1] * self.yScaling + OUTLINE_SPACE
        y2 = p2[1] * self.yScaling + OUTLINE_SPACE

        self.draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

    def drawPoints(self, ensureSpace, savePointPositions):
        if savePointPositions:
            self.pointPositions = []
        i = 1
        color = self.pickNextColor()
        for point in self.points:
            if i % NUMBERS_PER_COLOUR == 0:
                color = self.pickNextColor()
            if not self.drawPointWithNumber(point, i, color, ensureSpace, savePointPositions) and ensureSpace:
                return False
            i += 1

        return True

    def drawPDFPoints(self, cr):
        i = 1
        colour = self.pickNextColor()
        for j, point in enumerate(self.points):
            if i % NUMBERS_PER_COLOUR == 0:
                colour = self.pickNextColor()
            self.drawPDFCircle(cr, point, colour)
            self.drawPDFText(cr, i, point, self.pointPositions[j], colour)
            i += 1

    def drawPDFCircle(self, cr, point, colour):
        x = point[0] * self.xScaling + OUTLINE_SPACE
        y = point[1] * self.yScaling + OUTLINE_SPACE

        pointSize = 2

        r, g, b = self.colourToFloats(colour)
        cr.set_source_rgb(r, g, b)
        cr.move_to(x, y)
        cr.arc(x, y, pointSize, 0, 2 * math.pi)
        cr.fill()

    def drawPDFText(self, cr, number, point, positionIndex, colour):
        pointX = point[0] * self.xScaling + OUTLINE_SPACE
        pointY = point[1] * self.yScaling + OUTLINE_SPACE

        _, _, textWidth, textHeight, _, _ = cr.text_extents(str(number))

        pointSize = 4

        possibleTextPositions = [
            (pointX + pointSize, pointY + pointSize + textHeight),
            (pointX + pointSize, pointY - pointSize),
            (pointX - pointSize - textWidth, pointY - pointSize),
            (pointX - pointSize - textWidth, pointY + pointSize + textHeight)]

        x, y = possibleTextPositions[positionIndex]
        cr.move_to(x, y)
        r, g, b = self.colourToFloats(colour)
        cr.set_source_rgb(r, g, b)
        cr.show_text(str(number))

    def drawPointWithNumber(self, point, number, color, ensureSpace, savePointPositions):
        pointSize = 3

        ellipseX = point[0] * self.xScaling + OUTLINE_SPACE
        ellipseY = point[1] * self.yScaling + OUTLINE_SPACE
        textX, textY, positionIndex, success = self.chooseTextPoint(ellipseX, ellipseY, number, ensureSpace)
        if savePointPositions:
            self.pointPositions.append(positionIndex)

        if not success and ensureSpace:
            return False

        self.draw.text((textX, textY), str(number), font=self.font, fill=color)
        self.draw.ellipse([ellipseX - pointSize, ellipseY - pointSize, ellipseX + pointSize, ellipseY + pointSize], fill=color)

        return True

    def chooseTextPoint(self, pointX, pointY, number, ensureSpace):
        textWidth, textHeight = self.draw.textsize(str(number), self.font)
        possibleTextPositions = [
            (pointX + 2, pointY + 2),
            (pointX + 2, pointY - 2 - textHeight),
            (pointX - 2 - textWidth, pointY - 2 - textHeight),
            (pointX - 2 - textWidth, pointY + 2)]


        spaceExists = False

        for textPoint in possibleTextPositions:
            textX = textPoint[0]
            textY = textPoint[1]
            if not self.overlaps(textX, textY, textWidth, textHeight):
                spaceExists = True
                break

        if not spaceExists:
            if ensureSpace:
                print ('--- Overlap! No Space for Point: (' + str(pointX) + ', ' + str(pointY) + ') ---')
            return [textX, textY, possibleTextPositions.index((textX, textY)), False]

        return [textX, textY, possibleTextPositions.index((textX, textY)), True]

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

    def colourToFloats(self, colour):
        r = float(colour[0]) / 255
        g = float(colour[1]) / 255
        b = float(colour[2]) / 255

        return r, g, b
