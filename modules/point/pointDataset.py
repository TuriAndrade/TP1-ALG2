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
        valueFilters: Tuple[str] = (" ", "\n", ",", "."),
        labelTranslation: Dict = None,
    ) -> None:
        errorAssert(metadataId is not None, "Invalid metadada id.")
        errorAssert(valueSeparator is not None, "Invalid value separator.")

        self.metadataId: str = metadataId
        self.valueSeparator: str = valueSeparator
        self.dim: int = None
        self.labeledPoints: List[LabeledPoint] = []
        self.labelTranslation = labelTranslation
        self.valueFilters = valueFilters

        try:
            with open(path, 'r') as file:
                for line in file.readlines():
                    self.handleLine(line)

        except:
            throwException("Error reading dataset file.")

    def handleLine(self, line: str) -> None:
        if(not line.startswith(self.metadataId)):
            values = line.split(self.valueSeparator)

            if(self.dim is None):
                self.dim = (len(values) - 1)

            errorAssert(len(values) == (self.dim + 1),
                        "Invalid sample in file.")

            coordinates: List[float] = np.zeros(self.dim)

            for i in range(self.dim):
                value = values[i]

                if((self.valueFilters is not None) and (value.startswith(self.valueFilters))):
                    value = value[1:]

                if((self.valueFilters is not None) and (value.endswith(self.valueFilters))):
                    value = value[:-1]

                try:
                    coordinates[i] = float(value)
                except:
                    throwException("Values must be real numbers.")

            label: str = values[-1]

            if((self.valueFilters is not None) and (label.startswith(self.valueFilters))):
                label = label[1:]

            if((self.valueFilters is not None) and (label.endswith(self.valueFilters))):
                label = label[:-1]

            if(self.labelTranslation):
                errorAssert(
                    self.labelTranslation[label] is not None, "Invalid label.")
                label = self.labelTranslation[label]

            try:
                label = float(label)
            except:
                throwException("Labels must be real numbers.")

            point = LabeledPoint(coordinates, label)

            self.labeledPoints.append(point)

    def getPoints(self) -> None:
        return self.labeledPoints
