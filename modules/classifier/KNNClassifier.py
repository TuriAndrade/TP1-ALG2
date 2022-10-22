from ..point import LabeledPoint, Point
from ..KDTree import KDTree
from .classifier import Classifier
from utils.exception import errorAssert
from typing import List, Dict
from numpy.typing import NDArray
import numpy as np


class KNNClassifier(Classifier):
    def __init__(
        self,
        labeledDataset: List[LabeledPoint],
        trainLen: float = 0.7,
        positiveLabel: NDArray[np.int32] = np.array([0, 1]),
        negativeLabel: NDArray[np.int32] = np.array([-1]),
        k: int = 5,
        maxK: int = 100,
        optimalK: bool = True,
    ) -> None:
        super().__init__(labeledDataset, trainLen, positiveLabel, negativeLabel)

        errorAssert(optimalK or ((k is not None) and (k > 0)),
                    "Invalid k parameter.")

        errorAssert((maxK is None) or (maxK > 0), "Invalid max k parameter.")

        self.maxK: int = np.inf if (maxK is None) else maxK
        self.KDTree: KDTree = None
        self.k: int = k
        self.optimalK: bool = optimalK

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid point dataset.")

        self.KDTree = KDTree(dataset)

    def predict(self, point: Point) -> int:
        KNN = self.KDTree.kNearestNeighbors(point, self.k)

        PCount: int = 0
        NCount: int = 0

        for neighbor in KNN:
            if(neighbor[0].getLabel() in self.negativeLabel):
                NCount += 1
            elif(neighbor[0].getLabel() in self.positiveLabel):
                PCount += 1

        if(PCount >= NCount):
            return self.positiveLabel[0]
        else:
            return self.negativeLabel[0]

    def findOptimalK(self) -> None:
        bestF1 = -1
        bestK = 0

        sqrtLen: np.float32 = np.sqrt(len(self.trainSet))
        rangeLen: int = int(np.min(np.array([sqrtLen, self.maxK])))

        for k in range(1, rangeLen):
            self.k = k
            evaluation = self.crossValidation()

            meanEvaluation = evaluation.mean()

            if(meanEvaluation["F1"] > bestF1):
                bestF1 = meanEvaluation["F1"]
                bestK = k

        self.k = bestK

    def run(self) -> Dict:
        self.splitDataset()

        if(self.optimalK):
            self.findOptimalK()

        crossValidationMetrics = self.crossValidation()

        self.trainModel(self.trainSet)
        testConfusionMatrix, testMetrics = self.evaluateModel(self.testSet)

        return {
            "Cross Validation Metrics": crossValidationMetrics,
            "Test Metrics": testMetrics,
            "Test Confusion Matrix": testConfusionMatrix
        }
