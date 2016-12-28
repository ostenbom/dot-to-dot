import random
from ortools.constraint_solver import pywrapcp
# Must be imported after pywrapcp
from ortools.constraint_solver import routing_enums_pb2


from DistanceUtils import distanceBetween, angleBetween
from Segment import Segment

MAX_SEGMENTS = 100

class TraceConnecter():

    def __init__(self, segments, width, height):
        self.segments = []
        for segment in segments:
            self.segments.append(Segment(segment))
        self.width = width
        self.height = height

        amountNonEmpty = sum([ s.isEmpty() for s in self.segments ])

        if amountNonEmpty < MAX_SEGMENTS:
            self.numberTracingSegments = amountNonEmpty
        else:
            self.numberTracingSegments = MAX_SEGMENTS

        self.segments.sort(key = lambda l : l.getLength())
        self.largestSegments = self.segments[-self.numberTracingSegments:]

        self.points = []
        self.hasConnectedPoints = False

    def getConnectedTraces(self):
        if not self.hasConnectedPoints:
            self.connectTraces()
        return self.points

    def connectTraces(self):
        nodeOrder = self.getOptimalRoute()

        self.points = self.getPointsFromOrder(nodeOrder)

    def getPointsFromOrder(self, nodeOrder):
        points = []
        distanceBetweenSegments = []
        lastPointPositions = []

        for node in nodeOrder:
            segment = self.largestSegments[node]

            if len(lastPointPositions):
                lastPoint = lastPointPositions[-1]
                firstPoint = segment.getAtIndex(0)
                distance = distanceBetween(lastPoint, firstPoint)
                distanceBetweenSegments.append(distance)

            if not segment.isEmpty():
                endPoint = segment.getAtIndex(-1)
                lastPointPositions.append(endPoint)

            for point in segment.points:
                points.append(point)

        distanceBetweenSegments.sort()
        print ('Longest distances between segments: ', distanceBetweenSegments[-5:])
        return points

    def getOptimalRoute(self):
        routing = pywrapcp.RoutingModel(self.numberTracingSegments, 1, 0)
        routeCallback = self.distanceBetweenNodes
        routing.SetArcCostEvaluatorOfAllVehicles(routeCallback)

        assignment = routing.Solve()
        segmentOrderIndexes = []

        if assignment:
            print ('Optimal Route:')

            # Solution cost.
            print ('Cost: ', assignment.ObjectiveValue())
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
            route_number = 0
            node = routing.Start(route_number)

            route = ''
            while not routing.IsEnd(node):
                segmentOrderIndexes.append(node)
                route += str(node) + ' -> '
                node = assignment.Value(routing.NextVar(node))
            route += '0'
            print(route)

            return segmentOrderIndexes
        else:
            print('No solution found.')

    def distanceBetweenNodes(self, i, j):
        first = self.largestSegments[i]
        second = self.largestSegments[j]

        firstCenter = first.getCenter()
        secondCenter = second.getCenter()

        return distanceBetween(firstCenter, secondCenter)
