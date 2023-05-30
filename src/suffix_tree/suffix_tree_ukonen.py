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
        self.end = []
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
    
    def __hash__(self) -> int:
        """Hask method for the node
        """
        return hash((self.start, self.end[0], self.idx))


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
        self.leaf_end = [0]
        self.root_end = [0]
        self.split_end = -1
        self.size = -1
        self.build_tree()

    def new_node(self, start: int, end: list[int]) -> UkkonenTreeNode:
        node = UkkonenTreeNode()
        node.link = self.root
        node.start = start
        node.end = end
        node.idx = -1
        return node

    def edge_length(self, node):
        if node == self.root or node is None:
            return 0

        return node.end[0] - node.start + 1

    def walk_down(self, node):
        if self.active_length >= self.edge_length(node):
            self.active_edge += self.edge_length(node)
            self.active_length -= self.edge_length(node)
            self.active_node = node
            return True
        return False

    def extend_suffix_tree(self, pos: int):
        self.leaf_end[0] = pos
        self.remainning_suffixes += 1
        self.last_new_node = None
        while self.remainning_suffixes > 0:
            if self.active_length == 0:
                self.active_edge = pos
            char = self.text[self.active_edge]
            if (
                self.active_node is not None
                and self.active_node.children.get(char) is None
            ):
                self.active_node.children[char] = self.new_node(pos, self.leaf_end)
                
                if self.last_new_node is not None:
                    self.last_new_node.link = self.active_node
                    self.last_new_node = None
            
            elif self.active_node is not None:
                next = self.active_node.children.get(char)
                
                if self.walk_down(next):
                    continue
                
                if self.text[next.start + self.active_length] == self.text[pos]:
                    if self.last_new_node is not None and self.active_node != self.root:
                        self.last_new_node.link = self.active_node
                        self.last_new_node = None
                    self.active_length += 1
                    break
                tmp = next.start + self.active_length - 1
                split_end = [tmp]
                split = self.new_node(next.start, split_end)
                self.active_node.children[char] = split
                split.children[char] = self.new_node(pos, self.leaf_end)
                next.start += self.active_length
                split.children[self.text[next.start]] = next
                if self.last_new_node is not None:
                    self.last_new_node.link = split
                self.last_new_node = split
            self.remainning_suffixes -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainning_suffixes + 1
            elif self.active_node != self.root and self.active_node:
                self.active_node = self.active_node.link if self.active_node is not None else self.root
            
    def build_tree(self):
        self.size = len(self.text)
        tmp = -1
        self.root_end = [tmp]
        self.root = self.new_node(-1, self.root_end)
        self.active_node = self.root
        for i in range(self.size):
            self.extend_suffix_tree(i)

    def indices(self, substr: str):
        word = substr
        idx = 0
        cur = self.root
        while cur is not None and idx < len(word):
            char = word[idx]
            cur = cur.children.get(char)
            idx += 1
        if cur is None:
            return []
        stack = [cur]
        visited = {cur}
        indices = [cur.start]
        while stack:
            cur = stack.pop()
            print(cur.children)
            for child in cur.children.values():
                if child not in visited:
                    print(1)
                    stack.append(child)
                    indices.append(child.start)
        return indices

# import timeit
# with open(__file__, 'r') as f:
#     a = timeit.timeit(lambda: UkkonenTree(f.read()), number=10000)
#     print(a)