from ..segment import Segment, SegmentPoint
from ..point import Point
from ..line import Line2D
from ..AVLTree import AVLTree
from ..quicksort import quicksort
from utils.exception.exception import errorAssert
from typing import List, Any


class IntersectionChecker:
    def __init__(self, segments: List[Segment], coordinate1: int, coordinate2: int):
        errorAssert((segments is not None) and (
            len(segments) > 1), "Invalid number of segments.")
        errorAssert((coordinate1 is not None) and (
            coordinate2 is not None), "Invalid coordinates.")
        errorAssert((coordinate1 < segments[0].getDim()) and (
            coordinate2 < segments[0].getDim()), "Invalid coordinates.")

        self.segments: List[Segment] = segments
        self.points: List[SegmentPoint] = []

        for segment in self.segments:
            self.points.append(SegmentPoint(segment, 0, 0))
            self.points.append(SegmentPoint(segment, 1, 0))

        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2

        self.sweepLineStatus = AVLTree()

    def buildSweepLineComparsion(self, point: Point) -> Any:
        errorAssert(point is not None, "Invalid point.")

        def compare(segment1: Segment, segment2: Segment) -> int:
            errorAssert(segment1.getDim() ==
                        segment2.getDim(), "Invalid segments.")
            errorAssert(point.getDim() == segment1.getDim(), "Invalid point.")

            x = point.getCoordinate(self.coordinate1)

            line1 = Line2D(
                self.coordinate1, self.coordinate2,
                point1=segment1.getPoint(0), point2=segment1.getPoint(1)
            )
            y1 = line1.equation(x)

            line2 = Line2D(
                self.coordinate1, self.coordinate2,
                point1=segment2.getPoint(0), point2=segment2.getPoint(1)
            )
            y2 = line2.equation(x)

            if(y1 < y2):
                return -1
            elif(y1 > y2):
                return 1
            elif(segment1 == segment2):
                return 0
            else:
                if(segment1.computeLength() < segment2.computeLength()):
                    return -1

                elif(segment1.computeLength() > segment2.computeLength()):
                    return 1

                else:
                    if(segment1.getPointCoordinate(0, self.coordinate1) < segment2.getPointCoordinate(0, self.coordinate1)):
                        return -1
                    elif(segment1.getPointCoordinate(0, self.coordinate1) > segment2.getPointCoordinate(0, self.coordinate1)):
                        return 1
                    elif(segment1.getPointCoordinate(1, self.coordinate1) < segment2.getPointCoordinate(1, self.coordinate1)):
                        return -1
                    elif(segment1.getPointCoordinate(1, self.coordinate1) > segment2.getPointCoordinate(1, self.coordinate1)):
                        return 1
                    elif(segment1.getPointCoordinate(0, self.coordinate2) < segment2.getPointCoordinate(0, self.coordinate2)):
                        return -1
                    elif(segment1.getPointCoordinate(0, self.coordinate2) > segment2.getPointCoordinate(0, self.coordinate2)):
                        return 1
                    elif(segment1.getPointCoordinate(1, self.coordinate2) < segment2.getPointCoordinate(1, self.coordinate2)):
                        return -1
                    else:
                        return 1

        return compare

    def run(self) -> bool:
        quicksort(self.points, 0, len(self.points) - 1,
                  Point.buildPointsComparison(self.coordinate1))

        for point in self.points:
            if(point.isLeftEndpoint()):
                segment = point.getSegment()

                self.sweepLineStatus.insert(
                    segment, self.buildSweepLineComparsion(point)
                )

                above: Segment = self.sweepLineStatus.successor(
                    segment, self.buildSweepLineComparsion(point))
                below: Segment = self.sweepLineStatus.predecessor(
                    segment, self.buildSweepLineComparsion(point))

                if(
                    (above is not None) and
                    (Segment.intersects2D(self.coordinate1,
                     self.coordinate2, above, segment))
                ):
                    return True

                elif(
                    (below is not None) and
                    (Segment.intersects2D(self.coordinate1,
                     self.coordinate2, below, segment))
                ):
                    return True

            if(point.isRightEndpoint()):
                segment = point.getSegment()

                above: Segment = self.sweepLineStatus.successor(
                    segment, self.buildSweepLineComparsion(point))
                below: Segment = self.sweepLineStatus.predecessor(
                    segment, self.buildSweepLineComparsion(point))

                if(
                    (above is not None) and
                    (below is not None) and
                    (Segment.intersects2D(self.coordinate1,
                     self.coordinate2, above, below))
                ):
                    return True

                self.sweepLineStatus.delete(
                    segment, self.buildSweepLineComparsion(point)
                )

        return False
