import math
import sys
import numpy as np
import copy

from DistanceUtils import lineAngle, distanceBetween, angleBetween

TRACE_STEP = 3
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
            step = []
            for i in range(TRACE_STEP):
                if len(trace):
                    step.append(trace.pop(0))

            while self.getLineDistanceAverage(step) < self.distanceThreshold:
                if len(trace):
                    step.append(trace.pop(0))
                else:
                    break

            line.append(step[-1])

        return line


    def getLineDistanceAverage(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        a, c = np.polyfit(xs, ys, 1)
        b = -1

        distanceAvg = 0
        for point in points:
            x = point[0]
            y = point[1]
            distanceAvg += float(abs(a*x + b*y + c))/math.sqrt(a**2 + b**2)
        distanceAvg = distanceAvg / len(points)

        return distanceAvg
