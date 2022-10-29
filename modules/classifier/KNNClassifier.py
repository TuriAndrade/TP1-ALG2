from __future__ import annotations
from ..point import LabeledPoint, Point
from ..KDTree import KDTree
from .classifier import Classifier
from utils.exception import errorAssert
from typing import List, Dict, Any
from numpy.typing import NDArray
import numpy as np


class KNNClassifier(Classifier):
    def __init__(
        self,
        labeledDataset: List[LabeledPoint],
        trainLen: float = 0.7,
        positiveLabel: NDArray[np.int32] = np.array([0, 1]),
        negativeLabel: NDArray[np.int32] = np.array([-1]),
        name: str = "KNNClassifier",
        nFolds: int = 5,
        foldSizeTreshold=15,
        k: int = 5,
        maxK: int = 100,
        optimalK: bool = True,
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

        errorAssert(optimalK or ((k is not None) and (k > 0)),
                    "Invalid k parameter.")

        errorAssert((maxK is None) or (maxK > 0), "Invalid max k parameter.")

        self.__maxK: int = np.inf if (maxK is None) else maxK
        self.__KDTree: KDTree = None
        self.__k: int = k
        self.__optimalK: bool = optimalK

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid point dataset.")

        self.__KDTree = KDTree(dataset)

    def predict(self, point: Point) -> int:
        KNN = self.__KDTree.kNearestNeighbors(point, self.__k)

        PCount: int = 0
        NCount: int = 0

        for neighbor in KNN:
            if (neighbor[0].getLabel() in self._negativeLabel):
                NCount += 1
            elif (neighbor[0].getLabel() in self._positiveLabel):
                PCount += 1

        if (PCount >= NCount):
            return self._positiveLabel[0]
        else:
            return self._negativeLabel[0]

    def findOptimalK(self) -> None:
        bestF1 = -1
        bestK = 0

        sqrtLen: np.float32 = np.sqrt(len(self._trainSet))
        rangeLen: int = int(np.min(np.array([sqrtLen, self.__maxK])))

        for k in range(1, rangeLen):
            self.__k = k
            evaluation = self.crossValidation()

            meanEvaluation = evaluation.mean()

            if (meanEvaluation["F1"] > bestF1):
                bestF1 = meanEvaluation["F1"]
                bestK = k

        self.__k = bestK

    def run(self) -> Dict:
        self.splitDataset()

        if (self.__optimalK):
            self.findOptimalK()

        crossValidationMetrics = self.crossValidation(self._nFolds)

        self.trainModel(self._trainSet)
        testConfusionMatrix, testMetrics = self.evaluateModel(self._testSet)

        return {
            "Cross Validation Metrics": crossValidationMetrics,
            "Test Metrics": testMetrics,
            "Test Confusion Matrix": testConfusionMatrix
        }

    @staticmethod
    def buildInstance(**kwargs) -> Any:

        def instance(labeledDataset) -> KNNClassifier:
            return KNNClassifier(labeledDataset=labeledDataset, **kwargs)

        return instance
