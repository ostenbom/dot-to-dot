from PIL import Image
import numpy as np
import cv2

GAUSSIAN_KERNEL_SIZE = 3
GAUSSIAN_SIGMA = 0

DEFAULT_CANNY_SIGMA = 0.33
DEFAULT_IMAGES_TO_CHOOSE = 5

LOWER_SIGMA_THRESHOLD = 10
UPPER_SIGMA_THRESHOLD = 80

MAXIMUM_IMAGE_SIZE = 1920

class EdgeDetector():

    def __init__(self, fileName):
        self.fileName = fileName
        self.image = cv2.imread(fileName)
        grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(grayImage,
            (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE),
            GAUSSIAN_SIGMA)


    def getAutoCannyEdgePoints(self, image, sigma=DEFAULT_CANNY_SIGMA):
        median = np.median(image)

        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))
        return cv2.Canny(image, lower, upper)

    def getCannyEdges(self):
        edges = self.getAutoCannyEdgePoints(self.blurred)

        return edges

    def getCannyImage(self):
        edges = self.getAutoCannyEdgePoints(self.blurred)

        height, width, channels = self.image.shape
        image = self.createCannyImage(width, height, edges)

        return image

    def chooseCannyImage(self, choose=DEFAULT_IMAGES_TO_CHOOSE):
        thresholdStep = int(100.0 / (choose + 1))

        sigmas = []
        currentSigma = LOWER_SIGMA_THRESHOLD
        for i in range(choose):
            currentSigma += thresholdStep
            sigmas.append(currentSigma)

        cannyEdges = []
        for sigma in sigmas:
            sigmaPercent = float(sigma) / 100
            print(str(sigmaPercent))
            edge = self.getAutoCannyEdgePoints(self.blurred, sigmaPercent)
            cannyEdges.append(edge)

        # cv2.imwrite('out.png', np.hstack([cannyEdges[1]]))
        height, width, channels = self.image.shape
        selectionImage = self.createCannySelectionImage(width, height, cannyEdges)
        selectionImage.show()

        print("Pick an image between 1-" + str(choose))
        imagePick = int(input("Image Number: ")) - 1
        cannyPicked = cannyEdges[imagePick]

        return cannyPicked

    def createCannySelectionImage(self, width, height, cannyEdges):
        amountOfImages = len(cannyEdges)
        imageRatio = float(height) / width
        totalWidth = width * amountOfImages
        # totalWidth = min(MAXIMUM_IMAGE_SIZE, width * amountOfImages)
        # singleWidth = totalWidth / amountOfImages
        # totalHeight = int(singleWidth * imageRatio)
        image = Image.new("RGB", (totalWidth, height))

        cannyPixels = []
        currentWidth = 0
        for canny in cannyEdges:
            pixels = []
            y = 0
            for row in canny:
                x = 0
                for column in row:
                    if column == 255:
                        relativeX = x + currentWidth
                        image.putpixel((relativeX, y), (255, 255, 255))
                        #pixels.append((x, y))
                    x += 1
                y += 1
            currentWidth += width
            #cannyPixels.append(pixels)

        return image

    def createCannyImage(self, width, height, canny):
        image = Image.new("RGB", (width, height))
        y = 0
        for row in canny:
            x = 0
            for column in row:
                if column == 255:
                    image.putpixel((x, y), (255, 255, 255))
                x += 1
            y += 1
        return image
