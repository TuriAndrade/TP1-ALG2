from .stackNode import StackNode
from typing import Any, List


class Stack:
    def __init__(self) -> None:
        self.__first: StackNode = None
        self.__size: int = 0

    def push(self, data: Any) -> None:
        node = StackNode(data)
        node.setNext(self.__first)
        self.__first = node
        self.__size += 1

    def pop(self) -> Any:
        if (self.__size == 0):
            return None

        node = self.__first
        self.__first = self.__first.getNext()
        self.__size -= 1

        return node.getData()

    def isEmpty(self) -> bool:
        return self.__size == 0

    def getSize(self) -> int:
        return self.__size

    def toList(self) -> List[Any]:
        if (self.isEmpty()):
            return []

        stackToList: List[Any] = []
        while (not self.isEmpty()):
            data: Any = self.pop()
            stackToList.append(data)

        return stackToList

    def getNode(self, n) -> Any:
        i: int = 1
        current: StackNode = self.__first

        while ((i < n) and (current is not None)):
            current = current.getNext()
            i += 1

        return None if current is None else current.getData()
