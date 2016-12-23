import unittest

from DistanceUtils import angleBetween


class TestDistanceUtils(unittest.TestCase):

    def setUp(self):
        self.middle = (5, 5)

    def testRightOf(self):
        right = (6, 5)
        angle = angleBetween(self.middle, right)

        self.assertEqual(angle, 0)

    def testRightTopCorner(self):
        rightTop = (6, 4)
        angle = angleBetween(self.middle, rightTop)

        self.assertEqual(angle, 45)

    def testAbove(self):
        above = (5, 4)
        angle = angleBetween(self.middle, above)

        self.assertEqual(angle, 90)

    def testLeftTopCorner(self):
        leftTop = (4, 4)
        angle = angleBetween(self.middle, leftTop)

        self.assertEqual(angle, 135)

    def testLeftOf(self):
        left = (4, 5)
        angle = angleBetween(self.middle, left)

        self.assertEqual(angle, 180)

    def testLeftBottomCorner(self):
        leftBottom = (4, 6)
        angle = angleBetween(self.middle, leftBottom)

        self.assertEqual(angle, 225)

    def testBelow(self):
        below = (5, 6)
        angle = angleBetween(self.middle, below)

        self.assertEqual(angle, 270)

    def testRightBottomCorner(self):
        rightBottom = (6, 6)
        angle = angleBetween(self.middle, rightBottom)

        self.assertEqual(angle, 315)
