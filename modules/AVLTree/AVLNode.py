from __future__ import annotations
from utils.exception import errorAssert
from typing import Any


class AVLNode:
    def __init__(self, key: Any) -> None:
        errorAssert(key is not None, "Invalid node key.")

        self.key: Any = key
        self.left: AVLNode = None
        self.right: AVLNode = None
        self.height: int = 1

    def setLeft(self, left: AVLNode) -> None:
        self.left = left

    def getLeft(self) -> AVLNode:
        return self.left

    def setRight(self, right: AVLNode) -> None:
        self.right = right

    def getRight(self) -> AVLNode:
        return self.right

    def setHeight(self, height: int) -> None:
        errorAssert(height > 0, "Invalid height.")
        self.height = height

    def getHeight(self) -> int:
        return self.height

    def setKey(self, key: Any) -> None:
        errorAssert(key is not None, "Invalid node key.")
        self.key: Any = key

    def getKey(self) -> Any:
        return self.key

    def getLeftKey(self) -> Any:
        if(self.left is None):
            return None
        else:
            return self.left.getKey()

    def getRightKey(self) -> Any:
        if(self.right is None):
            return None
        else:
            return self.right.getKey()
