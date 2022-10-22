from ..segment import Segment
from ..point import Point
from ..quicksort import quicksort
from ..stack import Stack
from utils.exception import errorAssert
from typing import List


class ConvexHull2D:
    def __init__(self, points: List[Point], coordinate1: int, coordinate2: int) -> None:
        errorAssert((points is not None) and (
            len(points) > 2), "Invalid number of points.")
        errorAssert((coordinate1 is not None) and (
            coordinate2 is not None), "Invalid coordinates.")
        errorAssert((coordinate1 < points[0].getDim()) and (
            coordinate2 < points[0].getDim()), "Invalid coordinates.")

        self.points: List[Point] = list(set(points))

        self.nPoints: int = len(self.points)

        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2

        self.hull: List[Point] = []

        self.build()

    def build(self) -> None:
        p0: Point = self.points[0]

        for i in range(1, self.nPoints):
            if(p0.compare(self.points[i], 0) == -1):
                p0 = self.points[i]

        quicksort(
            self.points, 0, self.nPoints - 1,
            Segment.buildSegmentsComparison(0, 1, p0)
        )

        pointStack = Stack()

        pointStack.push(self.points[0])
        pointStack.push(self.points[1])
        pointStack.push(self.points[2])

        for i in range(3, self.nPoints):
            top = pointStack.getNode(1)
            nextToTop = pointStack.getNode(2)

            segment1 = Segment(nextToTop, top)
            segment2 = Segment(top, self.points[i])

            while(Segment.direction2D(0, 1, segment1, segment2) < 0):
                pointStack.pop()

                if(pointStack.getSize() <= 1):
                    break

                top = pointStack.getNode(1)
                nextToTop = pointStack.getNode(2)

                segment1 = Segment(nextToTop, top)
                segment2 = Segment(top, self.points[i])

            pointStack.push(self.points[i])

        self.hull = pointStack.toList()

    def getHull(self) -> List[Point]:
        return self.hull
