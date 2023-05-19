"""
Prefix Tree
"""

class PrefixTree:
    """
    Prefix Tree
    """
    def __init__(self) -> None:
        self._head = Node(letters=[])
    
    @staticmethod
    def get_letter(value, letters):
        '''Return a Letter with value if it is inside. Else None.'''
        for letter in letters:
            if letter.value == value:
                return letter

    def add_word(self, word: str, node = None) -> None:
        """
        Add word to the tree.
        """
        current_node = self._head if node is None else node # if it is the first letter of a word -> None
        letter = self.get_letter(word[0], current_node.letters)
        print(current_node)

        if len(word) == 1: # it is the end of the word
            if letter: # the word is already exist
                letter.is_end = True
            else:
                current_node.letters.append(Letter(word[0], is_end = True))
            print(current_node)
        else:
            if letter: # the part of the word is already exist
                if not letter.child:
                    letter.child = Node(letters=[])

                next_node = letter.child

                print(current_node)
                print(next_node)

                self.add_word(word[1:], next_node)
            else:
                new_letter = Letter(word[0], child = Node(letters=[]))
                current_node.letters.append(new_letter)

                print(new_letter.child.letters is current_node.letters)
                '''Леттер має порожній нод, але як тільки я в каррент роблю
                аппенд, то обидва ноди отримують леттер.'''

                print(current_node)

                next_node = new_letter.child

                self.add_word(word[1:], next_node)

class Node:
    """
    Node for prefix tree
    """
    def __init__(self, letters = []):
        self.letters = letters # a list of Letter

    def __str__(self):
        res = ''
        for let in self.letters:
            res += ' ' + str(let)

        return res

class Letter:
    """
    Letter for prefix tree
    """
    def __init__(self, value = None, child = None, is_end = False):
        self.value = value # letter
        self.child = child # Node(letters=[])
        self.is_end = is_end # if the letter can be the end of a word
    
    def __str__(self):
        return str(self.value)
 
