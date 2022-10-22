from __future__ import annotations
from ..point import Point
from utils.exception import errorAssert
from numpy.typing import NDArray
import numpy as np


class KDNode:
    def __init__(self, point: Point) -> None:
        errorAssert(point is not None, "Invalid point for node.")
        self.point: Point = point
        self.left: KDNode = None
        self.right: KDNode = None
        self.boundingBox: NDArray[np.float32] = None

    def __str__(self) -> str:
        return ("Coordinates: " + self.point.__str__() + "\nBounding Box: " + str(self.boundingBox))

    def getPoint(self) -> Point:
        return self.point

    def getLeft(self) -> KDNode:
        return self.left

    def setLeft(self, left: KDNode) -> None:
        self.left = left

    def getRight(self) -> KDNode:
        return self.right

    def setRight(self, right: KDNode) -> None:
        self.right = right

    def getBoundingBox(self) -> NDArray[np.float32]:
        return self.boundingBox

    def setBoundingBox(self, boundingBox: NDArray[np.float32]) -> None:
        self.boundingBox = boundingBox

    def getPointCoordinate(self, coordinate: int) -> np.float32:
        return self.point.getCoordinate(coordinate)

    def getPointCoordinates(self) -> NDArray[np.float32]:
        return self.point.getCoordinates()
