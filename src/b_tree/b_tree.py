"""
The B-tree module.
The B-tree wil serve as the basis for both the prefix and suffix trees
"""
from __future__ import annotations

from typing import Generic, TypeVar

from typing_extensions import Protocol

Tree = TypeVar("Tree", bound="BTree")


class NodeValueProtocol(Protocol):
    """
    Protocol for eq
    """

    def __eq__(self, other: "NodeValueProtocol") -> bool:
        return False


NodeValue = TypeVar("NodeValue", bound="NodeValueProtocol")


class IterableWithLen(Generic[NodeValue], Protocol):
    """
    Iterable with len protocol
    """

    def __iter__(self):
        """
        Iter method
        """
        ...

    def __len__(self) -> int:
        """
        Len method for the  protocol
        """
        return 0

    def __getitem__(self, key):
        """
        Getitem for the protocol
        """
        ...


class BTreeNode(Generic[NodeValue]):
    """
    The prefix tree class

    Attributes:
        val - the leaf's value
        children - the chlidren of the B-Tree

    Methods:
        add_child(child: BTreeNode[NodeValue]) - add a child to the tree
        leaves() -> int - get number of leaves the tree has
    """

    def __init__(self, val: NodeValue | None = None):
        """
        Init for BTreeNode

        Args:
            root: NodeVal | None - the value of root node. could be None
        """
        self.__val: NodeValue | None = val
        self.__children = []
        self.is_leaf: bool = True

    @property
    def val(self) -> NodeValue | None:
        """
        Getter for val
        """
        return self.__val

    @val.setter
    def val(self, value: NodeValue):
        """
        Setter for val
        """
        if not isinstance(value, type(self.__val)) and self.__val is not None:
            return

        self.__val = value

    def add_child_from_val(self, value: NodeValue):
        """
        Add a child from value
        """
        self.__children.append(type(self)(value))

    def add_child(self, child):
        """
        Add child to current node

        Args:
            child: Self - the child node
        """
        if not isinstance(child, type(self)):
            return

        if child not in self.__children:
            self.__children.append(child)
            self.is_leaf = False

    @property
    def children(self) -> list:
        """
        Get the children of the node
        """
        return self.__children

    @property
    def leaves(self) -> int:
        """
        Get number of leaves.

        Returns:
        """
        children: int = 0
        stack: list = self.__children

        while stack:
            node = stack.pop(0)
            if node.is_leaf:
                children += 1
            stack.extend(node.children)

        return children

    def __getitem__(self, key: "NodeValue"):
        """
        Getitem for BTreeNode
        """
        for item in self.children:
            if item.val == key:
                return item
        return None

    def __eq__(self, other) -> bool:
        """
        Eq method for BTreeNode
        """
        if other is not type(self):
            return False

        return self.__val == other.val


class BTree(Generic[NodeValue]):
    """
    The B-Tree class
    """

    def __init__(self, root: NodeValue | None = None):
        """
        Init for BTree. Gives an empty tree
        """
        self.root = BTreeNode(root)

    @property
    def leaves(self) -> int:
        """
        Get the number of the tree's leaves

        Returns:
            int - the number of leaves
        """
        return self.root.leaves
