from PyQt6.QtCore import QEvent, QPoint, Qt  # type: ignore
from PyQt6.QtGui import QTextCursor  # type: ignore
from PyQt6.QtWidgets import QMenu  # type: ignore
from PyQt6.QtWidgets import QVBoxLayout  # type: ignore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QProxyStyle,
                             QStyleOptionMenuItem, QTextEdit, QWidget)

from prefix_tree.prefix_tree import PrefixTree


class MenuProxyStyle(QProxyStyle):
    def drawControl(self, element, opt, p, w):
        if element == 14:
            menuitem = QStyleOptionMenuItem(opt)
            text = menuitem.text
            menuitem.text = ""
            QProxyStyle.drawControl(self, element, menuitem, p, w)
            if text == "":
                return
            padding = 8
            text_flags = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            p.drawText(
                menuitem.rect.adjusted(padding, 0, -padding, 0),
                text_flags,
                text,
            )


class PopupMenu(QMenu):
    """Popup menu for auto complete that closes on any keypress."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyle(MenuProxyStyle(self.style()))
        self.__parent = parent

    def keyPressEvent(self, event):
        if not self.isVisible():
            return
        # If tab or enter
        if event.key() in (16777217, 16777220):
            super().keyPressEvent(event)
            return
        self.close()
        self.__parent.setFocus()
        self.__parent.keyPressEvent(event)


class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.words_dict = {}
        self.previous_word = ""
        self.auto_complete_tree = PrefixTree()

        self.cursorPositionChanged.connect(self.cursor_moved)

    def cursor_moved(self):
        cursor = self.textCursor()
        current_text = self.toPlainText()
        current_text_words = current_text.replace("\n", " ").split(" ")
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        cursor_word = cursor.selectedText()

        if self.previous_word and self.previous_word not in current_text_words:
            del self.words_dict[self.previous_word]

        self.previous_text = current_text

        self.previous_word = cursor_word

        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        current_word = cursor.selectedText()

        if current_word:
            if current_word not in self.words_dict:
                self.words_dict[current_word] = 1
            else:
                self.words_dict[current_word] += 1

        self.auto_complete_tree = PrefixTree()
        self.auto_complete_tree.create_tree((word for word in self.words_dict))
        completion = [self.auto_complete_tree.autocomplete(current_word)] or []
        if not completion or not all(isinstance(word, str) for word in completion):
            return
        self.context_menu = PopupMenu(self)
        for word in completion:
            action = self.context_menu.addAction(word)
            if isinstance(word, str):
                to_insert = word[len(current_word) :]
            else:
                to_insert = word
            action.triggered.connect(
                lambda _, text=to_insert: self.insertPlainText(text)
            )
        self.context_menu.exec(
            self.mapToGlobal(self.cursorRect().topLeft() + QPoint(0, 20))
        )
        self.setFocus()

    def focusOutEvent(self, event):
        if event.type() == QEvent.Type.FocusOut:
            # Perform custom behavior when the widget loses focus
            self.setFocus()
        else:
            super().focusOutEvent(event)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Title")
        self.setGeometry(640, 480, 600, 480)

        self.textBox = CustomTextEdit()
        self.textBox.setPlainText("")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.textBox)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)

        self.setCentralWidget(centralWidget)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
