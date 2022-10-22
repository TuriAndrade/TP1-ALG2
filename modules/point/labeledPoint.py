from __future__ import annotations
from .point import Point
from utils.exception import errorAssert
from numpy.typing import NDArray
from typing import List
import numpy as np


class LabeledPoint(Point):
    def __init__(self, coordinates: NDArray[np.float32], label: int = None) -> None:
        super().__init__(coordinates)
        self.label = label

    def getLabel(self) -> int:
        return self.label

    def setLabel(self, label) -> None:
        errorAssert(label is not None, "Invalid label.")
        self.label = label

    @staticmethod
    def getLabeledSet(labeledPoints: List[LabeledPoint], label: int) -> None:
        errorAssert((labeledPoints is not None) and (
            len(labeledPoints) > 0), "Invalid points.")

        pointsOfInterest: List[LabeledPoint] = []

        for point in labeledPoints:
            if(point.getLabel() == label):
                pointsOfInterest.append(point)

        return pointsOfInterest

    def __str__(self) -> str:
        return str(self.coordinates) + " " + str(self.label)
