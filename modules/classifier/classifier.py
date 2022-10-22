from ..point import LabeledPoint, Point
from utils.exception import errorAssert
from typing import List, Dict
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
        negativeLabel: NDArray[np.int32] = np.array([-1])
    ) -> None:
        errorAssert((labeledDataset is not None) and (
            len(labeledDataset) > 0), "Invalid point dataset.")
        errorAssert(trainLen is not None, "Invalid train set len.")
        errorAssert((positiveLabel is not None) and (
            positiveLabel.shape[0] > 0), "Invalid positive labels.")
        errorAssert((negativeLabel is not None) and (
            negativeLabel.shape[0] > 0), "Invalid negative labels.")

        self.labeledDataset: List[LabeledPoint] = labeledDataset

        self.trainLen = int(len(labeledDataset) * trainLen)
        self.testLen = (len(labeledDataset) - self.trainLen)

        self.trainSet: List[LabeledPoint] = None
        self.testSet: List[LabeledPoint] = None

        self.positiveLabel = positiveLabel
        self.negativeLabel = negativeLabel

    def splitDataset(self) -> None:
        shuffledDataset: List[LabeledPoint] = sample(
            self.labeledDataset, k=len(self.labeledDataset))

        self.trainSet = shuffledDataset[:self.trainLen]
        self.testSet = shuffledDataset[self.trainLen:]

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
            self.trainSet, k=len(self.trainSet))

        foldSize: int = (len(shuffledDataset) // k)

        folds: List[Dict] = []

        rangeSize = foldSize * k
        for i in range(0, rangeSize, foldSize):
            testSamples = shuffledDataset[i:(i+foldSize)]
            trainSamples = shuffledDataset[:i] + shuffledDataset[(i+foldSize):]

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

            if(np.isin(labelPred, self.negativeLabel)):
                if(np.isin(labelTrue, self.negativeLabel)):
                    TN += 1
                elif(np.isin(labelTrue, self.positiveLabel)):
                    FN += 1
            elif(np.isin(labelPred, self.positiveLabel)):
                if(np.isin(labelTrue, self.positiveLabel)):
                    TP += 1
                elif(np.isin(labelTrue, self.negativeLabel)):
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

    def trainModel(self, dataset: List[LabeledPoint]) -> None:
        pass

    def predict(self, point: Point) -> int:
        pass

    def run(self) -> Dict:
        self.splitDataset()

        crossValidationMetrics = self.crossValidation()

        self.trainModel(self.trainSet)
        testConfusionMatrix, testMetrics = self.evaluateModel(self.testSet)

        return {
            "Cross Validation Metrics": crossValidationMetrics,
            "Test Metrics": testMetrics,
            "Test Confusion Matrix": testConfusionMatrix
        }
