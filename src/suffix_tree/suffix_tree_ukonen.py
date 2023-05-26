# flake8: noqa
"""
The Ukkonen suffix tree algorithm

The algorithm was taken from
https://rosettacode.org/wiki/Ukkonen%E2%80%99s_suffix_tree_construction
"""


class UkkonenTreeNode:
    """
    The tree node
    """

    def __init__(self):
        self.start = -1
        self.end = -1
        self.idx = -1
        self.link: "UkkonenTreeNode | None" = None
        self.children = {}

    def __repr__(self):
        return f"""UkkonenTreeNode(
            start={self.start}
            end={self.end}
            idx={self.idx}
            link={self.link}
            children={self.children}
        )
        """


class UkkonenTree:
    """
    The ukkonen tree
    """

    def __init__(self, text: str):
        self.text = text
        self.root = UkkonenTreeNode()
        self.active_node: UkkonenTreeNode | None = None
        self.last_new_node: UkkonenTreeNode | None = None
        self.active_edge = -1
        self.active_length = 0
        self.remainning_suffixes = 0
        self._leaf_end = -1
        self.root_end = -1
        self.spliit_end = -1
        self.size = -1
        self.leaves = []
        self.build_tree()

    @property
    def leaf_end(self) -> int:
        return self._leaf_end

    @leaf_end.setter
    def leaf_end(self, val):
        self._leaf_end = val
        for node in self.leaves:
            node.end = val

    def new_node(self, start: int, end: int) -> UkkonenTreeNode:
        node = UkkonenTreeNode()
        node.link = self.root
        node.start = start
        node.end = end
        node.idx = -1
        self.leaves.append(node)
        return self.leaves[-1]

    def edge_length(self, node):
        if node == self.root or node is None:
            return 0

        return node.end - node.start + 1

    def walk_down(self, node):
        if self.active_length >= self.edge_length(node):
            self.active_edge += self.edge_length(node)
            self.active_length -= self.edge_length(node)
            self.active_node = node
            return True
        return False

    def extend_suffix_tree(self, pos: int):
        self.leaf_end = pos
        self.remainning_suffixes += 1
        self.last_new_node = None
        while self.remainning_suffixes > 0:
            if self.active_length > 0:
                self.active_edge = pos

            char = self.text[self.active_edge]

            if (
                self.active_node is not None
                and self.active_node.children.get(char) is None
            ):
                self.active_node.children[char] = self.new_node(
                    pos, self.leaf_end
                )
                if self.last_new_node is not None:
                    self.last_new_node.link = self.active_node
                    self.last_new_node = None
            elif self.active_node is not None:
                next = self.active_node.children.get(char)
                if self.walk_down(next) or next is None:
                    continue

                if (
                    self.text[next.start + self.active_length]
                    == self.text[pos]
                ):
                    if (
                        self.last_new_node is not None
                        and self.active_node != self.root
                    ):
                        self.last_new_node.link = self.active_node
                        self.last_new_node = None
                    self.active_length += 1
                    break

                tmp = next.start + self.active_length - 1
                self.spliit_end = tmp
                split = self.new_node(next.start, self.leaf_end)
                next.start += self.active_length
                split.children[self.text[next.start]] = next

                if self.last_new_node is not None:
                    self.last_new_node.link = split

                self.last_new_node = split

            self.remainning_suffixes -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainning_suffixes + 1
            elif (
                self.active_node != self.root and self.active_node is not None
            ):
                self.active_node = self.active_node.link

    def build_tree(self):
        self.size = len(self.text)
        tmp = -1
        self.root_end = tmp
        self.root = self.new_node(-1, self.root_end)
        self.active_node = self.root
        for i in range(self.size):
            self.extend_suffix_tree(i)

    def indices(self, substr: str):
        word = substr
        return 0
