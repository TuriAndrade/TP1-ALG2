from __future__ import annotations
from ..point import LabeledPoint
from utils.exception import errorAssert, throwWarning
from random import choices
from typing import List, Any
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class ClassifiersComparison:
    def __init__(
        self,
        dataset: List[LabeledPoint],
        classifiers: List[Any],
        sampleSize: int = 100,
        nSamples: int = 100,
        allowSampleError: bool = True,
    ) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid dataset.")
        errorAssert((classifiers is not None) and (
            len(classifiers) > 1), "There must be at least 2 classifiers to compare.")
        errorAssert(sampleSize > 0, "Invalid sample size.")
        errorAssert(nSamples > 1, "Invalid sample number.")

        self.__sampleSize: int = sampleSize
        self.__nSamples: int = nSamples
        self.__dataset: List[LabeledPoint] = dataset
        self.__classifiers: List[Any] = classifiers
        self.__allowSampleError: bool = allowSampleError
        self.__results: pd.DataFrame = pd.DataFrame()

    def pairComparison(self, classifier1: Any, classifier2: Any) -> pd.DataFrame:
        meanDiff: pd.DataFrame = pd.DataFrame()

        for i in range(self.__nSamples):
            try:
                pointSample = choices(self.__dataset, k=self.__sampleSize)

                clf1 = classifier1(pointSample)
                clf2 = classifier2(pointSample)

                clf1Results = clf1.run()['Test Metrics']
                clf2Results = clf2.run()['Test Metrics']

                meanDiff = pd.concat([meanDiff, (clf1Results.mean() - clf2Results.mean())],
                                     ignore_index=True, axis=1)
            except Exception as e:
                if (self.__allowSampleError):
                    throwWarning(str(e))
                else:
                    raise e

        result: pd.DataFrame = meanDiff.transpose()

        result['Label'] = clf1.getName() + "/" + clf2.getName()

        return result

    def run(self) -> pd.DataFrame:
        for i in range(len(self.__classifiers)):
            for j in range(len(self.__classifiers)):
                if (i != j):
                    comparison: pd.DataFrame = self.pairComparison(
                        self.__classifiers[i], self.__classifiers[j])

                    self.__results = pd.concat(
                        [self.__results, comparison], ignore_index=True)

        return self.__results

    def plotPairComparison(self, label: str):
        errorAssert((label is not None) and (
            label in self.__results['Label'].values), "Invalid label.")

        comparisonDiff = self.__results[self.__results['Label'] == label]

        fig, ax = plt.subplots(2, 2, figsize=(16, 10))

        ax[0][0].hist(comparisonDiff[~np.isnan(comparisonDiff["Precision"])]
                      ["Precision"], bins=20, label="Precision mean difference", color='b')
        ax[0][0].legend()
        ax[0][0].axvline(x=0, color='r')

        ax[0][1].hist(comparisonDiff[~np.isnan(comparisonDiff["Recall"])]
                      ["Recall"], bins=20, label="Recall mean difference", color='b')
        ax[0][1].legend()
        ax[0][1].axvline(x=0, color='r')

        ax[1][0].hist(comparisonDiff[~np.isnan(comparisonDiff["F1"])]
                      ["F1"], bins=20, label="F1 mean difference", color='b')
        ax[1][0].legend()
        ax[1][0].axvline(x=0, color='r')

        ax[1][1].hist(comparisonDiff[~np.isnan(comparisonDiff["Accuracy"])]
                      ["Accuracy"], bins=20, label="Accuracy mean difference", color='b')
        ax[1][1].legend()
        ax[1][1].axvline(x=0, color='r')
