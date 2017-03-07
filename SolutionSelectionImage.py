from PIL import Image, ImageDraw, ImageFont

from OutputImage import OutputImage

WHITE=(255, 255, 255)

class SolutionSelectionImage():

    # Only defined for 6 potential solutions
    def __init__(self, potentialSolutions, width, height):
        assert(len(potentialSolutions) == 6)

        self.potentialSolutions = potentialSolutions

        self.solutionImages = []
        for image in potentialSolutions:
            flatPoints = [point for sublist in image for point in sublist]
            out = OutputImage(flatPoints, width, height, True, False)

            self.singleWidth = out.fullWidth
            self.singleHeight = out.fullHeight

            self.solutionImages.append(out.getImageObject())

        self.totalWidth = self.singleWidth * 3
        self.totalHeight = self.singleHeight * 2

        self.image = Image.new("RGB", (int(self.totalWidth), int(self.totalHeight) + 1), color=WHITE)

        self.createSolutionSelectionImage()

    def createSolutionSelectionImage(self):
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
        self.image.save("selectionImage.jpg")
