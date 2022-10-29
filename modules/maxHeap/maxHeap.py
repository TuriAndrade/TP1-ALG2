from utils.exception import errorAssert
from typing import List, Tuple, Any


class MaxHeap:
    def __init__(self, capacity: int) -> None:
        errorAssert(capacity > 0, "Invalid capacity.")

        self.__capacity: int = capacity
        self.__size: int = 0
        self.__heap: List[Tuple[Any, Any]] = [None] * self.__capacity

    def parent(self, position: int) -> int:
        return (position - 1)//2

    def leftChild(self, position: int) -> int:
        return (2*position) + 1

    def rightChild(self, position: int) -> int:
        return (2*position) + 2

    def insert(self, node: Tuple[Any, Any]) -> None:
        if (self.__size < self.__capacity):
            self.__size += 1
            position: int = self.__size - 1
            self.__heap[position] = node

            while (position != 0 and self.__heap[self.parent(position)][1] < self.__heap[position][1]):
                (self.__heap[position], self.__heap[self.parent(position)]) = (
                    self.__heap[self.parent(position)], self.__heap[position])

                position = self.parent(position)

        elif (node[1] < self.__heap[0][1]):
            self.__heap[0] = node
            self.heapify(0, self.__size)

    def decreaseKey(self, position: int, newNode: Any) -> None:
        errorAssert(position < self.__capacity, "Invalid position.")

        self.__heap[position] = newNode

        while (position != 0 and self.__heap[self.parent(position)][1] < self.__heap[position][1]):
            (self.__heap[position], self.__heap[self.parent(position)]) = (
                self.__heap[self.parent(position)], self.__heap[position])

            position = self.parent(position)

    def heapify(self, position: int, size: int) -> None:
        left: int = self.leftChild(position)
        right: int = self.rightChild(position)

        greatest: int = position

        if (left < size and self.__heap[left][1] > self.__heap[greatest][1]):
            greatest = left

        if (right < size and self.__heap[right][1] > self.__heap[greatest][1]):
            greatest = right

        if (greatest != position):
            (self.__heap[position], self.__heap[greatest]) = (
                self.__heap[greatest], self.__heap[position])

            self.heapify(greatest, size)

    def build(self) -> None:
        startIndex: int = (self.__size / 2) - 1

        for i in range(startIndex, -1, -1):
            self.heapify(i, self.__size)

    def getMax(self) -> Tuple[Any, Any]:
        errorAssert(self.__size > 0, "Heap vazio.")
        return self.__heap[0]

    def getSize(self) -> int:
        return self.__size

    def heapSort(self) -> List[Tuple[Any, Any]]:
        for i in range(self.__size - 1, -1, -1):
            (self.__heap[0], self.__heap[i]) = (self.__heap[i], self.__heap[0])
            self.heapify(0, i)

        return self.__heap
