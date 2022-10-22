from __future__ import annotations
from utils.exception import errorAssert
from typing import Any


class StackNode:
    def __init__(self, data: Any):
        errorAssert(data is not None, "Invalid data for stack node.")
        self.data: Any = data
        self.next: StackNode = None

    def getNext(self) -> StackNode:
        return self.next

    def setNext(self, node: StackNode) -> None:
        self.next = node

    def getData(self) -> Any:
        return self.data

    def setData(self, data) -> Any:
        errorAssert(data is not None, "Invalid data for stack node.")
        self.data = data
