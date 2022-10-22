from __future__ import annotations
from utils.exception import errorAssert
from numpy.typing import NDArray
from typing import Any
import numpy as np


class Point:
    def __init__(self, coordinates: NDArray[np.float32]) -> None:
        errorAssert(len(coordinates) > 0,
                    "Point must be in space of at least 1 dimension.")

        self.dim: int = len(coordinates)
        self.coordinates: NDArray[np.float32] = coordinates

    @staticmethod
    def buildPointsComparison(coordinate: int, type: str = 'LE') -> Any:
        def LE(point1: Point, point2: Point) -> bool:
            return point1.compare(point2, coordinate) < 1

        def LT(point1: Point, point2: Point) -> bool:
            return point1.compare(point2, coordinate) == -1

        def GE(point1: Point, point2: Point) -> bool:
            return point1.compare(point2, coordinate) > -1

        def GT(point1: Point, point2: Point) -> bool:
            return point1.compare(point2, coordinate) == 1

        if(type == 'LE'):
            return LE
        elif(type == 'LT'):
            return LT
        elif(type == 'GE'):
            return GE
        else:
            return GT

    def __eq__(self, point: Point) -> bool:
        if(not isinstance(point, self.__class__)):
            return False

        if(self.dim != point.getDim()):
            return False

        pointCoordinates: NDArray[np.float32] = point.getCoordinates()

        return np.array_equal(self.coordinates, pointCoordinates)

    def __ne__(self, point: Point) -> bool:
        return (not self.__eq__(point))

    def __hash__(self):
        toTuple = []

        for i in range(self.dim):
            toTuple.append(('x'+str(i), self.coordinates[i]))

        toTuple.append(('dim', self.dim))

        return hash(tuple(toTuple))

    def __sub__(self, point: Point) -> Point:
        errorAssert(isinstance(point, self.__class__),
                    "Can't subtract points.")
        errorAssert(self.dim == point.getDim(),
                    "Points of different dimensions.")

        coordinates = self.coordinates - point.getCoordinates()

        return Point(coordinates)

    def __mul__(self, point: Point) -> float:
        errorAssert(isinstance(point, self.__class__),
                    "Can't multiply points.")
        errorAssert(self.dim == point.getDim(),
                    "Points of different dimensions.")

        return np.inner(self.coordinates, point.getCoordinates())

    def computeDist(self, point: Point, coordinate: int = None) -> float:
        errorAssert(self.dim == point.dim, "Points in diferent dimensions.")

        pointCoordinates: NDArray[np.float32] = point.getCoordinates()

        if(coordinate is not None):
            errorAssert(coordinate < self.dim, "Invalid point coordinate.")
            return np.abs(self.coordinates[coordinate] - pointCoordinates[coordinate])

        return np.linalg.norm(self.coordinates - pointCoordinates)

    def compareCoordinate(self, point: Point, coordinate: int) -> int:

        pointCoordinates: NDArray[np.float32] = point.getCoordinates()
        if(self.coordinates[coordinate] > pointCoordinates[coordinate]):
            return 1
        elif(self.coordinates[coordinate] == pointCoordinates[coordinate]):
            return 0
        else:
            return -1

    def compare(self, point: Point, coordinate: int) -> int:
        errorAssert(self.dim == point.dim, "Points in diferent dimensions.")
        errorAssert(coordinate < self.dim, "Invalid point coordinate.")

        result: int = self.compareCoordinate(point, coordinate)

        if(result == 0):
            for i in range(self.dim):
                if(i != coordinate):
                    result = self.compareCoordinate(point, i)
                    if(result != 0):
                        return result

        return result

    def __str__(self) -> str:
        return str(self.coordinates)

    def getCoordinates(self) -> NDArray[np.float32]:
        return self.coordinates

    def getDim(self) -> int:
        return self.dim

    def getCoordinate(self, coordinate: int) -> np.float32:
        errorAssert(coordinate < self.dim, "Invalid coordinate.")

        return self.coordinates[coordinate]
