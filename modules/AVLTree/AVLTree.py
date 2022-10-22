from __future__ import annotations
from .AVLNode import AVLNode
from typing import Any, List


class AVLTree:
    def __init__(self) -> None:
        self.root: AVLNode = None

    @staticmethod
    def LT(key1: Any, key2: Any, compare: Any) -> bool:
        if(compare is None):
            return key1 < key2
        else:
            return compare(key1, key2) == -1

    @staticmethod
    def GT(key1: Any, key2: Any, compare: Any) -> bool:
        if(compare is None):
            return key1 > key2
        else:
            return compare(key1, key2) == 1

    @staticmethod
    def EQ(key1: Any, key2: Any, compare: Any) -> bool:
        if(compare is None):
            return key1 == key2
        else:
            return compare(key1, key2) == 0

    def insertHelper(self, root: AVLNode, key: Any, compare: Any = None) -> AVLNode:

        if not root:
            return AVLNode(key)
        elif self.LT(key, root.getKey(), compare):
            root.setLeft(self.insertHelper(root.getLeft(), key, compare))
        elif(self.GT(key, root.getKey(), compare)):
            root.setRight(self.insertHelper(root.getRight(), key, compare))
        else:
            return root

        root.setHeight(1 + max(self.getHeight(root.getLeft()),
                               self.getHeight(root.getRight())))

        balance = self.getBalance(root)

        if balance > 1 and self.LT(key, root.getLeftKey(), compare):
            return self.rightRotate(root)

        if balance < -1 and self.GT(key, root.getRightKey(), compare):
            return self.leftRotate(root)

        if balance > 1 and self.GT(key, root.getLeftKey(), compare):
            root.setLeft(self.leftRotate(root.getLeft()))
            return self.rightRotate(root)

        if balance < -1 and self.LT(key, root.getRightKey(), compare):
            root.setRight(self.rightRotate(root.getRight()))
            return self.leftRotate(root)

        return root

    def insert(self, key: Any, compare: Any = None) -> None:
        self.root = self.insertHelper(self.root, key, compare)

    def deleteHelper(self, root: AVLNode, key: Any, compare: Any = None) -> AVLNode:

        if not root:
            return root

        elif self.LT(key, root.getKey(), compare):
            root.setLeft(self.deleteHelper(root.getLeft(), key, compare))

        elif self.GT(key, root.getKey(), compare):
            root.setRight(self.deleteHelper(root.getRight(), key, compare))

        else:
            if root.getLeft() is None:
                temp = root.getRight()
                root = None
                return temp

            elif root.getRight() is None:
                temp = root.getLeft()
                root = None
                return temp

            temp = self.getLeftmost(root.getRight())
            root.setKey(temp.getKey())
            root.setRight(self.deleteHelper(root.getRight(),
                                            temp.getKey(),
                                            compare))

        if root is None:
            return root

        root.setHeight(1 + max(self.getHeight(root.getLeft()),
                               self.getHeight(root.getRight())))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.getLeft()) >= 0:
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.getRight()) <= 0:
            return self.leftRotate(root)

        if balance > 1 and self.getBalance(root.getLeft()) < 0:
            root.setLeft(self.leftRotate(root.getLeft()))
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.getRight()) > 0:
            root.setRight(self.rightRotate(root.getRight()))
            return self.leftRotate(root)

        return root

    def delete(self, key: Any, compare: Any = None) -> None:
        self.root = self.deleteHelper(self.root, key, compare)

    def leftRotate(self, z: AVLNode) -> AVLNode:

        y = z.getRight()
        T2 = y.getLeft()

        y.setLeft(z)
        z.setRight(T2)

        z.setHeight(1 + max(self.getHeight(z.getLeft()),
                            self.getHeight(z.getRight())))

        y.setHeight(1 + max(self.getHeight(y.getLeft()),
                            self.getHeight(y.getRight())))

        return y

    def rightRotate(self, z: AVLNode) -> AVLNode:

        y = z.getLeft()
        T3 = y.getRight()

        y.setRight(z)
        z.setLeft(T3)

        z.setHeight(1 + max(self.getHeight(z.getLeft()),
                            self.getHeight(z.getRight())))

        y.setHeight(1 + max(self.getHeight(y.getLeft()),
                            self.getHeight(y.getRight())))

        return y

    def getHeight(self, root: AVLNode) -> int:
        if not root:
            return 0

        return root.getHeight()

    def getBalance(self, root: AVLNode) -> int:
        if not root:
            return 0

        return self.getHeight(root.getLeft()) - self.getHeight(root.getRight())

    def getLeftmost(self, root: AVLNode) -> AVLNode:
        if root is None or root.getLeft() is None:
            return root

        return self.getLeftmost(root.getLeft())

    def inOrderHelper(self, root: AVLNode, nodesList: List[Any]) -> None:

        if not root:
            return

        self.inOrderHelper(root.getLeft(), nodesList)
        nodesList.append(root.getKey())
        self.inOrderHelper(root.getRight(), nodesList)

    def inOrder(self) -> List[Any]:
        nodes = []
        self.inOrderHelper(self.root, nodes)
        return nodes

    def getRightmost(self, root: AVLNode) -> AVLNode:
        if root is None or root.getRight() is None:
            return root
        return self.getRightmost(root.getRight())

    def printHelper(self, currPtr: AVLNode, indent: str, last: bool):
        if currPtr != None:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            print(currPtr.getKey())
            self.printHelper(currPtr.getLeft(), indent, False)
            self.printHelper(currPtr.getRight(), indent, True)

    def print(self) -> None:
        self.printHelper(self.root, "", True)

    def findHelper(self, root: AVLNode, key: Any, compare: Any = None) -> AVLNode:
        if((root is None) or ((root.getKey() == key) if (compare is None) else (compare(key, root.getKey()) == 0))):
            return root

        elif (((key < root.getKey()) if (compare is None) else (compare(key, root.getKey()) == -1))):
            return self.findHelper(root.getLeft(), key, compare)

        else:
            return self.findHelper(root.getRight(), key, compare)

    def find(self, key: Any, compare: Any = None) -> AVLNode:
        return self.findHelper(self.root, key, compare)

    def inOrderSuccessorHelper(self, root: AVLNode, successor: AVLNode, key: Any, compare: Any = None) -> AVLNode:
        if((root is None)):
            return root

        elif((root.getKey() == key) if (compare is None) else (compare(key, root.getKey()) == 0)):
            return successor

        elif (((key < root.getKey()) if (compare is None) else (compare(key, root.getKey()) == -1))):
            successor = root
            return self.inOrderSuccessorHelper(root.getLeft(), successor, key, compare)

        else:
            return self.inOrderSuccessorHelper(root.getRight(), successor, key, compare)

    def inOrderSuccessor(self, key: Any, compare: Any = None) -> AVLNode:
        return self.inOrderSuccessorHelper(self.root, None, key, compare)

    def successor(self, key: Any, compare: Any = None) -> Any:
        node: AVLNode = self.find(key, compare)

        if(node is None):
            return node

        elif(node.getRight() is not None):
            successor = self.getLeftmost(node.getRight())

        else:
            successor = self.inOrderSuccessor(key, compare)

        if(successor is not None):
            return successor.getKey()
        else:
            return None

    def inOrderPredecessorHelper(self, root: AVLNode, predecessor: AVLNode, key: Any, compare: Any = None) -> AVLNode:
        if((root is None)):
            return root

        elif((root.getKey() == key) if (compare is None) else (compare(key, root.getKey()) == 0)):
            return predecessor

        elif (((key < root.getKey()) if (compare is None) else (compare(key, root.getKey()) == -1))):
            return self.inOrderPredecessorHelper(root.getLeft(), predecessor, key, compare)

        else:
            predecessor = root
            return self.inOrderPredecessorHelper(root.getRight(), predecessor, key, compare)

    def inOrderPredecessor(self, key: Any, compare: Any = None) -> AVLNode:
        return self.inOrderPredecessorHelper(self.root, None, key, compare)

    def predecessor(self, key: Any, compare: Any = None) -> Any:
        node: AVLNode = self.find(key, compare)

        if(node is None):
            return node

        elif(node.getLeft() is not None):
            predecessor = self.getRightmost(node.getLeft())

        else:
            predecessor = self.inOrderPredecessor(key, compare)

        if(predecessor is not None):
            return predecessor.getKey()
        else:
            return None
