from ..point import LabeledPoint, Point
from ..convexHull import ConvexHull2D
from ..KDTree import KDTree
from ..line import Line2D
from .classifier import Classifier
from utils.exception import errorAssert
from typing import List
from numpy.typing import NDArray
import numpy as np


class ConvexHullClassifier(Classifier):
    def __init__(
        self,
        coordinate1: int,
        coordinate2: int,
        labeledDataset: List[LabeledPoint],
        trainLen: float = 0.7,
        positiveLabel: NDArray[np.int32] = np.array([0, 1]),
        negativeLabel: NDArray[np.int32] = np.array([-1])
    ) -> None:
        super().__init__(labeledDataset, trainLen, positiveLabel, negativeLabel)

        errorAssert((coordinate1 is not None) and (
            coordinate2 is not None), "Invalid coordinates.")

        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2
        self.linearlySeparablePoints: bool = False
        self.separationLine: Line2D = None

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid point dataset.")

        set0: List[LabeledPoint] = []
        set1: List[LabeledPoint] = []

        for label in self.negativeLabel:
            set0.extend(
                LabeledPoint.getLabeledSet(dataset, label)
            )

        for label in self.positiveLabel:
            set1.extend(
                LabeledPoint.getLabeledSet(dataset, label)
            )

        ch0 = ConvexHull2D(set0, self.coordinate1, self.coordinate2)
        ch1 = ConvexHull2D(set1, self.coordinate1, self.coordinate2)

        hull0: List[LabeledPoint] = ch0.getHull()
        hull1: List[LabeledPoint] = ch1.getHull()

        [(p1, p2), dist] = KDTree.closestPointsSubsets(hull0, hull1)

        line = Line2D(self.coordinate1, self.coordinate2, point1=p1, point2=p2)
        self.separationLine = line.perpendicularLine()

        self.linearlySeparablePoints = self.separationLine.areLinearlySeparable(
            set0, set1)

    def predict(self, point: Point) -> int:
        return self.separationLine.getPointSide(point)
