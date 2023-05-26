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
        self.is_leaf = True
        self.children = children
        self.indices = indices
        self.remainder = ""

    def __eq__(self, other) -> bool:
        """
        Eq for the node
        """
        return self.val == other.val

    def __repr__(self) -> str:
        """
        Repr for node
        """
        return f"""UkkonenTreeNode(
                val = "{self.val}",
                children = {self.children},
                indices={self.indices})\n"""


class UkkonenTree:
    """
    The Ukkonen suffix tree
    """

    def __init__(self, text: str):
        """
        Init for the basic suffix tree
        """
        self.nodes = [UkkonenTreeNode()]
        self.active_point = None
        for idx in range(len(text)):
            self.add_suffix(text[idx], idx)

    def add_suffix(self, char: str, orig_idx: int):
        """
        Add a suffix to the tree
        """
        if self.active_point is not None:
            node = self.active_point
            print("Match: ", node.val)

            if node.remainder.startswith(char) and char:
                node.val += char
                node.remainder = node.remainder[1:]
                node.indices.append(orig_idx)

            elif node.remainder:
                suffix = node.remainder
                node.remainder = ""
                node.indices.append(orig_idx)

                node.is_leaf = False

                if not suffix.endswith(char):
                    suffix += char

                node.children = []
                old_suffix_node = UkkonenTreeNode(
                    suffix,
                    node.children,
                    node.indices + [orig_idx + len(node.val)],
                )

                for idx, i in enumerate(self.nodes):
                    if old_suffix_node == i:
                        i.indices.extend(old_suffix_node.indices)
                        i.children.extend(old_suffix_node.children)
                        node.children.append(idx)
                        break
                else:
                    node.children.append(len(self.nodes))
                    self.nodes[0].children.append(len(self.nodes))
                    self.nodes.append(old_suffix_node)

                new_suffix_node = UkkonenTreeNode(
                    char, [], [orig_idx + len(node.val)]
                )

                for idx, i in enumerate(self.nodes):
                    if new_suffix_node == i:
                        i.indices.extend(new_suffix_node.indices)
                        i.children.extend(new_suffix_node.children)
                        node.children.append(idx)
                        break
                else:
                    node.children.append(len(self.nodes))
                    self.nodes[0].children.append(len(self.nodes))
                    self.nodes.append(new_suffix_node)
                # Set only the two new suffixes to be the nodes's children,
                # as not to make any loops
                self.active_point = None
                return

        branch_matched = False
        for node in self.nodes:
            if node.is_leaf and node.val:
                node.val += char

            if node.val.startswith(char) and char:
                branch_matched = True
                self.active_point = node
                node.val = char
                node.remainder = node.val[1:]
                node.indices.append(orig_idx)

            node.indices = list(set(node.indices))
            node.children = list(set(node.children))

        if not branch_matched:
            self.nodes[0].children.append(len(self.nodes))
            self.nodes.append(UkkonenTreeNode(char, [], [orig_idx]))

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
