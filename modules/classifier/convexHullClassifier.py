from __future__ import annotations
from ..point import LabeledPoint, Point
from ..convexHull import ConvexHull2D
from ..KDTree import KDTree
from ..line import Line2D
from .classifier import Classifier
from utils.exception import errorAssert
from typing import List, Any, Tuple
from numpy.typing import NDArray
import numpy as np
import matplotlib.pyplot as plt


class ConvexHullClassifier(Classifier):
    def __init__(
        self,
        labeledDataset: List[LabeledPoint],
        trainLen: float = 0.7,
        positiveLabel: NDArray[np.int32] = np.array([0, 1]),
        negativeLabel: NDArray[np.int32] = np.array([-1]),
        name: str = "ConvexHullClassifier",
        nFolds: int = 5,
        foldSizeTreshold=15,
        coordinate1: int = 0,
        coordinate2: int = 1
    ) -> None:
        super().__init__(
            labeledDataset=labeledDataset,
            trainLen=trainLen,
            positiveLabel=positiveLabel,
            negativeLabel=negativeLabel,
            name=name,
            nFolds=nFolds,
            foldSizeTreshold=foldSizeTreshold
        )

        errorAssert((coordinate1 is not None) and (
            coordinate1 >= 0), "Invalid coordinate.")
        errorAssert((coordinate2 is not None) and (
            coordinate2 >= 0), "Invalid coordinate.")

        self.__coordinate1 = coordinate1
        self.__coordinate2 = coordinate2

        self.__linearlySeparablePoints: bool = False
        self.__hull0: List[Point] = []
        self.__hull1: List[Point] = []
        self.__connectHullsLine: Line2D = None
        self.__closestPointsHulls: Tuple[Point, Point] = None
        self.__separationLine: Line2D = None
        self.__set0: List[LabeledPoint] = []
        self.__set1: List[LabeledPoint] = []

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid point dataset.")

        for label in self._negativeLabel:
            self.__set0.extend(
                LabeledPoint.getLabeledSet(dataset, label)
            )

        for label in self._positiveLabel:
            self.__set1.extend(
                LabeledPoint.getLabeledSet(dataset, label)
            )

        ch0 = ConvexHull2D(self.__set0, self.__coordinate1, self.__coordinate2)
        ch1 = ConvexHull2D(self.__set1, self.__coordinate1, self.__coordinate2)

        self.__hull0: List[LabeledPoint] = ch0.getHull()
        self.__hull1: List[LabeledPoint] = ch1.getHull()

        [(p1, p2), dist] = KDTree.closestPointsSubsets(
            self.__hull0, self.__hull1)

        self.__connectHullsLine = Line2D(0, 1,
                                         point1=p1, point2=p2)

        self.__closestPointsHulls = (p1, p2)

        self.__separationLine = self.__connectHullsLine.perpendicularLine()

        self.__linearlySeparablePoints = self.__separationLine.areLinearlySeparable(
            self.__set0, self.__set1)

    def predict(self, point: Point) -> int:
        return self.__separationLine.getPointSide(point)

    @staticmethod
    def buildInstance(**kwargs) -> Any:

        def instance(labeledDataset) -> ConvexHullClassifier:
            return ConvexHullClassifier(labeledDataset=labeledDataset, **kwargs)

        return instance

    def linearSeparabilityTest(self) -> bool:
        return self.__linearlySeparablePoints

    def plotHulls(self, square=False) -> None:
        smallestCoord1 = self._labeledDataset[0].getCoordinate(
            self.__coordinate1)
        smallestCoord2 = self._labeledDataset[0].getCoordinate(
            self.__coordinate2)
        greatestCoord1 = self._labeledDataset[0].getCoordinate(
            self.__coordinate1)
        greatestCoord2 = self._labeledDataset[0].getCoordinate(
            self.__coordinate2)

        for i in range(1, len(self._labeledDataset)):
            currentCoord1 = self._labeledDataset[i].getCoordinate(
                self.__coordinate1)
            currentCoord2 = self._labeledDataset[i].getCoordinate(
                self.__coordinate2)

            if (currentCoord1 < smallestCoord1):
                smallestCoord1 = currentCoord1
            elif (currentCoord1 > greatestCoord1):
                greatestCoord1 = currentCoord1

            if (currentCoord2 < smallestCoord2):
                smallestCoord2 = currentCoord2
            elif (currentCoord2 > greatestCoord2):
                greatestCoord2 = currentCoord2

        isVertical, verticalCross = self.__separationLine.isVertical()

        if (isVertical):
            pLineP1 = Point(np.array([verticalCross, smallestCoord2]))
            pLineP2 = Point(np.array([verticalCross, greatestCoord2]))
        else:
            y1 = self.__separationLine.equation(smallestCoord1)
            y2 = self.__separationLine.equation(greatestCoord1)
            pLineP1 = Point(np.array([smallestCoord1, y1]))
            pLineP2 = Point(np.array([greatestCoord1, y2]))

        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        for point in self.__set0:
            ax.plot([point.getCoordinate(self.__coordinate1)], [
                    point.getCoordinate(self.__coordinate2)], marker="o", color="r")

        for point in self.__set1:
            ax.plot([point.getCoordinate(self.__coordinate1)], [
                    point.getCoordinate(self.__coordinate2)], marker="o", color="b")

        for i in range(len(self.__hull0) - 1):
            ax.plot([self.__hull0[i].getCoordinate(0),
                     self.__hull0[i+1].getCoordinate(0)],
                    [self.__hull0[i].getCoordinate(1),
                    self.__hull0[i+1].getCoordinate(1)], color='r')

        ax.plot([self.__hull0[len(self.__hull0) - 1].getCoordinate(0),
                 self.__hull0[0].getCoordinate(0)],
                [self.__hull0[len(self.__hull0) - 1].getCoordinate(1),
                self.__hull0[0].getCoordinate(1)], color="r")

        for i in range(len(self.__hull1) - 1):
            ax.plot([self.__hull1[i].getCoordinate(0),
                     self.__hull1[i+1].getCoordinate(0)],
                    [self.__hull1[i].getCoordinate(1),
                    self.__hull1[i+1].getCoordinate(1)], color='b')

        ax.plot([self.__hull1[len(self.__hull1) - 1].getCoordinate(0),
                 self.__hull1[0].getCoordinate(0)],
                [self.__hull1[len(self.__hull1) - 1].getCoordinate(1),
                self.__hull1[0].getCoordinate(1)], color="b")

        ax.plot([self.__closestPointsHulls[0].getCoordinate(0),
                 self.__closestPointsHulls[1].getCoordinate(0)], [
                self.__closestPointsHulls[0].getCoordinate(1),
                self.__closestPointsHulls[1].getCoordinate(1)], color="g")

        ax.plot([pLineP1.getCoordinate(0), pLineP2.getCoordinate(0)], [
                pLineP1.getCoordinate(1), pLineP2.getCoordinate(1)], color="y")

        if (square):
            ax.axis('square')
