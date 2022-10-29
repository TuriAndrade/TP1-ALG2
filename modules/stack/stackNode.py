from __future__ import annotations
from utils.exception import errorAssert
from typing import Any


class StackNode:
    def __init__(self, data: Any):
        errorAssert(data is not None, "Invalid data for stack node.")
        self.__data: Any = data
        self.__next: StackNode = None

    def getNext(self) -> StackNode:
        return self.__next

    def setNext(self, node: StackNode) -> None:
        self.__next = node

    def getData(self) -> Any:
        return self.__data

    def setData(self, data) -> Any:
        errorAssert(data is not None, "Invalid data for stack node.")
        self.__data = data
