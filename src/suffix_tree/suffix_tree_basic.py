"""The suffix tree module.

The suffix tree is used to search for substring in linear time
"""

from typing import Iterator

from b_tree.b_tree import BTreeNode, IterableWithLen, NodeValue


class SufTreeNode(BTreeNode):
    """Suffix tree node."""

    def __init__(self, val: NodeValue | None = None, idx: int = -1):
        """Init for suffix tree node."""
        super().__init__(val)
        self.indices: list[int] = [idx]


class BasicSuffixTree:
    """The suffix tree class."""

    def __init__(self, text: IterableWithLen[NodeValue] | None = None):
        """Init for the basic suffix tree."""
        self.root = SufTreeNode()
        if text is not None:
            self.root = self.build_from_iterable(text)

    def build_from_iterable(self, iterable: IterableWithLen[NodeValue]) -> SufTreeNode:
        """Build the tree from iterable."""
        root = SufTreeNode()
        for suffix, start in self.suffixes(iterable):
            cur: SufTreeNode = root
            idx = 0
            while idx < len(suffix):
                val = cur[suffix[idx]]
                if val is not None:
                    cur = val
                else:
                    cur.add_child(SufTreeNode(suffix[idx], start + idx))
                    cur = cur[suffix[idx]]

                if start + idx not in cur.indices:
                    cur.indices.append(start + idx)
                idx += 1
        return root

    def indices(self, string: IterableWithLen[NodeValue]) -> list[int]:
        """Get indices for iterable."""
        cur = self.root
        idx = 0
        while idx < len(string):
            val = cur[string[idx]]
            if val is None:
                return []
            else:
                cur = val
            idx += 1
        return [idx - len(string) + 1 for idx in cur.indices]

    @staticmethod
    def suffixes(iterable: IterableWithLen[NodeValue]) -> Iterator[NodeValue]:
        """Get all the suffixes from the iterable."""
        for start in range(len(iterable)):
            yield (iterable[start:], start)

    @property
    def leaves(self) -> int:
        """Get the leaves."""
        return self.root.leaves
