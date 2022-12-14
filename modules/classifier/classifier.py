from __future__ import annotations
from ..point import LabeledPoint, Point
from utils.exception import errorAssert
from typing import List, Dict, Any
from random import sample
from numpy.typing import NDArray
import numpy as np
import pandas as pd


class Classifier:
    def __init__(
        self,
        labeledDataset: List[LabeledPoint],
        trainLen: float = 0.7,
        positiveLabel: NDArray[np.int32] = np.array([0, 1]),
        negativeLabel: NDArray[np.int32] = np.array([-1]),
        name: str = "Classifier",
        nFolds: int = 5,
        foldSizeTreshold=15
    ) -> None:
        errorAssert((labeledDataset is not None) and (
            len(labeledDataset) > 0), "Invalid point dataset.")
        errorAssert(trainLen is not None, "Invalid train set len.")
        errorAssert((positiveLabel is not None) and (
            positiveLabel.shape[0] > 0), "Invalid positive labels.")
        errorAssert((negativeLabel is not None) and (
            negativeLabel.shape[0] > 0), "Invalid negative labels.")
        errorAssert((name is not None) and (len(name) > 0), "Invalid name.")
        errorAssert((nFolds is not None) and (
            nFolds > 0), "Invalid number of folds.")
        errorAssert((foldSizeTreshold is not None) and (
            foldSizeTreshold > 0), "Invalid fold size treshold.")

        self._labeledDataset: List[LabeledPoint] = labeledDataset

        self._trainLen = int(len(labeledDataset) * trainLen)
        self._testLen = (len(labeledDataset) - self._trainLen)

        self._trainSet: List[LabeledPoint] = None
        self._testSet: List[LabeledPoint] = None

        self._positiveLabel = positiveLabel
        self._negativeLabel = negativeLabel

        self._name: str = name

        self._foldSizeTreshold = foldSizeTreshold

        self._nFolds = nFolds

    def splitDataset(self) -> None:
        shuffledDataset: List[LabeledPoint] = sample(
            self._labeledDataset, k=len(self._labeledDataset))

        self._trainSet = shuffledDataset[:self._trainLen]
        self._testSet = shuffledDataset[self._trainLen:]

    def computePrecision(self, confusionMatrix: NDArray[np.int32]) -> float:
        try:
            precision: float = confusionMatrix[0][0] / \
                (confusionMatrix[0][0] + confusionMatrix[0][1])
        except:
            precision = np.nan

        return precision

    def computeRecall(self, confusionMatrix: NDArray[np.int32]) -> float:
        try:
            recall: float = confusionMatrix[0][0] / \
                (confusionMatrix[0][0] + confusionMatrix[1][0])
        except:
            recall = np.nan

        return recall

    def computeF1(self, confusionMatrix: NDArray[np.int32]) -> float:
        try:
            precision: float = self.computePrecision(confusionMatrix)
            recall: float = self.computePrecision(confusionMatrix)

            f1 = (2*precision*recall)/(precision + recall)
        except:
            f1 = np.nan

        return f1

    def computeAccuracy(self, confusionMatrix: NDArray[np.int32]) -> float:
        try:
            accuracy = (confusionMatrix[0][0] + confusionMatrix[1][1]) / \
                (confusionMatrix[0][0] + confusionMatrix[1][1] +
                 confusionMatrix[0][1] + confusionMatrix[1][0])
        except:
            accuracy = np.nan

        return accuracy

    def splitFolds(self, k: int) -> List[Dict]:
        errorAssert(k > 1, "Number of folds must be greater than 1.")

        shuffledDataset: List[LabeledPoint] = sample(
            self._trainSet, k=len(self._trainSet))

        foldSize: int = (len(shuffledDataset) // k)

        folds: List[Dict] = []

        rangeSize = foldSize * k
        for i in range(0, rangeSize, foldSize):
            testSamples = shuffledDataset[i:(i+foldSize)]

            if ((len(testSamples) >= self._foldSizeTreshold) or (len(testSamples) >= foldSize)):
                trainSamples = shuffledDataset[:i] + \
                    shuffledDataset[(i+foldSize):]

                folds.append({
                    "Train": trainSamples,
                    "Validation": testSamples
                })

        return folds

    def crossValidation(self, k: int = 5) -> None:
        trainFolds: List[Dict] = self.splitFolds(k)

        evaluation = pd.DataFrame()

        for fold in trainFolds:
            self.trainModel(fold["Train"])

            results = self.evaluateModel(fold["Validation"])[1]

            evaluation = pd.concat([evaluation, results], ignore_index=True)

        return evaluation

    def evaluateModel(self, dataset: List[LabeledPoint]) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid point dataset.")

        TP: int = 0
        FP: int = 0
        FN: int = 0
        TN: int = 0

        for point in dataset:
            labelTrue = point.getLabel()
            labelPred = self.predict(point)

            if (np.isin(labelPred, self._negativeLabel)):
                if (np.isin(labelTrue, self._negativeLabel)):
                    TN += 1
                elif (np.isin(labelTrue, self._positiveLabel)):
                    FN += 1
            elif (np.isin(labelPred, self._positiveLabel)):
                if (np.isin(labelTrue, self._positiveLabel)):
                    TP += 1
                elif (np.isin(labelTrue, self._negativeLabel)):
                    FP += 1

        confusionMatrix: NDArray[np.int32] = np.array([[TP, FP],
                                                      [FN, TN]])

        metrics = pd.DataFrame({
            "Precision": [self.computePrecision(confusionMatrix)],
            "Recall": [self.computeRecall(confusionMatrix)],
            "F1": [self.computeF1(confusionMatrix)],
            "Accuracy": [self.computeAccuracy(confusionMatrix)]
        })

        return confusionMatrix, metrics

    @staticmethod
    def buildInstance(**kwargs) -> Any:
        pass

    def getName(self) -> str:
        return self._name

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        pass

    def predict(self, point: Point) -> int:
        pass

    def run(self) -> Dict:
        self.splitDataset()

        crossValidationMetrics = self.crossValidation(k=self._nFolds)

        self.trainModel(self._trainSet)
        testConfusionMatrix, testMetrics = self.evaluateModel(self._testSet)

        return {
            "Cross Validation Metrics": crossValidationMetrics,
            "Test Metrics": testMetrics,
            "Test Confusion Matrix": testConfusionMatrix
        }
