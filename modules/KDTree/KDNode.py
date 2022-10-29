from __future__ import annotations
from ..point import Point
from utils.exception import errorAssert
from numpy.typing import NDArray
import numpy as np


class KDNode:
    def __init__(self, point: Point) -> None:
        errorAssert(point is not None, "Invalid point for node.")
        self.__point: Point = point
        self.__left: KDNode = None
        self.__right: KDNode = None
        self.__boundingBox: NDArray[np.float32] = None

    def __str__(self) -> str:
        return ("Coordinates: " + self.__point.__str__() + "\nBounding Box: " + str(self.__boundingBox))

    def getPoint(self) -> Point:
        return self.__point

    def getLeft(self) -> KDNode:
        return self.__left

    def setLeft(self, left: KDNode) -> None:
        self.__left = left

    def getRight(self) -> KDNode:
        return self.__right

    def setRight(self, right: KDNode) -> None:
        self.__right = right

    def getBoundingBox(self) -> NDArray[np.float32]:
        return self.__boundingBox

    def setBoundingBox(self, boundingBox: NDArray[np.float32]) -> None:
        self.__boundingBox = boundingBox

    def getPointCoordinate(self, coordinate: int) -> np.float32:
        return self.__point.getCoordinate(coordinate)

    def getPointCoordinates(self) -> NDArray[np.float32]:
        return self.__point.getCoordinates()
