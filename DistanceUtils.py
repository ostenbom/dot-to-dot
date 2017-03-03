import math

def distanceBetween(first, second):
    x1 = first[0]
    x2 = second[0]

    y1 = first[1]
    y2 = second[1]

    deltaX = abs(x1 - x2)
    deltaY = abs(y1 - y2)

    distance = math.sqrt(float(deltaX * deltaX) + float(deltaY * deltaY))

    return distance

def lineAngle(p1, p2, p3):
    b1 = distanceBetween(p1, p2)
    c1 = distanceBetween(p2, p3)
    a1 = distanceBetween(p1, p3)

    pointsOnLine = colinear(p1, p2, p3)

    if pointsOnLine:
        return 180
    if a1 == 0 or b1 == 0:
        return 90
    if abs(a1 - (b1 + c1)) < 0.001:
        return 180

    f1 = float((a1 * a1) - (b1 * b1) - (c1 * c1)) / float(-2 * b1 * c1)

    # Round down if going to be math domain error and very close
    if f1 > 0 and f1 - 1 > 0 and f1 - 1 < 0.01:
        f1 = 1
    elif f1 < 0 and f1 + 1 < 0 and f1 + 1 > -0.01:
        f1 = -1

    angle = math.degrees(math.acos(f1))
    return angle

def colinear(p1, p2, p3):
    p1x = p1[0]
    p2x = p2[0]
    p3x = p3[0]

    p1y = p1[1]
    p2y = p2[1]
    p3y = p3[1]

    area = p1x * ( p2y - p3y ) + p2x * ( p3y - p1y ) + p3x * ( p1y - p2y )

    return area == 0

def angleBetween(p1, p2):
    assert p1 != p2

    x1 = p1[0]
    x2 = p2[0]

    y1 = p1[1]
    y2 = p2[1]

    deltaX = abs(x1 - x2)
    deltaY = abs(y1 - y2)

    if deltaX == 0:
        if y1 > y2:
            return 90
        else:
            return 270

    angle = math.degrees(math.atan(float(deltaY) / float(deltaX)))
    if x1 < x2 and y1 > y2:
        pass
    elif x1 > x2 and y1 >= y2:
        angle = 180 - angle
    elif x1 < x2 and y1 < y2:
        angle = 360 - angle
    elif x1 > x2 and y1 < y2:
        angle = 180 + angle

    return angle
