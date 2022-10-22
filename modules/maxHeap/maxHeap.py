from utils.exception import errorAssert
from typing import List, Tuple, Any


class MaxHeap:
    def __init__(self, capacity: int) -> None:
        errorAssert(capacity > 0, "Invalid capacity.")

        self.capacity: int = capacity
        self.size: int = 0
        self.heap: List[Tuple[Any, Any]] = [None] * self.capacity

    def parent(self, position: int) -> int:
        return (position - 1)//2

    def leftChild(self, position: int) -> int:
        return (2*position) + 1

    def rightChild(self, position: int) -> int:
        return (2*position) + 2

    def insert(self, node: Tuple[Any, Any]) -> None:
        if(self.size < self.capacity):
            self.size += 1
            position: int = self.size - 1
            self.heap[position] = node

            while (position != 0 and self.heap[self.parent(position)][1] < self.heap[position][1]):
                (self.heap[position], self.heap[self.parent(position)]) = (
                    self.heap[self.parent(position)], self.heap[position])

                position = self.parent(position)

        elif(node[1] < self.heap[0][1]):
            self.heap[0] = node
            self.heapify(0, self.size)

    def decreaseKey(self, position: int, newNode: Any) -> None:
        errorAssert(position < self.capacity, "Invalid position.")

        self.heap[position] = newNode

        while (position != 0 and self.heap[self.parent(position)][1] < self.heap[position][1]):
            (self.heap[position], self.heap[self.parent(position)]) = (
                self.heap[self.parent(position)], self.heap[position])

            position = self.parent(position)

    def heapify(self, position: int, size: int) -> None:
        left: int = self.leftChild(position)
        right: int = self.rightChild(position)

        greatest: int = position

        if(left < size and self.heap[left][1] > self.heap[greatest][1]):
            greatest = left

        if(right < size and self.heap[right][1] > self.heap[greatest][1]):
            greatest = right

        if(greatest != position):
            (self.heap[position], self.heap[greatest]) = (
                self.heap[greatest], self.heap[position])

            self.heapify(greatest, size)

    def build(self) -> None:
        startIndex: int = (self.size / 2) - 1

        for i in range(startIndex, -1, -1):
            self.heapify(i, self.size)

    def getMax(self) -> Tuple[Any, Any]:
        errorAssert(self.size > 0, "Heap vazio.")
        return self.heap[0]

    def getSize(self) -> int:
        return self.size

    def heapSort(self) -> List[Tuple[Any, Any]]:
        for i in range(self.size - 1, -1, -1):
            (self.heap[0], self.heap[i]) = (self.heap[i], self.heap[0])
            self.heapify(0, i)

        return self.heap
