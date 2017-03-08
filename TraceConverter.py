import math
import sys
import numpy as np
import copy

from DistanceUtils import lineAngle, distanceBetween, angleBetween

TRACE_STEP = 5
DISTANCE_THRESHOLD = 0.55

class TraceConverter():

    def __init__(self, traces, distanceThreshold = None):
        self.traces = copy.deepcopy(traces)
        self.hasMadeLines = False
        self.lines = []

        if not distanceThreshold:
            self.distanceThreshold = DISTANCE_THRESHOLD
        else:
            print ('--- Threshold: ' + str(distanceThreshold) + ' ---')
            self.distanceThreshold = distanceThreshold

    def getLines(self):
        if not self.hasMadeLines:
            self.lines = self.convertTracesToLines()
            self.hasMadeLines = True
        return self.lines

    def convertTracesToLines(self):
        lines = []
        for trace in self.traces:
            lines.append(self.traceToLine(trace))

        return lines

    def traceToLine(self, trace):
        line = [trace[0]]

        while len(trace):
            lineSection = []
            for i in range(TRACE_STEP):
                if len(trace):
                    lineSection.append(trace.pop(0))

            while self.getLineDistanceAverage(lineSection) < self.distanceThreshold:
                if len(trace):
                    lineSection.append(trace.pop(0))
                else:
                    break

            line.append(lineSection[-1])

        return line


    def getLineDistanceAverage(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        if all([xs[0] == x for x in xs]) or all([ys[0] == y for y in ys]):
            return 0

        a1, c1 = np.polyfit(xs, ys, 1)
        b1 = -1

        distanceAvg = 0
        for point in points:
            x = point[0]
            y = point[1]
            distanceAvg += float(abs(a1*x + b1*y + c1))/math.sqrt(a1**2 + b1**2)
        distanceAvg = distanceAvg / len(points)

        return distanceAvg
