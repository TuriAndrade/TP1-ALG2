from __future__ import annotations
from ..point import LabeledPoint
from utils.exception import errorAssert, throwWarning
import pandas as pd
from random import choices
from typing import List, Any


class ClassifiersComparison:
    def __init__(
        self,
        dataset: List[LabeledPoint],
        classifiers=List[Any],
        sampleSize=100,
        nSamples=100,
        allowSampleError=True,
    ) -> None:
        errorAssert((dataset is not None) and (
            len(dataset) > 0), "Invalid dataset.")
        errorAssert((classifiers is not None) and (
            len(classifiers) > 1), "There must be at least 2 classifiers to compare.")
        errorAssert(sampleSize > 0, "Invalid sample size.")
        errorAssert(nSamples > 1, "Invalid sample number.")

        self.__sampleSize = sampleSize
        self.__nSamples = nSamples
        self.__dataset = dataset
        self.__classifiers = classifiers
        self.__allowSampleError = allowSampleError

    def compare2(self, classifier1: Any, classifier2: Any) -> pd.DataFrame:
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
        results: pd.DataFrame = pd.DataFrame()

        for i in range(len(self.__classifiers)):
            for j in range(len(self.__classifiers)):
                if (i != j):
                    comparison: pd.DataFrame = self.compare2(
                        self.__classifiers[i], self.__classifiers[j])

                    results = pd.concat(
                        [results, comparison], ignore_index=True)

        return results
