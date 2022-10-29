from ..segment import Segment
from ..point import Point
from ..quicksort import quicksort
from ..stack import Stack
from utils.exception import errorAssert
from typing import List
import numpy as np


class ConvexHull2D:
    def __init__(self, points: List[Point], coordinate1: int, coordinate2: int) -> None:
        errorAssert((points is not None) and (
            len(points) > 2), "Invalid number of points.")
        errorAssert((coordinate1 is not None) and (
            coordinate2 is not None), "Invalid coordinates.")
        errorAssert((coordinate1 < points[0].getDim()) and (
            coordinate2 < points[0].getDim()), "Invalid coordinates.")

        self.__coordinate1 = coordinate1
        self.__coordinate2 = coordinate2

        self.__points: List[Point] = []

        self.__nPoints: int = 0

        self.getPoints(points)

        errorAssert(self.__nPoints > 2, "Invalid number of different points.")

        self.__hull: List[Point] = []

        self.build()

    def getPoints(self, points: List[Point]) -> None:
        for point in points:
            coordinates = [
                point.getCoordinate(self.__coordinate1),
                point.getCoordinate(self.__coordinate2)
            ]

            self.__points.append(Point(
                np.array(coordinates)
            ))

        self.__points = list(set(self.__points))
        self.__nPoints = len(self.__points)

    def removeCollinearPoints(self) -> None:
        count = 1
        for i in range(1, self.__nPoints):

            while ((i < self.__nPoints - 1) and
                   (Segment.direction2D(
                    0, 1,
                    Segment(self.__points[0], self.__points[i]),
                    Segment(self.__points[i], self.__points[i+1])) == 0)
                   ):
                i += 1

            self.__points[count] = self.__points[i]
            count += 1

        self.__points = self.__points[:count]
        self.__nPoints = count

    def build(self) -> None:
        p0: Point = self.__points[0]

        for i in range(1, self.__nPoints):
            if (p0.compare(self.__points[i], 1) == 1):
                p0 = self.__points[i]

        quicksort(
            self.__points, 0, self.__nPoints - 1,
            Segment.buildSegmentsComparison(
                0, 1, p0)
        )

        self.removeCollinearPoints()
        errorAssert(self.__nPoints > 2,
                    "Invalid number of non-collinear points.")

        pointStack = Stack()

        pointStack.push(self.__points[0])
        pointStack.push(self.__points[1])
        pointStack.push(self.__points[2])

        for i in range(3, self.__nPoints):

            while (
                (pointStack.getSize() > 1) and
                (Segment.direction2D(
                    0, 1,
                    Segment(pointStack.getNode(2), pointStack.getNode(1)),
                    Segment(pointStack.getNode(1), self.__points[i])) != 1)
            ):
                pointStack.pop()
            pointStack.push(self.__points[i])

        self.__hull = pointStack.toList()

    def getHull(self) -> List[Point]:
        return self.__hull
