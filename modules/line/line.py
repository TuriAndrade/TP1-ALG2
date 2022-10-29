from __future__ import annotations
from ..point import Point
from ..segment import Segment
from utils.exception import errorAssert
from typing import Tuple, List
import numpy as np


class Line2D:
    def __init__(
        self, coordinate1: int, coordinate2: int, point1: Point, point2: Point = None, slope: float = None
    ) -> None:
        errorAssert(point1 is not None, "Invalid point.")
        errorAssert((point2 is None) or (point1.getDim() == point2.getDim()),
                    "Points of different dimensions.")
        errorAssert((coordinate1 < point1.getDim()) and (
            coordinate2 < point1.getDim()), "Invalid coordinates")
        errorAssert((slope is not None) or (point2 is not None),
                    "Line need slope and point or 2 points.")

        self.__coordinate1: int = coordinate1
        self.__coordinate2: int = coordinate2
        self.__point1: Point = point1
        self.__point2: Point = point2
        self.__vertical: bool = False
        self.__horizontal: bool = False
        self.__slope = slope
        self.__verticalCross: float = None
        self.__horizontalCross: float = None

        if (self.__slope is None):
            self.segment = Segment(self.__point1, self.__point2)
            self.__slope: float = self.computeSlope()

        if (np.isinf(self.__slope)):
            self.__vertical = True
            self.__verticalCross: float = point1.getCoordinate(coordinate1)
        else:
            self.c: float = point1.getCoordinate(
                coordinate2) - self.__slope*point1.getCoordinate(coordinate1)

            if (self.__slope == 0):
                self.__horizontal = True
                self.__horizontalCross: float = point1.getCoordinate(
                    coordinate2)

    def computeSlope(self) -> float:
        if (self.__slope is None):
            return self.segment.slope(self.__coordinate1, self.__coordinate2)
        else:
            return self.__slope

    def isVertical(self) -> Tuple[bool, float]:
        return self.__vertical, self.__verticalCross

    def isHorizontal(self) -> Tuple[bool, float]:
        return self.__horizontal, self.__horizontalCross

    def equation(self, coord1Init) -> float:
        if (self.__vertical):
            if (coord1Init == self.__point1.getCoordinate(self.__coordinate1)):
                return np.inf
            else:
                return np.nan

        elif (self.__horizontal):
            return self.__point1.getCoordinate(self.__coordinate2)

        else:
            return self.__slope*coord1Init + self.c

    def perpendicularLine(self, point: Point = None) -> Line2D:
        errorAssert((point is not None) or (
            self.__point2 is not None), "Point is necessary.")

        if (self.__vertical):
            if (point is not None):
                return Line2D(self.__coordinate1, self.__coordinate2, point, slope=0)

            else:
                medianPoint = self.segment.median()
                return Line2D(self.__coordinate1, self.__coordinate2, medianPoint, slope=0)

        elif (self.__horizontal):
            if (point is not None):
                return Line2D(self.__coordinate1, self.__coordinate2, point, slope=np.inf)

            else:
                medianPoint = self.segment.median()
                return Line2D(self.__coordinate1, self.__coordinate2, medianPoint, slope=np.inf)

        else:
            negSlope = -1/self.__slope

            if (point is not None):
                return Line2D(self.__coordinate1, self.__coordinate2, point, slope=negSlope)

            else:
                medianPoint = self.segment.median()
                return Line2D(self.__coordinate1, self.__coordinate2, medianPoint, slope=negSlope)

    def getPointSide(self, point: Point) -> int:
        if (self.__vertical):
            if (point.getCoordinate(self.__coordinate1) < self.__point1.getCoordinate(self.__coordinate1)):
                return -1
            elif (point.getCoordinate(self.__coordinate1) == self.__point1.getCoordinate(self.__coordinate1)):
                return 0
            else:
                return 1
        else:
            lineY = self.equation(point.getCoordinate(self.__coordinate1))

            if (point.getCoordinate(self.__coordinate2) < lineY):
                return -1
            elif (point.getCoordinate(self.__coordinate2) == lineY):
                return 0
            else:
                return 1

    def areLinearlySeparable(
        self, pointSet1: List[Point], pointSet2: List[Point]
    ) -> bool:
        errorAssert((len(pointSet1) > 0) and (
            len(pointSet2) > 0), "Invalid point sets.")

        ps1 = self.getPointSide(pointSet1[0])
        ps2 = self.getPointSide(pointSet2[0])

        if (ps1 == ps2):
            return False

        else:
            if (ps1 < 0):
                belowSet = pointSet1
                aboveSet = pointSet2
            elif (ps1 > 0):
                belowSet = pointSet2
                aboveSet = pointSet1
            elif (ps1 == 0):
                if (ps2 < 0):
                    belowSet = pointSet2
                    aboveSet = pointSet1
                else:
                    belowSet = pointSet1
                    aboveSet = pointSet2

        for i in range(1, len(belowSet)):
            psb = self.getPointSide(belowSet[i])

            if (psb > -1):
                return False

        for i in range(1, len(aboveSet)):
            psa = self.getPointSide(aboveSet[i])

            if (psa < 0):
                return False

        return True
