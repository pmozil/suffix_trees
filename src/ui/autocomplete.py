from PyQt6.QtGui import QTextCursor  # type: ignore
from PyQt6.QtWidgets import QVBoxLayout  # type: ignore
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget


class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.words_dict = {}
        self.previous_word = ""

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
