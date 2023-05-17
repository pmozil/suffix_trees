"""
The suffix tree module.
The suffix tree is used to search for substring in linear time
"""


from ..b_tree import BTreeNode, IterableWithLen, NodeValue


class BasicSuffixTree:
    """
    The suffix tree class.
    """

    def __init__(self, text: IterableWithLen[NodeValue] | None = None):
        """
        Init for the basic suffix tree
        """
        self.root = BTreeNode()
        if text is not None:
            self.root = self.build_from_iterable(text)

    def build_from_iterable(
        self, iterable: IterableWithLen[NodeValue]
    ) -> BTreeNode[NodeValue]:
        """
        Build the tree from iterable
        """
        root = BTreeNode()
        for suffix in self.suffixes(iterable):
            cur: BTreeNode = root
            idx = 0
            while idx < len(suffix):
                val = cur[suffix[idx]]
                if val is not None:
                    cur = val
                else:
                    cur.add_child(BTreeNode(suffix[idx]))
                    cur: BTreeNode = cur[suffix[idx]]
                idx += 1
        return root

    @staticmethod
    def suffixes(iterable: IterableWithLen[NodeValue]) -> list:
        """
        Get all the suffixes from the iterable
        """
        return [iterable[start:] for start in range(len(iterable))]

    @property
    def leaves(self) -> int:
        """
        Get the leaves
        """
        return self.root.leaves
