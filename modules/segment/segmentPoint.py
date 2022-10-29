from __future__ import annotations
from ..point import Point
from .segment import Segment
from utils.exception import errorAssert


class SegmentPoint(Point):
    def __init__(self, segment: Segment, index: int) -> None:
        errorAssert(segment is not None, "Invalid segment.")
        errorAssert((index == 0) or (index == 1), "Invalid index.")

        self.__segment = segment
        self.__index = index
        super().__init__(self.__segment.getPointCoordinates(index))

    def getSegment(self) -> Segment:
        return self.__segment

    def getIndex(self) -> int:
        return self.__index

    def getPosition(self, coordinate: int) -> int:
        errorAssert((coordinate > -1) and (coordinate <
                    self.__segment.getDim()), "Invalid coordinate.")

        return self.__segment.getPointOrder(self.__index, coordinate)

    def isLeftEndpoint(self, coordinate: int) -> bool:
        return self.getPosition(coordinate) == -1

    def isRightEndpoint(self, coordinate: int) -> bool:
        return self.getPosition(coordinate) == 1
