from __future__ import annotations
from ..point import Point
from utils.exception import errorAssert
from typing import Any, List
from numpy.typing import NDArray
import numpy as np


class Segment:
    def __init__(self, p1: Point, p2: Point) -> None:
        errorAssert((p1 is not None) and (p2 is not None), "Invalid points.")
        errorAssert(p1.getDim() == p2.getDim(),
                    "Points of different dimensions.")

        self.points: List[Point] = [p1, p2]
        self.dim = p1.getDim()

    def __eq__(self, segment: Segment) -> bool:
        return (
            (
                (self.getPoint(0) == segment.getPoint(0)) and
                (self.getPoint(1) == segment.getPoint(1))
            ) or
            (
                (self.getPoint(1) == segment.getPoint(0)) and
                (self.getPoint(0) == segment.getPoint(1))
            )
        )

    def getDim(self) -> int:
        return self.dim

    def getPoint(self, index: int) -> Point:
        errorAssert(index == 0 or index == 1, "Invalid index.")

        return self.points[index]

    def getPointCoordinate(self, index: int, coordinate: int) -> np.float32:
        errorAssert(coordinate < self.dim, "Invalid coordinates")
        errorAssert(index == 0 or index == 1, "Invalid index.")

        return self.points[index].getCoordinate(coordinate)

    def getPointCoordinates(self, index: int) -> NDArray:
        errorAssert(index == 0 or index == 1, "Invalid index.")

        return self.points[index].getCoordinates()

    def computeLength(self) -> float:
        return self.points[0].computeDist(self.points[1])

    @staticmethod
    def buildSegmentsComparison(coordinate1: int, coordinate2: int, p0: Point) -> Any:
        def compareLE(p1: Point, p2: Point) -> bool:
            segment1 = Segment(p0, p1)
            segment2 = Segment(p0, p2)

            d = Segment.direction2D(
                coordinate1, coordinate2, segment1, segment2)

            if(d == 1):
                return True
            elif(d == -1):
                return False
            else:
                return segment1.computeLength() <= segment2.computeLength()

        return compareLE

    @staticmethod
    def onBounds(segment: Segment, point: Point) -> bool:
        errorAssert(segment.getDim() == point.getDim(),
                    "Point and segment of different dimensions.")

        for i in range(segment.getDim()):
            if(
                (point.getCoordinate(i) < min(segment.getPointCoordinate(0, i), segment.getPointCoordinate(1, i))) or
                (point.getCoordinate(i) > max(segment.getPointCoordinate(
                    0, i), segment.getPointCoordinate(1, i)))
            ):
                return False

        return True

    @staticmethod
    def direction2D(coordinate1: int, coordinate2: int, segment1: Segment, segment2: Segment) -> int:
        errorAssert(segment1.getDim() == segment2.getDim(),
                    "Segments of different dimensions.")

        errorAssert(
            (coordinate1 < segment1.getDim()) and
            (coordinate2 < segment1.getDim()),
            "Invalid coordinates."
        )

        p1 = Point(np.array([
            segment1.getPointCoordinate(1, coordinate1) -
            segment1.getPointCoordinate(0, coordinate1),
            segment1.getPointCoordinate(1, coordinate2) -
            segment1.getPointCoordinate(0, coordinate2)
        ]))

        p2 = Point(np.array([
            segment2.getPointCoordinate(1, coordinate1) -
            segment2.getPointCoordinate(0, coordinate1),
            segment2.getPointCoordinate(1, coordinate2) -
            segment2.getPointCoordinate(0, coordinate2)
        ]))

        vectorProduct = (
            (
                p1.getCoordinate(coordinate1) *
                p2.getCoordinate(coordinate2)
            ) -
            (
                p2.getCoordinate(coordinate1) *
                p1.getCoordinate(coordinate2)
            )
        )

        if(vectorProduct < 0):
            return -1
        elif(vectorProduct > 0):
            return 1
        else:
            return 0

    @staticmethod
    def intersects2D(coordinate1: int, coordinate2: int, segment1: Segment, segment2: Segment) -> bool:
        p1 = segment1.getPoint(0)
        p2 = segment1.getPoint(1)

        q1 = segment2.getPoint(0)
        q2 = segment2.getPoint(1)

        p1p2: Segment = segment1
        p1q1: Segment = Segment(p1, q1)
        p1q2: Segment = Segment(p1, q2)

        d1: int = Segment.direction2D(coordinate1, coordinate2, p1p2, p1q1)
        d2: int = Segment.direction2D(coordinate1, coordinate2, p1p2, p1q2)

        q1q2: Segment = segment2
        q1p1: Segment = Segment(q1, p1)
        q1p2: Segment = Segment(q1, p2)

        d3: int = Segment.direction2D(coordinate1, coordinate2, q1q2, q1p1)
        d4: int = Segment.direction2D(coordinate1, coordinate2, q1q2, q1p2)

        if((d1*d2 == -1) and (d3*d4 == -1)):
            return True

        elif((d1 == 0) and (Segment.onBounds(p1p2, q1))):
            return True
        elif((d2 == 0) and (Segment.onBounds(p1p2, q2))):
            return True
        elif((d3 == 0) and (Segment.onBounds(q1q2, p1))):
            return True
        elif((d4 == 0) and (Segment.onBounds(q1q2, p2))):
            return True
        else:
            return False

    def __str__(self) -> str:
        return self.points[0].__str__() + ", " + self.points[1].__str__()

    def slope(self, coordinate1: int, coordinate2: int) -> float:
        if(self.getPointCoordinate(1, coordinate1) == self.getPointCoordinate(0, coordinate1)):
            return np.inf

        elif(self.getPointCoordinate(1, coordinate2) == self.getPointCoordinate(0, coordinate2)):
            return 0

        else:
            return (self.getPointCoordinate(1, coordinate2) -
                    self.getPointCoordinate(0, coordinate2)) / \
                (self.getPointCoordinate(1, coordinate1) -
                 self.getPointCoordinate(0, coordinate1))

    def internalProduct(self, segment: Segment) -> float:
        errorAssert(self.dim == segment.getDim(),
                    "Segments of different dimensions.")

        v1 = (self.getPoint(1) - self.getPoint(0))

        v2 = (segment.getPoint(1) - segment.getPoint(0))

        return (v1*v2)

    def median(self) -> Point:
        endPoint = self.getPoint(1)
        startPoint = self.getPoint(0)

        endCoordinates = endPoint.getCoordinates()
        startCoordinates = startPoint.getCoordinates()

        median = startCoordinates + (endCoordinates - startCoordinates)/2

        return Point(median)

    def getPointOrder(self, index: int, coordinate: int) -> int:
        errorAssert(coordinate < self.dim, "Invalid coordinate.")
        errorAssert(index == 0 or index == 1, "Invalid index.")

        return self.points[index].compare(self.points[(index + 1) % 2], coordinate)
