from PIL import Image, ImageDraw, ImageFont

from OutputNonConnectedLines import OutputNonConnectedLines

WHITE=(255, 255, 255)

class LineDetailViewing():

    # Only defined for 6 potential solutions
    def __init__(self, lines, width, height):
        assert(len(lines) == 6)

        self.lines = lines
        self.width = width
        self.height = height

    def createSolutionSelectionImage(self):
        self.solutionImages = []
        for lineGroup in self.lines:
            out = OutputNonConnectedLines(lineGroup, self.width, self.height)

            self.singleWidth = out.width
            self.singleHeight = out.height

            self.solutionImages.append(out.getImageObject())

        self.totalWidth = self.singleWidth * 3
        self.totalHeight = self.singleHeight * 2

        self.image = Image.new("RGB", (int(self.totalWidth), int(self.totalHeight) + 1), color=WHITE)


        placements = [
            (0, 0),
            (self.singleWidth, 0),
            (self.singleWidth * 2, 0),
            (0, int(self.singleHeight)),
            (self.singleWidth, int(self.singleHeight)),
            (self.singleWidth * 2, int(self.singleHeight))
        ]

        for i in range(6):
            self.image.paste(self.solutionImages[i], placements[i])

        return

    def saveImage(self):
        self.image.save("lineDetailView.jpg")

    def showImage(self):
        self.image.show()
