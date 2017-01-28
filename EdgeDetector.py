import numpy as np
import cv2

GAUSSIAN_KERNEL_SIZE = 3
GAUSSIAN_SIGMA = 0

DEFAULT_CANNY_SIGMA = 0.33
DEFAULT_IMAGES_TO_CHOOSE = 5

LOWER_SIGMA_THRESHOLD = 10
UPPER_SIGMA_THRESHOLD = 80

class EdgeDetector():

    def __init__(self, fileName):
        self.fileName = fileName
        image = cv2.imread(fileName)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(gray,
            (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE),
            GAUSSIAN_SIGMA)


    def getAutoCannyEdgePoints(image, sigma=DEFAULT_CANNY_SIGMA):
        median = np.median(image)

        lower = int(max(0, (1.0 - sigma) * median))
        upper = int(min(255, (1.0 + sigma) * median))
        return cv2.Canny(image, lower, upper)

    def chooseCannyImage(choose=DEFAULT_IMAGES_TO_CHOOSE):
        step = int((UPPER_SIGMA_THRESHOLD - LOWER_SIGMA_THRESHOLD) / choose)

        sigmas = []
        currentSigma = LOWER_SIGMA_THRESHOLD
        for i in range(choose):
            currentSigma += step
            sigmas.append(currentSigma)

        cannyEdges = []
        for sigma in sigmas:
            edge = getAutoCannyEdgePoints(self.blurred, sigma)

        cv2.imshow("Edges", np.hstack(cannyEdges))

        print("Pick an image between 1-" + str(choose))
        imagePick = int(input("Image Number: ")) - 1
        cannyPicked = cannyEdges[imagePick]

        return cannyPicked
