from __future__ import annotations
from utils.exception import errorAssert
from typing import Any


class AVLNode:
    def __init__(self, key: Any) -> None:
        errorAssert(key is not None, "Invalid node key.")

        self.__key: Any = key
        self.__left: AVLNode = None
        self.__right: AVLNode = None
        self.__height: int = 1

    def setLeft(self, left: AVLNode) -> None:
        self.__left = left

    def getLeft(self) -> AVLNode:
        return self.__left

    def setRight(self, right: AVLNode) -> None:
        self.__right = right

    def getRight(self) -> AVLNode:
        return self.__right

    def setHeight(self, height: int) -> None:
        errorAssert(height > 0, "Invalid height.")
        self.__height = height

    def getHeight(self) -> int:
        return self.__height

    def setKey(self, key: Any) -> None:
        errorAssert(key is not None, "Invalid node key.")
        self.__key: Any = key

    def getKey(self) -> Any:
        return self.__key

    def getLeftKey(self) -> Any:
        if self.__left is None:
            return None
        else:
            return self.__left.getKey()

    def getRightKey(self) -> Any:
        if self.__right is None:
            return None
        else:
            return self.__right.getKey()
