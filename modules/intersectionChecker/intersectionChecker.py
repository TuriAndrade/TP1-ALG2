from ..segment import Segment, SegmentPoint
from ..point import Point
from ..AVLTree import AVLTree
from ..quicksort import quicksort
from utils.exception.exception import errorAssert
from typing import List


class IntersectionChecker:
    def __init__(self, segments: List[Segment], coordinate1: int, coordinate2: int):
        errorAssert((segments is not None) and (
            len(segments) > 1), "Invalid number of segments.")
        errorAssert((coordinate1 is not None) and (
            coordinate2 is not None), "Invalid coordinates.")
        errorAssert((coordinate1 < segments[0].getDim()) and (
            coordinate2 < segments[0].getDim()), "Invalid coordinates.")

        self.__segments: List[Segment] = segments
        self.__points: List[SegmentPoint] = []

        for segment in self.__segments:
            self.__points.append(SegmentPoint(segment, 0))
            self.__points.append(SegmentPoint(segment, 1))

        self.__coordinate1 = coordinate1
        self.__coordinate2 = coordinate2

        self.__sweepLineStatus = AVLTree()

    def run(self) -> bool:
        quicksort(self.__points, 0, len(self.__points) - 1,
                  Point.buildPointsComparison(self.__coordinate1, type='LE'))

        for point in self.__points:
            if (point.isLeftEndpoint(self.__coordinate1)):
                self.__sweepLineStatus.insert(
                    point, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW')
                )

                abovePoint: SegmentPoint = self.__sweepLineStatus.successor(
                    point, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW'))
                belowPoint: SegmentPoint = self.__sweepLineStatus.predecessor(
                    point, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW'))

                aboveSegment: Segment = None if not abovePoint else abovePoint.getSegment()
                belowSegment: Segment = None if not belowPoint else belowPoint.getSegment()

                currentSegment: Segment = point.getSegment()

                if (
                    (aboveSegment is not None) and
                    (Segment.intersects2D(self.__coordinate1,
                     self.__coordinate2, aboveSegment, currentSegment))
                ):
                    return True

                elif (
                    (belowSegment is not None) and
                    (Segment.intersects2D(self.__coordinate1,
                     self.__coordinate2, belowSegment, currentSegment))
                ):
                    return True

            if (point.isRightEndpoint(self.__coordinate1)):
                abovePoint: SegmentPoint = self.__sweepLineStatus.successor(
                    point, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW'))
                belowPoint: SegmentPoint = self.__sweepLineStatus.predecessor(
                    point, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW'))

                aboveSegment: Segment = None if not abovePoint else abovePoint.getSegment()
                belowSegment: Segment = None if not belowPoint else belowPoint.getSegment()

                currentSegment: Segment = point.getSegment()

                if (
                    (aboveSegment is not None) and
                    (belowSegment is not None) and
                    (Segment.intersects2D(self.__coordinate1,
                     self.__coordinate2, aboveSegment, belowSegment))
                ):
                    return True

                leftEndpoint: Point = currentSegment.getLeftEndpoint(
                    self.__coordinate1)

                self.__sweepLineStatus.delete(
                    leftEndpoint, Point.buildPointsComparison(
                        self.__coordinate2, type='RAW')
                )

        return False
