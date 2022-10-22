from ..point import Point
from ..maxHeap import MaxHeap
from ..quicksort import quicksort
from .KDNode import KDNode
from utils.exception import errorAssert
from typing import List, Tuple
from numpy.typing import NDArray
import numpy as np


class KDTree:
    def __init__(self, points: List[Point]) -> None:
        errorAssert((points is not None) and (
            len(points) > 0), "Invalid number of points.")

        self.points: List[Point] = list(set(points))
        self.dim: int = self.points[0].getDim()
        self.nPoints = len(self.points)
        self.height: int = 0
        self.root: KDNode = self.build(
            self.points, 0, np.array([[-np.inf, np.inf]] * self.dim))

    def partitionMedian(self, points: List[Point], coordinate: int) -> Tuple[Point, List[Point], List[Point]]:
        nPoints: int = len(points)

        errorAssert(nPoints > 0, "Invalid number of points.")

        quicksort(
            points, 0, nPoints - 1,
            Point.buildPointsComparison(coordinate)
        )

        if(nPoints == 1):
            return points[0], [], []
        elif(nPoints == 2):
            return points[1], [points[0]], []
        else:

            median: int = nPoints // 2

            return points[median], points[:median], points[(median + 1):]

    def build(self, points: List[Point], depth: int, boundingBox: NDArray[np.float32]) -> KDNode:
        self.height = max(self.height, depth)
        currentNPoints = len(points)

        if(currentNPoints == 0):
            return None

        elif(currentNPoints == 1):
            currentNode: KDNode = KDNode(points[0])
            currentNode.setBoundingBox(boundingBox)

            return currentNode
        else:
            coordinate: int = depth % self.dim
            partition: Tuple[Point, List[Point], List[Point]] = \
                self.partitionMedian(points, coordinate)

            median = partition[0]
            leftPoints = partition[1]
            rightPoints = partition[2]

            currentNode: KDNode = KDNode(median)
            currentNode.setBoundingBox(boundingBox)

            updateBoundingBoxLeft = np.copy(boundingBox)
            updateBoundingBoxLeft[coordinate][1] = median.coordinates[coordinate]

            updateBoundingBoxRight = np.copy(boundingBox)
            updateBoundingBoxRight[coordinate][0] = median.coordinates[coordinate]

            currentNode.setLeft(
                self.build(
                    leftPoints, depth + 1, updateBoundingBoxLeft)
            )
            currentNode.setRight(
                self.build(
                    rightPoints, depth + 1, updateBoundingBoxRight)
            )

            return currentNode

    def kNearestNeighborsHelper(
        self, root: KDNode, target: Point, depth: int, k: int, maxHeap: MaxHeap
    ) -> List[Tuple[Point, float]]:

        if(root is not None):
            coordinate: int = depth % self.dim

            if(target.getCoordinate(coordinate) < root.getPointCoordinate(coordinate)):
                nextBranch: KDNode = root.getLeft()
                siblingBranch: KDNode = root.getRight()
            else:
                nextBranch = root.getRight()
                siblingBranch = root.getLeft()

            self.kNearestNeighborsHelper(
                nextBranch, target, depth + 1, k, maxHeap)

            rootDist = target.computeDist(root.getPoint())
            maxHeap.insert((root.getPoint(), rootDist))

            splitDist: float = target.computeDist(root.getPoint(), coordinate)

            if((depth + 1) < (k - maxHeap.getSize()) or maxHeap.getMax()[1] >= splitDist):
                self.kNearestNeighborsHelper(
                    siblingBranch, target, depth + 1, k, maxHeap)

    def kNearestNeighbors(self, target: Point, k: int) -> List[Tuple[Point, float]]:
        maxHeap: MaxHeap = MaxHeap(k)

        self.kNearestNeighborsHelper(self.root, target, 0, k, maxHeap)

        KNN = maxHeap.heapSort()

        return KNN[:maxHeap.getSize()]

    def computeDistsAux(self, root: KDNode, target: Point, dists: List[Tuple[Point, float]]) -> None:
        if(root is not None):
            dist = target.computeDist(root.getPoint())
            dists.append((root.getPoint(), dist))
            self.computeDistsAux(root.getLeft(), target, dists)
            self.computeDistsAux(root.getRight(), target, dists)

    def computeDists(self, target: Point) -> List[Tuple[Point, float]]:
        dists: List[Tuple[Point, float]] = []

        self.computeDistsAux(self.root, target, dists)

        return dists

    def printHelper(self, node: KDNode) -> None:
        if(node is not None):
            print("Point: ", node.getPointCoordinates())
            print("Bounding Box:\n", node.getBoundingBox())

            left = node.getLeft()
            if(left is not None):
                print("Left: ", left.getPointCoordinates())

            right = node.getRight()
            if(right is not None):
                print("Right: ", right.getPointCoordinates())

            print()
            self.printHelper(left)
            self.printHelper(right)

    def print(self) -> None:
        self.printHelper(self.root)

    def reportSubtreeHelper(self, root: KDNode, reportedNodes: List[KDNode]) -> None:
        if(root is not None):
            reportedNodes.append(root)
            self.reportSubtreeHelper(root.getLeft(), reportedNodes)
            self.reportSubtreeHelper(root.getRight(), reportedNodes)

    def reportSubtree(self, node: KDNode) -> List[KDNode]:
        reportedNodes: List[KDNode] = []
        self.reportSubtree(node, reportedNodes)

        return reportedNodes

    def intervalContainsRegion(self, interval: NDArray[np.float32], node: KDNode) -> bool:
        for i in range(self.dim):

            boundingBox: NDArray[np.float32] = node.getBoundingBox()
            if(interval[i][0] > boundingBox[i][0] or interval[i][1] < boundingBox[i][1]):
                return False

        return True

    def intervalIntersectsRegion(self, interval: NDArray[np.float32], node: KDNode) -> bool:
        for i in range(self.dim):

            boundingBox: NDArray[np.float32] = node.getBoundingBox()
            if(not (interval[i][1] < boundingBox[i][0] or interval[i][0] > boundingBox[i][1])):
                return True

        return False

    def intervalContainsNode(self, interval: NDArray[np.float32], node: KDNode) -> bool:
        for i in range(self.dim):

            pointCoordinates: NDArray[np.float32] = node.getPointCoordinates()
            if(interval[i][0] > pointCoordinates[i] or interval[i][1] < pointCoordinates[i]):
                return False

        return True

    def searchRangeHelper(
        self, root: KDNode, searchInterval: NDArray[np.float32], reportedNodes: List[KDNode]
    ) -> None:
        if(root is not None):
            if(self.intervalContainsRegion(searchInterval, root)):
                self.reportSubtreeHelper(root, reportedNodes)

            else:
                if(self.intervalContainsNode(searchInterval, root)):
                    reportedNodes.append(root)

                left = root.getLeft()
                if(left is not None and self.intervalIntersectsRegion(searchInterval, left)):
                    self.searchRangeHelper(
                        left, searchInterval, reportedNodes
                    )

                right = root.getRight()
                if(right is not None and self.intervalIntersectsRegion(searchInterval, right)):
                    self.searchRangeHelper(
                        right, searchInterval, reportedNodes
                    )

    def searchRange(self, searchInterval: NDArray[np.float32]) -> List[KDNode]:
        reportedNodes: List[KDNode] = []
        self.searchRangeHelper(self.root, searchInterval, reportedNodes)

        return reportedNodes

    @staticmethod
    def closestPointsSubsets(subset1: List[Point], subset2: List[Point]) -> Tuple[Point, Point]:
        l1 = len(subset1)
        l2 = len(subset2)

        errorAssert((l1 > 0) and (l2 > 0), "Invalid point subsets.")

        if(l1 < l2):
            pointsTree = KDTree(subset1)
            pointsList = subset2
        else:
            pointsTree = KDTree(subset2)
            pointsList = subset1

        [(NN, dist)] = pointsTree.kNearestNeighbors(pointsList[0], 1)
        closestPoints = [(pointsList[0], NN), dist]

        for i in range(1, len(pointsList)):
            [(NN, dist)] = pointsTree.kNearestNeighbors(pointsList[i], 1)

            if(dist < closestPoints[1]):
                closestPoints = [(pointsList[i], NN), dist]

        return closestPoints
