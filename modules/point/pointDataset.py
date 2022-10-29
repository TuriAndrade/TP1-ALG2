from .labeledPoint import LabeledPoint
from utils.exception import throwException, errorAssert
from typing import List, Tuple, Dict
import numpy as np


class PointDataset:
    def __init__(
        self,
        path: str,
        metadataId: str = "@",
        valueSeparator: str = ",",
        filters: Tuple[str] = (" ", "\n", ",", "."),
        valueTranslation: Dict = None,
        labelTranslation: Dict = None,
    ) -> None:
        errorAssert(metadataId is not None, "Invalid metadada id.")
        errorAssert(valueSeparator is not None, "Invalid value separator.")

        self.__metadataId: str = metadataId
        self.__valueSeparator: str = valueSeparator
        self.__dim: int = None
        self.__labeledPoints: List[LabeledPoint] = []
        self.__filters = filters
        self.__labelTranslation = labelTranslation
        self.__valueTranslation = valueTranslation

        try:
            with open(path, 'r') as file:
                for line in file.readlines():
                    self.handleLine(line)

        except:
            throwException("Error reading dataset file.")

    def handleLine(self, line: str) -> None:
        if (not line.startswith(self.__metadataId)):
            entries = line.split(self.__valueSeparator)

            if (self.__dim is None):
                self.__dim = (len(entries) - 1)

            errorAssert(len(entries) == (self.__dim + 1),
                        "Invalid sample in file.")

            coordinates: List[float] = np.zeros(self.__dim)

            for i in range(self.__dim):
                value = entries[i]

                if ((self.__filters is not None) and (value.startswith(self.__filters))):
                    value = value[1:]

                if ((self.__filters is not None) and (value.endswith(self.__filters))):
                    value = value[:-1]

                if (
                    (self.__valueTranslation) and
                    (value in self.__valueTranslation)
                ):
                    value = self.__valueTranslation[value]

                try:
                    coordinates[i] = float(value)
                except:
                    throwException("Values must be real numbers.")

            label: str = entries[-1]

            if ((self.__filters is not None) and (label.startswith(self.__filters))):
                label = label[1:]

            if ((self.__filters is not None) and (label.endswith(self.__filters))):
                label = label[:-1]

            if (
                (self.__labelTranslation) and
                (label in self.__labelTranslation)
            ):
                label = self.__labelTranslation[label]

            try:
                label = float(label)
            except:
                throwException("Labels must be real numbers.")

            point = LabeledPoint(coordinates, label)

            self.__labeledPoints.append(point)

    def getPoints(self) -> None:
        return self.__labeledPoints
