from PIL import Image, ImageDraw, ImageFont
from CannyScorer import CannyScorer
import copy

class ConnectionImage():

    def __init__(self, lines, cannyScorer, width, height):
        self.lines = lines
        self.inbetweenLines = []
        self.cannyScorer = cannyScorer

        self.width = width
        self.height = height
        self.image = cannyScorer.getCannyImage().copy()
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype('open-sans.ttf', 12)

    def showImage(self):
        self.image.show()

    def scoreInbetweenLines(self):
        lines = copy.deepcopy(self.lines)

        prev = lines.pop(0)
        while len(lines):
            curr = lines.pop(0)
            start = prev[-1]
            end = curr[0]
            lineScore = self.cannyScorer.scoreLine(start, end)
            self.inbetweenLines.append((lineScore, [start, end]))
            prev = curr


    def drawInbetweenLines(self):
        self.scoreInbetweenLines()
        minScore = min(self.inbetweenLines, key=lambda x: x[1])[0]
        maxScore = max(self.inbetweenLines, key=lambda x: x[0])[0]

        for line in self.inbetweenLines:
            score = line[0]
            colorScale = float(score - minScore) / float(maxScore - minScore)
            color = (int(round(255 * colorScale)), 0, int(round(255 - (255 * colorScale))))
            self.drawLine(line, color)

    def drawLine(self, line, color):
        p1 = line[1][0]
        p2 = line[1][1]
        self.draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=color, width=1)
