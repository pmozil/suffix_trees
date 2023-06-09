"""Prefix Tree."""
from typing import Iterable


class PrefixTree:
    """Prefix Tree."""

    def __init__(self) -> None:
        self._head = Node(letters=[])

    @staticmethod
    def get_letter(value, letters):
        """Return a Letter with value if it is inside.

        Else None.
        """
        for letter in letters:
            if letter.value == value:
                return letter

    def add_word(self, word: str, node=None) -> None:
        """Add word to the tree."""
        # if it is the first letter of a word -> None
        current_node = self._head if node is None else node
        letter = self.get_letter(word[0], current_node.letters)

        if len(word) == 1:  # it is the end of the word
            if letter:  # the word is already exist
                letter.is_end = True
            else:
                current_node.letters.append(Letter(word[0], is_end=True))
        else:
            if letter:  # the part of the word is already exist
                if not letter.child:
                    letter.child = Node(letters=[])

                next_node = letter.child

                self.add_word(word[1:], next_node)
            else:
                new_letter = Letter(word[0], child=Node(letters=[]))
                current_node.letters.append(new_letter)

                next_node = new_letter.child

                self.add_word(word[1:], next_node)

    def __str__(self):
        """Returns a string representation with the tree rotated 90 degrees
        counterclockwise."""

        def recurse(node, level):
            res = ""
            if node is not None:
                for letter in node.letters:
                    if letter.child:
                        res += recurse(letter.child, level + 1)
                    if letter.is_end:
                        res += "\n" + " |" * level + str(letter.value) + "."
                    else:
                        res += "\n" + " |" * level + str(letter.value) + " "
            return res

        return recurse(self._head, 0)

    def read_file(self, path):
        """Read file and return list of words."""
        self.words_lst = []
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                word = line.split(" ")[0].strip()
                if word != "":
                    self.words_lst.append(word)
        return self.words_lst

    def create_tree(self, words: Iterable):
        """Create a tree from a list of words."""
        for word in words:
            self.add_word(word)

    def autocomplete(self, prefix: str):
        """Return a word with the prefix."""
        if prefix == "":
            return None

        def search_word(node, prefix):
            ret_lst = []
            for letter in node.letters:
                if letter.is_end:
                    ret_lst.append(prefix + letter.value)
                if letter.child:
                    ret_lst += search_word(letter.child, prefix + letter.value)
            return ret_lst

        current_node = self._head
        for letter in prefix:
            for let in current_node.letters:
                if let.value == letter:
                    current_node = let.child
                    break
            else:
                return None
        if current_node is None:
            return None
        return search_word(current_node, prefix)


class Node:
    """Node for prefix tree."""

    def __init__(self, letters=[]):
        self.letters = letters  # a list of Letter

    def __str__(self):
        return str(self.letters)


class Letter:
    """Letter for prefix tree."""

    def __init__(self, value=None, child=None, is_end=False):
        self.value = value  # letter
        self.child = child  # Node(letters=[])
        self.is_end = is_end  # if the letter can be the end of a word

    def __repr__(self):
        return str(self.value)


if __name__ == "__main__":
    tree = PrefixTree()
    tree.create_tree(tree.read_file("base.lst"))
    print(tree.autocomplete("коде"))
    print(tree.autocomplete("заклин"))
