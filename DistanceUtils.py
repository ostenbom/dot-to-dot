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
    print ("a: " + str(a1) + " b: " + str(b1) + " c: " + str(c1))
    print ("p1: " + str(p1) + " p2: " + str(p2) + " p3: " + str(p3))
    if p1 == (120, 198):
        import pdb; pdb.set_trace()


    areOnLine = colinear(p1, p2, p3)

    if not areOnLine:
        return 180

    if a1 == 0 or b1 == 0:
        return 90
    if abs(a1 - (b1 + c1)) < 0.001:
        return 180
    angle = math.degrees(math.acos(float((a1 * a1) - (b1 * b1) - (c1 * c1)) / float(-2 * b1 * c1)))
    return angle

def colinear(p1, p2, p3):
    x1 = p1[0]
    x2 = p2[0]
    x3 = p3[0]

    y1 = p1[0]
    y2 = p2[0]
    y3 = p3[0]
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)

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
