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
    a = distanceBetween(p1, p2)
    b = distanceBetween(p2, p3)
    c = distanceBetween(p1, p3)
    if a == 0 or b == 0:
        return 90
    angle = math.degrees(math.acos(float(c * c - a * a - b * b) / float(-2 * a * b)))
    return angle

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
