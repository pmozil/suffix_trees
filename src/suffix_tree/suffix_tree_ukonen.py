"""
The Ukkonen suffix tree algorithm
"""


class UkkonenTreeNode:
    """
    The suffix tree node
    """

    def __init__(
        self, val: str = "", children: list[int] = [], indices: list[int] = []
    ):
        """
        Init for suffix tree node
        """
        self.val = val
        self.children = children
        self.indices = indices

    def __repr__(self) -> str:
        """
        Repr for node
        """
        return (
            f'UkkonenTreeNode(val = "{self.val}", children = {self.children})'
        )


class UkkonenTree:
    """
    The Ukkonen suffix tree
    """

    def __init__(self, text: str):
        """
        Init for the basic suffix tree
        """
        self.nodes = [UkkonenTreeNode()]
        for idx in range(len(text)):
            self.add_suffix(text[idx:], idx)

    def add_suffix(self, suffix: str, orig_idx: int):
        """
        Add a suffix to the tree
        """
        chr_idx = 0
        # find the last fitting child
        node = 0
        while chr_idx < len(suffix):
            child_idx = 0
            while True:
                children = self.nodes[node].children
                if child_idx == len(children):
                    new_node = len(self.nodes)
                    self.nodes.append(
                        UkkonenTreeNode(
                            suffix[chr_idx:], [], [chr_idx + orig_idx]
                        )
                    )
                    self.nodes[node].children.append(new_node)
                    return
                new_node = children[child_idx]

                print(new_node, len(self.nodes), self.nodes[new_node])

                if (
                    not self.nodes[new_node].val
                    or self.nodes[new_node].val[0] == suffix[chr_idx]
                ):
                    break
                child_idx += 1
            substitute = self.nodes[new_node].val
            j = 0
            while j < len(substitute):
                if suffix[chr_idx + j] != substitute:
                    prev = new_node
                    new_node = len(self.nodes)
                    self.nodes.append(
                        UkkonenTreeNode(
                            substitute[:j], [], [orig_idx + chr_idx]
                        )
                    )
                    self.nodes[prev].val = substitute[j:]
                    self.nodes[prev].indices = [
                        node + j for node in self.nodes[prev].indices
                    ]
                    self.nodes[node].children[child_idx] = new_node
                    break
                j += 1
            chr_idx += j
            node = new_node

    def __repr__(self) -> str:
        """
        Repr for the tree
        """
        nodes = "\n".join(str(x) for x in self.nodes)
        return f"UkkonenTree(nodes = \n{nodes})"

    # def __str__(self) -> str:
    #     """
    #     Str method
    #     """
    #     if len(self.nodes) == 0:
    #         return ""

    #     def f(n, pre):
    #         res = ""
    #         children = self.nodes[n].children
    #         if len(children) == 0:
    #             res += "-- " + self.nodes[n].val + "\n"
    #             return res
    #         res += "+-" + self.nodes[n].val + "\n"
    #         for c in children[:-1]:
    #             res += pre + "+-\n"
    #             res += f(c, pre + " | ")
    #         res += pre + "+-\n"
    #         res += f(children[-1], pre + "  ")
    #         return res

    #     return f(0, "")
