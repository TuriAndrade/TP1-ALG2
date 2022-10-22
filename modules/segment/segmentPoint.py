from __future__ import annotations
from ..point import Point
from .segment import Segment
from utils.exception import errorAssert


class SegmentPoint(Point):
    def __init__(self, segment: Segment, index: int, coordinate: int) -> None:
        errorAssert(segment is not None, "Invalid segment.")
        errorAssert((index == 0) or (index == 1), "Invalid index.")
        errorAssert((coordinate > -1) and (coordinate <
                    segment.getDim()), "Invalid coordinate.")

        self.segment = segment
        self.position = segment.getPointOrder(index, coordinate)

        super().__init__(self.segment.getPointCoordinates(index))

    def getSegment(self) -> Segment:
        return self.segment

    def getIndex(self) -> int:
        return self.index

    def getPosition(self) -> int:
        return self.position

    def isLeftEndpoint(self) -> bool:
        return self.position == -1

    def isRightEndpoint(self) -> bool:
        return self.position == 1
