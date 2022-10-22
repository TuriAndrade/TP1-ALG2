from .stackNode import StackNode
from typing import Any, List


class Stack:
    def __init__(self) -> None:
        self.first: StackNode = None
        self.size: int = 0

    def push(self, data: Any) -> None:
        node = StackNode(data)
        node.setNext(self.first)
        self.first = node
        self.size += 1

    def pop(self) -> Any:
        if(self.size == 0):
            return None

        node = self.first
        self.first = self.first.getNext()
        self.size -= 1

        return node.getData()

    def isEmpty(self) -> bool:
        return self.size == 0

    def getSize(self) -> int:
        return self.size

    def toList(self) -> List[Any]:
        if(self.isEmpty()):
            return []

        stackToList: List[Any] = []
        while(not self.isEmpty()):
            data: Any = self.pop()
            stackToList.append(data)

        return stackToList

    def getNode(self, n) -> Any:
        i: int = 1
        current: StackNode = self.first

        while((i < n) and (current is not None)):
            current = current.getNext()
            i += 1

        return None if current is None else current.getData()
