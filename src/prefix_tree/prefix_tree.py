"""
Prefix Tree
"""

class PrefixTree:
    """
    Prefix Tree
    """
    def __init__(self) -> None:
        pass

    def add_word(self, word: str) -> None:
        """
        Add word to the tree
        """
        pass

class Node:
    """
    Node for prefix tree
    """
    def __init__(self, letters = []):
        self.letters = letters

class Letter:
    """
    Letter for prefix tree
    """
    def __init__(self, value = None, child = None, is_end = False):
        self.value = value
        self.child = child
        self.is_end = is_end
